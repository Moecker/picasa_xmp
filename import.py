# Requirements
# python -m pip install --upgrade pip setuptools
# sudo apt install python3-pip
# pip install lxml
# pip install image
# sudo python -m  pip install matplotlib
# sudo apt install python-tk

from __future__ import division
from PIL import Image
from lxml import html, etree

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.patches as patches

IMAGE_NAME = "IMG_20180909_124837.jpg"

# This function will extract the XMP Bag Tag
def Get_XMP_Bag_Tag(file):
    # initialize our return data
    file_data = None
    try:
        # attempt to open the file as binary
        file_as_binary = open(file,'rb')
        # if it opened try to read the file
        file_data = file_as_binary.read()
        # close the file afterward done
        file_as_binary.close()
    except:
        # if we sell the open the file abort
        return False, None

    # if the file is empty abort
    if file_data is None:
        return False, None

    # using the file data, attempt to locate the starting XMP XML Bag tag
    xmp_start = file_data.find('<rdf:Bag')
    # also try and locate the ending XMP XML Bag tag
    xmp_end = file_data.find('</rdf:Bag')
    # if the tag is found, -1 is used and we get "" else we get data
    xmp_bag = file_data[xmp_start:xmp_end+len("</rdf:Bag>")]

    # if nothing is found abort
    if xmp_bag == "":
        return False, None

    #  if we found something, return tag information
    return True, xmp_bag


# extract the XMP BAG information using the previous function
found, value = Get_XMP_Bag_Tag(IMAGE_NAME)
# if data was found, then process this data
if found:
    # Because lxml has strict XML syntax standards, a XML root with namespaces
    # must be provided
    rawxml = """<root xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:mwg-rs="http://www.metadataworkinggroup.com/schemas/regions/"
                xmlns:stArea="http://ns.adobe.com/xmp/sType/Area#"
                xmlns:stDim="http://ns.adobe.com/xap/1.0/sType/Dimensions#"
                xmlns:xmp="http://ns.adobe.com/xap/1.0/"> %s </root>""" % value
    # adding a root also added a extra child we must ignore via [0]
    # getchildren() will return all rdf:li tags
    root = etree.fromstring(rawxml).getchildren()[0].getchildren()
    # making a array to hold tag information
    tags = []
    # iterate through each rdf:li tag
    for li in list(root):
        # dig into rdf:li via [0] to access the child rdf:Description tag
        li2 = li[0]
        # extract the XMP tag name
        name = li2.get('{http://www.metadataworkinggroup.com/schemas/regions/}Name')
        # every rdf:Description has 1 child mwg-rs:Area that defines the tag location
        # extract this information via getchildren() and [0]
        li3 = li2.getchildren()[0]
        # the extract the normalized center X, Y coordinates
        # and the total rectangle size
        x = li3.get('{http://ns.adobe.com/xmp/sType/Area#}x')
        y = li3.get('{http://ns.adobe.com/xmp/sType/Area#}y')
        w = li3.get('{http://ns.adobe.com/xmp/sType/Area#}w')
        h = li3.get('{http://ns.adobe.com/xmp/sType/Area#}h')
        # save the information into the tag array
        tags.append((name,float(x),float(y),float(w),float(h)))


#  define your JPG image here
TheImagePath = IMAGE_NAME
# open the image
TheImage = Image.open(TheImagePath)
# extract the width and height of the image in pixels
img_width, img_height = TheImage.size

# assuming tags were defined previously,  process each tag found
faces = []
for name, x, y, width, height in tags:
    # convert normalized XMP x, y center coordinates into relative pixel coordinates
    center_x = x*img_width
    center_y = y*img_height

    # convert normalized XMP width and height into relative pixel coordinates
    total_width = width*img_width
    total_height = height*img_height

    # calculate half width and height in order to determine rectangular coordinates
    half_width = total_width/2.0
    half_height = total_height/2.0

    # calculate web rectangular coordinates from center coordinates
    top = center_y-half_height
    bottom = center_y+half_height
    left= center_x-half_width
    right = center_x+half_width

    face = {"name": name, "top": top, "bottom": bottom, "left": left, "right": right}
    faces.append(face)
    print(face)


img = mpimg.imread(IMAGE_NAME)

fig, ax = plt.subplots(1)
imgplot = ax.imshow(img)

for face in faces:
    rect = patches.Rectangle(
        (face["left"],
         face["top"]),
         face["right"]-face["left"],
         face["bottom"]-face["top"],
         linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)

plt.show()

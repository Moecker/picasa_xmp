from lxml import html, etree


def get_xmp_bag_tag(file):
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
    xmp_start = file_data.find(b'<rdf:Bag')
    # also try and locate the ending XMP XML Bag tag
    xmp_end = file_data.find(b'</rdf:Bag')
    # if the tag is found, -1 is used and we get "" else we get data
    xmp_bag = file_data[xmp_start:xmp_end+len(b"</rdf:Bag>")]

    # if nothing is found abort
    if xmp_bag == b"":
        return False, None

    return True, xmp_bag


def encode(name):
    name = name.replace('\\xc3\\x9f', 'ẞ')
    name = name.replace('\\xc3\\xa4', 'ä')
    name = name.replace('\\xc3\\xb6', 'ö')
    name = name.replace('\\xc3\\xbc', 'ü')
    return name


def get_face_tags(file_path):
    # making a array to hold tag information
    tags = []
    # extract the XMP BAG information using the previous function
    found, value = get_xmp_bag_tag(file_path)
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

            name = encode(name)

            tags.append((name, float(x), float(y), float(w), float(h)))

    return found, tags

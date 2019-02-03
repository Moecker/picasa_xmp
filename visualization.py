import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.patches as patches


def visualize(file_path, faces):
    img = mpimg.imread(file_path)
    fig, axis = plt.subplots(1)
    imgplot = axis.imshow(img)

    for face in faces:
        rect = patches.Rectangle(
            (face["left"], face["top"]),
             face["right"]-face["left"],
             face["bottom"]-face["top"],
             linewidth=2, edgecolor='r', facecolor='none')
        axis.add_patch(rect)
    plt.show()


def visualize_faces(files_with_tags, plot=False):
    for file_with_tag in files_with_tags:
        list_of_name = [faces.get("name") for faces in file_with_tag.get("faces")]
        print("File {} which has faces {}".format(file_with_tag.get("file"), list_of_name))
        if plot:
            visualize(file_with_tag.get("file"), file_with_tag.get("faces"))

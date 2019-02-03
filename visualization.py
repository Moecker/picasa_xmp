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

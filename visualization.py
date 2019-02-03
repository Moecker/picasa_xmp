import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.patches as patches
import math
from tqdm import tqdm
import logging


def visualize_face(file_path, face):
    img = mpimg.imread(file_path)

    top = int(face["top"])
    height = int(face["bottom"]-face["top"])
    left = int(face["left"])
    width = int(face["right"]-face["left"])
    img = img[top:top+height , left:left+width, :]
    return img


def visualize_face_in_files(files_with_name):
    if len(files_with_name) == 0:
        return
    logging.info("Prepare plotting images...")

    rows_cols = math.ceil(math.sqrt(len(files_with_name)))
    rows = rows_cols
    cols = rows_cols
    fig, ax = plt.subplots(nrows=rows_cols, ncols=rows_cols)

    logging.info("Ploting images...")
    for i, file_with_name in enumerate(tqdm(files_with_name)):
        file_path = file_with_name.get("file")
        face = file_with_name.get("face")
        img = visualize_face(file_path, face)

        plt.imshow(img, aspect="auto")
        fig.add_subplot(rows, cols, i+1)
    plt.show()


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
        logging.debug("File {} which has faces {}".format(file_with_tag.get("file"), list_of_name))
        if plot:
            visualize(file_with_tag.get("file"), file_with_tag.get("faces"))

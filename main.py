from xmp import get_face_tags
from visualization import visualize

import argparse
import os
from PIL import Image
from random import shuffle


def get_file_paths(image_dir):
    file_paths = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG"):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    return file_paths


def get_face_poses_from_tags(image, tags):
    img_width, img_height = image.size

    faces = []
    for name, x, y, width, height in tags:
        center_x = x*img_width
        center_y = y*img_height

        total_width = width*img_width
        total_height = height*img_height

        half_width = total_width/2.0
        half_height = total_height/2.0

        top = center_y-half_height
        bottom = center_y+half_height
        left= center_x-half_width
        right = center_x+half_width

        face = {"name": name, "top": top, "bottom": bottom, "left": left, "right": right}
        faces.append(face)
    return faces


def visualize_faces(files_with_tags):
    for file_with_tag in files_with_tags:
        list_of_name = [faces.get("name") for faces in file_with_tag.get("faces")]
        print("File {} has faces {}".format(file_with_tag.get("file"), list_of_name))
        visualize(file_with_tag.get("file"), file_with_tag.get("faces"))


def sample_paths(image_dir):
    NUMBER_OF_SAMPLES = 20
    file_paths = get_file_paths(image_dir)
    shuffle(file_paths)
    file_paths = file_paths[1:NUMBER_OF_SAMPLES]
    return file_paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', help='image_dir help')
    args = parser.parse_args()

    file_paths = sample_paths(args.image_dir)

    files_with_tags = []
    for file_path in file_paths:
        print("Analysing {}".format(file_path))
        found, tags = get_face_tags(file_path)
        if found:
            image = Image.open(file_path)
            faces = get_face_poses_from_tags(image, tags)
            files_with_tags.append({"file":file_path, "faces":faces})

    visualize_faces(files_with_tags)



if __name__ == "__main__":
    main()

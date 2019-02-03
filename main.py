from xmp import get_face_tags
from visualization import visualize
from face_extraction import get_face_poses_from_tags

import time
from tqdm import tqdm
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


def visualize_faces(files_with_tags):
    for file_with_tag in files_with_tags:
        list_of_name = [faces.get("name") for faces in file_with_tag.get("faces")]
        print("File {} has faces {}".format(file_with_tag.get("file"), list_of_name))
        visualize(file_with_tag.get("file"), file_with_tag.get("faces"))


def sample_paths(image_dir):
    NUMBER_OF_SAMPLES = 100
    file_paths = get_file_paths(image_dir)
    shuffle(file_paths)
    file_paths = file_paths[1:NUMBER_OF_SAMPLES ]
    return file_paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', help='image_dir help')
    args = parser.parse_args()

    file_paths = sample_paths(args.image_dir)

    files_with_tags = []
    for file_path in tqdm(file_paths)   :
        found, tags = get_face_tags(file_path)
        if found:
            image = Image.open(file_path)
            faces = get_face_poses_from_tags(image, tags)
            files_with_tags.append({"file":file_path, "faces":faces})

    visualize_faces(files_with_tags)



if __name__ == "__main__":
    main()

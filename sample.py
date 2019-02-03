import logging
import argparse
import time
import pickle
import os

from tqdm import tqdm
from PIL import Image
from random import shuffle

from xmp import get_face_tags
from visualization import visualize_faces
from face_extraction import get_face_poses_from_tags


def get_file_paths(image_dir):
    file_paths = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG"):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    return file_paths


def sample_paths(image_dir, number_samples):
    file_paths = get_file_paths(image_dir)
    shuffle(file_paths)
    file_paths = file_paths[0:min(number_samples, len(file_paths))]
    return file_paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', help='Directory containing the images')
    parser.add_argument('--number_samples', help='Number of sample from (randomized) paths',
                        default=20)
    parser.add_argument('--pickle_file', help='Pickle file (acts as database)',
                        default="files_with_tags.p")

    args = parser.parse_args()

    file_paths = sample_paths(args.image_dir, int(args.number_samples))
    logging.info("Found {} file(s) to analyse".format(len(file_paths)))

    files_with_tags = []
    for file_path in tqdm(file_paths):
        logging.debug("Analysing {}".format(file_path))
        found, tags = get_face_tags(file_path)
        if found:
            logging.debug("Found {} face tags".format(len(tags)))
            image = Image.open(file_path)
            faces = get_face_poses_from_tags(image, tags)
            files_with_tags.append({"file":file_path, "faces":faces})

    logging.info("Found {} file(s) with face tags".format(len(files_with_tags)))
    pickle.dump(files_with_tags, open(args.pickle_file, "wb"))


if __name__ == "__main__":
    logging.basicConfig(filename='sample.log',level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    main()

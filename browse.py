import logging
import pickle
import argparse

from tqdm import tqdm

from visualization import visualize_faces


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pickle_file', help='Pickle file (acts as database)',
                        default="files_with_tags.p")
    parser.add_argument('--plot', help='Shall plot face tags?',
                        default="no")

    args = parser.parse_args()

    logging.info("Loading pickle file...")
    files_with_tags = pickle.load(open(args.pickle_file, "rb"))
    logging.info("Loadad {} file(s) with face tags".format(len(files_with_tags)))

    shall_plot = True if args.plot == "yes" else False
    visualize_faces(files_with_tags, shall_plot)

    for file_with_tag in tqdm(files_with_tags):
        for tags in file_with_tag.get("faces"):
            name = tags.get("name")
            if name == "Jana Wenig":
                print(tags.get("left"))


if __name__ == "__main__":
    logging.basicConfig(filename='sample.log',level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    main()

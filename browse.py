import logging
import pickle
import argparse

from tqdm import tqdm

from visualization import visualize_faces, visualize_face_in_files


def find_faces(search_name, files_with_tags):
    search_name = search_name
    files_with_name = []
    for file_with_tag in files_with_tags:
        for tags in file_with_tag.get("faces"):
            name = tags.get("name")
            if search_name in name:
                file_name = file_with_tag.get("file")
                files_with_name.append({"name":name, "file":file_with_tag.get("file"), "face":tags})
    return files_with_name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pickle_file', help='Pickle file (acts as database)',
                        default="files_with_tags.p")
    parser.add_argument('--search_name', help='Name to search in database')
    parser.add_argument('--plot', help='Shall plot face tags?',
                        default="no")

    args = parser.parse_args()
    shall_plot = True if args.plot == "yes" else False

    logging.info("Loading pickle file...")
    files_with_tags = pickle.load(open(args.pickle_file, "rb"))
    logging.info("Loadad {} file(s) with face tags".format(len(files_with_tags)))

    search_name = args.search_name
    files_with_name = find_faces(search_name, files_with_tags)
    logging.info("Found {} faces for {}".format(len(files_with_name), search_name))


    if shall_plot:
        visualize_faces(files_with_tags, False)
        visualize_face_in_files(files_with_name)


if __name__ == "__main__":
    logging.basicConfig(filename='sample.log',level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    main()

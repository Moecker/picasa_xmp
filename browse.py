import logging
import pickle
import argparse

from tqdm import tqdm

from visualization import visualize_faces, visualize_face_in_files


def make_face_to_file_dict(files_with_tags):
    faces_to_filetags_dict = {}
    for file_with_tag in files_with_tags:
        for tags in file_with_tag.get("faces"):
            name = tags.get("name")
            if name not in faces_to_filetags_dict:
                faces_to_filetags_dict[name] = []
            else:
                file_name = file_with_tag.get("file")
                faces_to_filetags_dict[name].append({"file":file_with_tag.get("file"), "face":tags})
    return faces_to_filetags_dict


def find_faces(search_name, files_with_tags):
    files_with_name = []
    for file_with_tag in files_with_tags:
        names_in_file = {}
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
    parser.add_argument('--search_name', help='Name to search in database', default="")
    parser.add_argument('--plot', help='Shall plot face tags?',
                        default="no")

    args = parser.parse_args()
    shall_plot = True if args.plot == "yes" else False

    logging.info("Loading pickle file...")
    files_with_tags = pickle.load(open(args.pickle_file, "rb"))
    logging.info("Loadad {} file(s) with face tags".format(len(files_with_tags)))

    search_name = args.search_name
    files_with_name = find_faces(search_name, files_with_tags)
    logging.info("Found {} face(s) for search '{}''".format(len(files_with_name), search_name))

    faces_to_filetags_dict = make_face_to_file_dict(files_with_tags)
    logging.info("Found {} different face(s)".format(len(faces_to_filetags_dict.keys())))
    for key, value in sorted(faces_to_filetags_dict.items(), key=lambda kv: len(kv[1]), reverse=True):
        print("{} appears in {} images".format(key, len(value)))

    if shall_plot:
        visualize_faces(files_with_tags, False)
        visualize_face_in_files(files_with_name)


if __name__ == "__main__":
    logging.basicConfig(filename='sample.log',level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    main()

from visualization import visualize_face

import pickle

files_with_tags = pickle.load(open("test.p", "rb"))
files_with_tag = files_with_tags[0]
visualize_face(files_with_tag.get("file"), files_with_tag.get("faces")[0])

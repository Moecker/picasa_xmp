# Picasa XMP Face Tag Extraction
Playground to obtain Picasa xmp name tags from images

# Installation
conda env create -f environment.yml
source activate picasa_xmp

# Usage
Create the database and store into pickle file:
```
python sample.py --image_dir /home/samo/xmp/images --pickle_file all_files.p --number_samples 1000
```

Browse database from pickle file:
```
python browse.py  --pickle_file all_files.p --plot yes
```

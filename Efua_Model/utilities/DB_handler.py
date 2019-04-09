import glob
import os
import sys
import base64
from os.path import join

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["efua_V1"]
mycol = mydb["photos"]

data_path = "/home/sai-pher/work/Project_Efua/Efua_model/data/efua_V1/photos"


# use time stamp to select data to pull.

def get_labels():
    return [f.name for f in os.scandir(data_path) if f.is_dir()]


def db_load(time):
    # read files in directory into a list

    # read all photos from db
    for x in mycol.find({"time": {"$gt": str(time)}}):
        label = x["label"]
        name = x["name"]
        image = x["photo"]

        # for each photo, if label in file_d: add photo to file_d, else: create new file in file_d and put photo in
        # file.

        if x["label"] not in get_labels():
            os.mkdir(join(data_path, label))

        with open(join(data_path, label, name + ".png"), "w") as photo:
            photo.write(image)

        sys.stdout.flush()

# my_find("photo")

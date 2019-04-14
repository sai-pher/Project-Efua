import base64
import os
from os.path import join

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["efua_V1"]
mycol = mydb["photos"]

if os.path.exists("/home/sai-pher/work/Project_Efua/Efua_Model"):
    # Change the current working Directory
    os.chdir("/home/sai-pher/work/Project_Efua/Efua_Model")
    print("working dir: " + os.getcwd())
else:
    print("Can't change the Current Working Directory")

data_path = "./data/efua_V1/photos"
model_path = "./models"
results_path = "./models/results"


# use time stamp to select data to pull.

def get_labels():
    return [f.name for f in os.scandir(data_path) if f.is_dir()]

    pass


def db_load():
    # read files in directory into a list

    # read all photos from db
    for x in mycol.find({}):
        label = x["label"]
        name = x["name"]
        image = x["photo"]

        # for each photo, if label in file_d: add photo to file_d, else: create new file in file_d and put photo in
        # file.

        if x["label"] not in get_labels():
            try:
                os.mkdir(join(data_path, label))
                with open(join(data_path, label, name), "wb") as photo:
                    photo.write(base64.b64decode(image))
                with open(join(results_path, "label.txt"), "a") as label_txt:
                    label_txt.write(label + "\n")
            except:
                print("failed to mkdir")
        else:
            if not os.path.exists(join(data_path, label, name)):
                with open(join(data_path, label, name), "wb") as photo:
                    photo.write(base64.b64decode(image))

        # sys.stdout.flush()


db_load()
# my_find("photo")

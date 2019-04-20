import base64
import json
import os
from datetime import datetime
from os.path import join

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["efua_V1"]
photo_collection = mydb["photos"]
caltech_collection = mydb["caltech14"]
model_collection = mydb["models"]

if os.path.exists("/home/sai-pher/work/Project_Efua/Efua_Model"):
    # Change the current working Directory
    os.chdir("/home/sai-pher/work/Project_Efua/Efua_Model")
    print("working dir: " + os.getcwd())
else:
    print("Can't change the Current Working Directory")

data_path = "./data/efua_V1/photos"
cal_data_path = "./data/efua_V1/caltech_14"
model_path = "./models"
results_path = "./models/results"


# use time stamp to select data to pull.

def get_labels(d_path):
    return [f.name for f in os.scandir(d_path) if f.is_dir()]


def get_files(d_path, name):
    return [f.name for f in os.scandir(join(d_path, name))]


def build_label_dict(d_path):
    labels = get_labels(d_path)

    d = {}

    for label in labels:
        path = join(d_path, label)
        d[label] = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])

    return json.dumps(d)


def image_download(caltech=False, d_path=data_path):
    # read files in directory into a list
    if caltech is True:
        collection = caltech_collection
    else:
        collection = photo_collection
    # read all photos from db
    for x in collection.find({}):
        label = x["label"]
        name = x["name"]
        image = x["photo"]

        # for each photo, if label in file_d: add photo to file_d, else: create new file in file_d and put photo in
        # file.

        if x["label"] not in get_labels(d_path):
            try:
                os.mkdir(join(d_path, label))
                with open(join(d_path, label, name), "wb") as photo:
                    photo.write(base64.b64decode(image))
                with open(join(results_path, "label.txt"), "a") as label_txt:
                    label_txt.write(label + "\n")
            except:
                print("failed to mkdir")
        else:
            if not os.path.exists(join(d_path, label, name)):
                with open(join(d_path, label, name), "wb") as photo:
                    photo.write(base64.b64decode(image))


def model_upload(d_path, tflite, num_classes, num_data, t_time, sess, epochs):
    time = datetime.now()

    n = model_collection.count_documents({})
    model_collection.insert_one({"name": "tf_model-" + str(n + 1),
                                 "tflite_model": tflite,
                                 "lables": get_labels(d_path),
                                 "time": str(time),
                                 "train_time": t_time,
                                 "number": sess,
                                 "epochs": epochs,
                                 "trained_classes": num_classes,
                                 "trained_images": num_data,
                                 "class_count": build_label_dict(d_path)})


def image_uplaod():
    c = 0
    for l in get_labels(cal_data_path):
        f_l = get_files(cal_data_path, l)
        for f_n in f_l:
            im = open(join(cal_data_path, l, f_n), "rb")

            im = base64.b64encode(im.read())

            print("#{}|| wrinting: {} from: {}".format(c, f_n, l))
            caltech_collection.insert_one({"name": f_n,
                                           "label": l,
                                           "photo": im})
            c += 1

            # print({"name": f_n,
            #        "label": l,
            #        "photo": "i"})

        print("Written - {} photos - to label: {}".format(c, l))

    print("Successfully uploaded {} photos".format(c))

from models.basemodel import *
from utilities.DB_handler import *
from utilities.utils import *

tf.logging.set_verbosity(tf.logging.WARN)

load_weights = False
load_model = False
write_tensorboard = True

caltech = True

try:
    with open(join(results_path, "sess.txt"), "r") as sess_f:
        sess = int(sess_f.read())
except:
    sess = 0

try:
    os.mkdir(join(results_path, "session_" + str(sess)))
    res_url = results_path + "/session_" + str(sess)

    os.mkdir(join(res_url, "trained_models"))
    os.mkdir(join(res_url, "logs"))
    os.mkdir(join(res_url, "converted_models"))
except:
    print("Failed to make {}".format(join(results_path, str(sess))))
    res_url = results_path

data_url = "./data/efua_V1/photos"
cal_data_url = "./data/efua_V1/caltech_14"
saved_model_weights_url = "{0}/trained_models/saved_model_weights.h5".format(res_url)
saved_model_url = "{0}/trained_models/saved_model.h5".format(res_url)
log_dir = "{0}/logs/def_log".format(res_url)
tflite_model_path = "{0}/converted_models".format(res_url)

batch_size = 32
image_size = 250
epochs = 10

if caltech is True:
    d_url = cal_data_url
else:
    d_url = data_path

print("Training from: {}.....\n session: {}".format(d_url, sess))

# get data
start = datetime.now()
image_download(caltech=caltech, d_path=d_url)
finish = datetime.now()
print("DB load finished at: " + diff(start, finish))

model = BaseModel(load_weights=load_weights,
                  load_model=load_model,
                  write_tensorboard=write_tensorboard,
                  data_url=d_url,
                  saved_model_url=saved_model_url,
                  saved_model_weights_url=saved_model_weights_url,
                  log_dir=log_dir,
                  batch_size=batch_size,
                  image_size=image_size)

start = datetime.now()
if model.train(epochs=epochs):
    tflite_model = model.convert(tflite_model_path, "converted_model")
    if tflite_model[0]:
        print("models ready for export.")
        finish = datetime.now()

        model_upload(d_url, tflite_model[1], model.num_classes, model.num_data, diff(start, finish), sess, epochs)

print("Training finished at: " + diff(start, finish))

with open(join(results_path, "sess.txt"), "w") as sess_w:
    sess_w.write(str(sess + 1))

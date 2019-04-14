from models.base_model import *
from utilities.DB_handler import *
from utilities.utils import *

load_weights = False
load_model = False
write_tensorboard = True

data_url = "./data/efua_V1/photos"
saved_model_weights_url = "./models/results/trained_models/saved_model_weights.h5"
saved_model_url = "./models/results/trained_models/saved_model.h5"
log_dir = "./models/results/logs/def_log"
tflite_model_path = "./models/results/converted_models"

batch_size = 32
image_size = 250

# get data
start = datetime.now()
db_load()
finish = datetime.now()
print("DB load finished at: " + diff(start, finish))

model = Base_model(load_weights=load_weights,
                   load_model=load_model,
                   write_tensorboard=write_tensorboard,
                   data_url=data_url,
                   saved_model_url=saved_model_url,
                   saved_model_weights_url=saved_model_weights_url,
                   log_dir=log_dir,
                   batch_size=batch_size,
                   image_size=image_size)

start = datetime.now()
if model.train(epochs=1):
    if model.convert(tflite_model_path, "converted_model"):
        print("models ready for export.")

finish = datetime.now()
print("Training finished at: " + diff(start, finish))

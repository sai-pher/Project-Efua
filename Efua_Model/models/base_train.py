import os
from datetime import datetime

from dateutil.relativedelta import relativedelta
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.python.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D
from tensorflow.python.keras.layers.normalization import BatchNormalization
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.models import save_model


def diff(t_a, t_b):
    t_diff = relativedelta(t_b, t_a)  # later/end time comes first!
    return '{h}h {m}m {s}s'.format(h=t_diff.hours, m=t_diff.minutes, s=t_diff.seconds)


batch_size = 10
image_size = 250

if os.path.exists("/home/sai-pher/work/Project_Efua/Efua_Model"):
    # Change the current working Directory
    os.chdir("/home/sai-pher/work/Project_Efua/Efua_Model")
    print("working dir: " + os.getcwd())
else:
    print("Can't change the Current Working Directory")

data_url = "./data/efua_V1/photos"
saved_model_weights_url = "./models/trained_models/saved_model_weights.h5"
saved_model_url = "./models/trained_models/saved_model.h5"
log_dir = "./models/logs/def_log"
tflite_model_path = "./models/converted_models"

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
    data_url,  # this is the target directory
    target_size=(image_size, image_size),  # all images will be resized to 150x150
    batch_size=batch_size,
    class_mode='categorical',
    subset="training")  # since we use binary_cross_entropy loss, we need binary labels

# this is a similar generator, for validation data
validation_generator = train_datagen.flow_from_directory(
    data_url,
    target_size=(image_size, image_size),
    batch_size=batch_size,
    class_mode='categorical',
    subset="validation")

"""

Model

"""
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=[image_size, image_size, 3], strides=2))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(BatchNormalization())
# model.add(Dropout(0.25))

# model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(BatchNormalization())
# model.add(Dropout(0.25))

# model.add(MaxPooling2D(pool_size=(3, 3), strides=2))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), strides=2))
model.add(Activation('relu'))
model.add(BatchNormalization())
# model.add(Dropout(0.25))
# model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# model.add(Conv2D(128, (5, 5)))
# model.add(Activation('relu'))

model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
model.add(Dense(1024))
model.add(Activation('relu'))
# model.add(Dense(1024))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(train_generator.num_classes))
model.add(Activation('softmax'))

# model.load_weights("saved_weights.h5")

model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
              metrics=['accuracy'])

tensor_b = TensorBoard(log_dir="./logs_mod_ts2" + str(datetime.now()), histogram_freq=1, write_graph=True,
                       write_images=False)

start = datetime.now()

print("starting at: " + diff(start, datetime.now()))
print(train_generator.num_classes)

model.fit_generator(
    train_generator,
    steps_per_epoch=train_generator.n // batch_size,
    epochs=1,
    validation_data=validation_generator,
    validation_steps=validation_generator.n // batch_size,
    callbacks=[tensor_b],
    use_multiprocessing=True,
    workers=4)
model.save_weights("./models/model_weights.h5")  # always save your weights after training or during training

save_model(model=model, filepath="./models/model.h5", overwrite=True, include_optimizer=True)

finish = datetime.now()

print("finished at: " + diff(start, finish))

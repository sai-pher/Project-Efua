from os.path import join

import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.python.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D
from tensorflow.python.keras.layers.normalization import BatchNormalization
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.models import save_model


class BaseModel:

    def __init__(self,
                 data_url,
                 batch_size,
                 image_size,
                 load_weights=False,
                 saved_model_weights_url="saved_model_weights.h5",
                 load_model=False,
                 saved_model_url="saved_model.h5",
                 write_tensorboard=True,
                 log_dir="logs/def_log"):

        self.batch_size = batch_size
        self.image_size = image_size

        # booleans
        self.load_weights_bool = load_weights
        self.load_model_bool = load_model
        self.write_tensorboard_bool = write_tensorboard

        # URL's
        self.data_url = data_url
        self.saved_model_weights_url = saved_model_weights_url
        self.saved_model_url = saved_model_url
        self.log_dir = log_dir

        # Data
        data = self.datagen(self.data_url, self.image_size, self.batch_size)
        self.num_data = data[0]
        self.num_classes = data[1]
        self.training_data = data[2]
        self.validation_data = data[3]

        # model
        self.model = self.model_build(num_classes=self.num_classes,
                                      image_size=self.image_size,
                                      load_weights=self.load_weights_bool,
                                      saved_model_weights_url=self.saved_model_weights_url,
                                      load_model=False, saved_model_url=None)

        self.tensorboard_callback = self.write_tensorboard(write=self.write_tensorboard_bool, log_dir=self.log_dir)

    def model_build(self,
                    num_classes,
                    image_size,
                    load_weights=False, saved_model_weights_url=None,
                    load_model=False, saved_model_url=None):

        model = None

        if load_model:
            if saved_model_url:
                model = tf.keras.models.load_model(saved_model_url)
            else:
                print("no model specified")

        else:
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

            model.add(Flatten())
            model.add(Dense(1024))
            model.add(Activation('relu'))
            # model.add(Dense(1024))
            model.add(BatchNormalization())
            model.add(Dropout(0.5))
            model.add(Dense(num_classes))
            model.add(Activation('softmax'))

            if load_weights is True:
                if saved_model_weights_url:
                    model.load_weights(saved_model_weights_url)
                else:
                    print("no model weights specified")

            model.compile(loss='categorical_crossentropy',
                          optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
                          metrics=['accuracy'])

        return model

    def datagen(self, data_url, image_size, batch_size):

        datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            validation_split=0.2)

        train_generator = datagen.flow_from_directory(
            data_url,
            target_size=(image_size, image_size),
            batch_size=batch_size,
            class_mode='categorical',
            subset="training")

        validation_generator = datagen.flow_from_directory(
            data_url,
            target_size=(image_size, image_size),
            batch_size=batch_size,
            class_mode='categorical',
            subset="validation")

        num_data = train_generator.n
        num_classes = train_generator.num_classes

        return num_data, num_classes, train_generator, validation_generator

    def write_tensorboard(self, write=True, log_dir=None):

        tensor_board = None
        if write is True:
            if log_dir:
                tensor_board = TensorBoard(log_dir=log_dir, histogram_freq=1, write_graph=True,
                                           write_images=False)
            else:
                print("log_dir: {log} -> invalid or does not exist.".format(log=log_dir))

        return tensor_board

    def train(self,
              epochs,
              save_weights=True,
              _save_model=True):

        train = self.training_data
        valid = self.validation_data
        batch_size = self.batch_size
        tensor_b = self.tensorboard_callback
        weights_save_path = self.saved_model_weights_url
        model_save_path = self.saved_model_url

        self.model.fit_generator(
            train,
            steps_per_epoch=self.num_data // batch_size,
            epochs=epochs,
            validation_data=valid,
            validation_steps=self.num_data // batch_size,
            callbacks=[tensor_b])

        if save_weights is True:
            if weights_save_path:
                self.model.save_weights(weights_save_path)
            else:
                print("Weights path: {path} -> invalid or does not exist.".format(path=weights_save_path))

        if _save_model is True:
            if model_save_path:
                save_model(model=self.model, filepath=model_save_path, overwrite=True, include_optimizer=True)
            else:
                print("Model path: {path} -> invalid or does not exist.".format(path=model_save_path))

        return True

    def convert(self, conversion_path, conversion_name):
        converter = tf.lite.TFLiteConverter.from_keras_model_file(self.saved_model_url)
        print("Converting model to TfLite.....")
        tflite_model = converter.convert()
        try:
            open(join(conversion_path, conversion_name + ".tflite"), "wb").write(tflite_model)
        except:
            print("Conversion path: {path} -> invalid or does not exist.".format(path=conversion_path))
        print("Model written!")

        return True, tflite_model

    def summary(self):
        return self.model.summary()

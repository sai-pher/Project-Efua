var mongoose = require("mongoose");

var Schema = mongoose.Schema;

var ModelSchema = new Schema(
    {
        name: {type: String},
        tflite_model: {type: Buffer},
        lables: {type: Array},
        time: {type: String},
        train_time: {type: Date},
        number: {type: Number},
        epochs: {type: Number},
        trained_classes: {type: Number},
        trained_images: {type: Number},
        class_count: {type: String}
    }
);

module.exports = mongoose.model(('models'), ModelSchema);

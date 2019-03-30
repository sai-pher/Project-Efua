var mongoose = require("mongoose");

var Schema = mongoose.Schema;

var PhotoSchema = new Schema(
    {
        label: {type: String, required: true},
        name: {type: String, required: true},
        photo: {type: String, required: false}
    }
);

module.exports = mongoose.model(('Photo'), PhotoSchema);
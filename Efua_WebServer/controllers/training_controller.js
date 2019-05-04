var {PythonShell} = require('python-shell');
const {spawn} = require('child_process');
const cron = require('node-cron');

var models = require('../models/models');

const python_path = "/home/sai-pher/work/Project_Efua/Efua_Model/venv/bin/python";
const script_path = "/home/sai-pher/work/Project_Efua/Efua_Model";


exports.train = function (req, res) {

    let options = {
        pythonPath: python_path,
        scriptPath: script_path,
    };
    // TODO: create train activation logic


    PythonShell.run('train_handler.py', options, function (err, data) {
        if (err) res.send(err.message);

        // send data here

        // res.write(data.slice(-2));
    });

    res.send("training....")
};

exports.update = function (req, res) {

    models.find({}).sort({number: -1}).limit(1).exec(function (err, result) {
        if (err)
            res.send(err);
        else
            res.send(result[0].tflite_model)
    })


};

cron.schedule("30 20 * * *", function () {
    let options = {
        pythonPath: python_path,
        scriptPath: script_path,
    };
    // TODO: create train activation logic


    PythonShell.run('train_handler.py', options, function (err, data) {
        if (err) console.log(err.message);

        // send data here

        // res.write(data.slice(-2));
    });

    console.log("training....")
});


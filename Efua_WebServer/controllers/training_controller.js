var {PythonShell} = require('python-shell');
const {spawn} = require('child_process');

const python_path = "/home/sai-pher/work/Project_Efua/Efua_Model/venv/bin/python";
const script_path = "/home/sai-pher/work/Project_Efua/Efua_Model";

exports.train_test = function (req, res) {
    // PythonShell.run('/home/sai-pher/work/test_projects/CNN_test/models/train.py', null, function (err, data) {
    //     if (err) res.send(err);
    //     res.send(data.toString())
    // });

    console.log("starting training");
    var process = spawn('python', ["/home/sai-pher/work/test_projects/CNN_test/models/mock_train.py", req.params.id]);

    console.log("training.....");

    process.stdout.on('data', function (data) {
        res.render("display_view", {message: data.toString()});
    });

    console.log("training from server complete!")

};

exports.train = function (req, res) {

    let options = {
        pythonPath: python_path,
        scriptPath: script_path,
    };
    // TODO: create train activation logic

    PythonShell.run('train_handler.py', options, function (err, data) {
        if (err) res.send(err.message);
        res.send(data.slice(-2))
    });



};


exports.db_pull = function (req, res) {
    var options = {
        // pythonPath: "path", TODO: use virtual env path here
        args: ["label"]
    };
    PythonShell.run('/home/sai-pher/work/test_projects/CNN_test/mongo_test.py', options, function (err, data) {
        if (err) res.send(err);
        res.send(data.toString())
    });
};


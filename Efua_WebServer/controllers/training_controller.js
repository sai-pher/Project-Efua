var {PythonShell} = require('python-shell');
const {spawn} = require('child_process');

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
    // PythonShell.run('/home/sai-pher/work/test_projects/CNN_test/models/train.py', null, function (err, data) {
    //     if (err) res.send(err);
    //     res.send(data.toString())
    // });

    console.log("starting training");
    var process = spawn('python', ["/home/sai-pher/work/test_projects/CNN_test/models/train.py", 10]);

    console.log("training.....");

    process.stdout.on('data', function (data) {
        console.log("display_view", {message: data.toString()});
    });

    res.render("display_view", {message: "Training started"});

    console.log("training from server complete!")

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


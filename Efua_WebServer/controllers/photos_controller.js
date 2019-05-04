var Photo = require('../models/photos');
var {PythonShell} = require('python-shell');


const python_path = "/home/sai-pher/work/Project_Efua/Efua_Model/venv/bin/python";
const script_path = "/home/sai-pher/work/Project_Efua/Efua_Model";

// const base64decode = require('nodejs-base64');


exports.photo_list = function (req, res) {
    // res.send('NOT IMPLEMENTED: Photo list');
    Photo.find({})
        .exec(function (err, list_images) {
            if (err) {
                return next(err);
            }
            //Successful, so render
            res.render('gallery', {title: 'Gallery', image_list: list_images});
        });
};
exports.photo_detail = function (req, res) {
    res.send('NOT IMPLEMENTED: Photo detail');
};

exports.photo_create_get = function (req, res) {
    res.send('NOT IMPLEMENTED: Photo create get');
};
exports.photo_create_post = function (req, res) {

    let encoded_photo = req.body.image;
    let photo_label = req.body.label;
    let photo_name = req.body.name;
    // let decoded_photo = base64decode(encoded_photo);

    let photo_obj = new Photo({
        label: photo_label,
        name: photo_name,
        photo: encoded_photo
    });

    photo_obj.save(
        function (err) {

            if (err) {
                // TODO: handle error
                console.log(err);
                console.log("broken");
                res.send("Save Unsuccessful")
            } else {
                Photo.countDocuments({label: photo_label}).exec(function (err, count) {
                    if (err) console.log(err);
                    res.send("Photo Saved!\n" + photo_label + ": " + count);
                });

                // Photo.countDocuments({}).exec(function (err, count) {
                //     if (err)
                //         console.log(err);
                //     else {
                //         if (count % 50 === 0) {
                //             let options = {
                //                 pythonPath: python_path,
                //                 scriptPath: script_path,
                //             };
                //             // TODO: create train activation logic
                //
                //
                //             PythonShell.run('train_handler.py', options, function (err, data) {
                //                 console.log("training...");
                //                 if (err) console.log(err.message);
                //                 else{
                //                     console.log(data.slice(-2))
                //                 }
                //
                //                 // send data here
                //
                //                 // res.write(data.slice(-2));
                //             });
                //         }
                //     }
                // })

            }
        }
    )


};

exports.photo_delete_get = function (req, res) {
    res.send('NOT IMPLEMENTED: Photo delete get');
};
exports.photo_delete_post = function (req, res) {
    res.send('NOT IMPLEMENTED: Photo delete post');
};

exports.photo_update_get = function (req, res) {
    res.send('NOT IMPLEMENTED: Photo update get');
};
exports.photo_update_post = function (req, res) {
    res.send('NOT IMPLEMENTED: Photo update post');
};

exports.photo_test = function (req, res) {
    data = "some text";
    res.render('display_view', data);
};

exports.photo_count = function (req, res) {
    Photo.aggregate({$group: {_id: {label: '$label'}, count: {$sum: 1}}}).exec(function (err, counts) {
        if (err) return err;
        res.send(counts)
    })
};




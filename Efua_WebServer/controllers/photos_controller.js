var Photo = require('../models/photos');
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
            } else
                res.send("Photo Saved!")
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




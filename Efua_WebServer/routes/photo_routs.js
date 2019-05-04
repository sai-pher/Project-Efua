var express = require('express');
var router = express.Router();

var photos_controller = require('../controllers/photos_controller');

router.get('/', function (req, res, next) {
    data = "some text";
    res.render('display_view', {message: 'Photos'}, data);
});

router.get('/create', photos_controller.photo_create_get);
router.post('/create', photos_controller.photo_create_post);

router.get('/:id/delete', photos_controller.photo_delete_get);
router.post('/:id/delete', photos_controller.photo_delete_post);

router.get('/:id/update', photos_controller.photo_update_get);
router.post('/:id/update', photos_controller.photo_update_post);

router.get('/list', photos_controller.photo_list);
router.get('/:id', photos_controller.photo_detail);

router.get('/test', photos_controller.photo_test);

router.get('/counts', photos_controller.photo_count);


module.exports = router;

var express = require('express');
var router = express.Router();

var training_controller = require('../controllers/training_controller');

router.get('/train', training_controller.train);
router.get('/db_check', training_controller.db_pull);
router.get('/:id/train_test', training_controller.train_test);

module.exports = router;

var express = require('express');
var router = express.Router();

var training_controller = require('../controllers/training_controller');

router.get('/train', training_controller.train);
router.post('/update', training_controller.update);

module.exports = router;

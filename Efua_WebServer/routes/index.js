var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {title: 'Express'});
});

router.get('/test', function (req, res, next) {
    res.render('display_view', {message: 'test'});
});

router.get('/ok', function (req, res, next) {
    res.send("A - OK!")
});

module.exports = router;

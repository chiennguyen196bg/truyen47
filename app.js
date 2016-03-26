var express = require('express');

var app = express();
var bodyParser          = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.json({type:'application/vnd.api+json'}));
app.use(bodyParser.urlencoded({extended: true}));
var multipart           = require('connect-multiparty');
var multipartMiddleware = multipart();
var mongoose            = require('mongoose');
var slug = require('slug');

var Post = require('models/post.js')
var Chap = require('models/chap.js');

// app setting
app.use(express.static('public'));
app.set('views','./src/views');

app.set('view engine', 'ejs');


mongoose.connect('mongodb://localhost/admin');

// Khởi tạo đối tượng connection để test kết nối
var dbMongo = mongoose.connection;
// Handle sự kết open và error khi kết nối mongo
dbMongo.on('error', console.error.bind(console, 'connection error:'));

dbMongo.once('open', function(){
    console.log('MongoDb connected');
});



// var genres;
// for(var i = 0; i<temp.length; i++){
// 	genres[i].slug = slug(temp[i]);
// 	genres[i].name = temp[i];
// };


var port = process.env.PORT || 8080;


var router_doctruyen = require('./src/routes/router_doctruyen')();
var router_danhsach = require('./src/routes/router_danhsach')();
var router_json = require('./src/routes/router_json')();
app.get('/', function(req, res){
	Post.find({})
		.limit(20)
        .sort('-lastChap.id')
        .select('name slug lastChap genres')
        .exec(function(err, posts){
            if(err){
                res.send('err');
            } else {
                res.render('index.ejs',{posts: posts});
            }
        });
   
});


app.use('/json', router_json);
app.use('/danh-sach', router_danhsach);
app.use('/', router_doctruyen);






app.listen(port, function(err){
	console.log('runing server on port '+ port);
});
// app.listen(port, function(err){
// 	console.log('running server on port ' + port);
// });


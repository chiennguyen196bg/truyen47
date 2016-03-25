var express = require('express');
var mongoose = require('mongoose');

var slug = require('slug');
var router_doctruyen = express.Router();
var Post = require('models/post.js')
var Chap = require('models/chap.js');


var router = function(){

	router_doctruyen.route('/doc-truyen/:chap_slug')
		.get(function(req, res){
			var chap_slug = req.params.chap_slug;
			Chap.findOne({'slug': chap_slug}).exec(function(err, chap){
				if (err) {
					res.render('404.ejs',{err : err});

				} else{
					Post.findOne({'chapter.slug': chap_slug}).exec(function(err, post){
						if (err) {
							res.render('404.ejs',{err: err});
						} else {
							if(chap!=null&&post!=null)
								res.render('chapter.ejs',{chap : chap, post: post});
							else
								res.render('404.ejs',{err: 'Có cái đéo gì lỗi thì phải'});
						}
					});
				}
			});
		});
	router_doctruyen.route('/:post_slug')
		.get(function(req, res){
			Post.findOne({'slug':req.params.post_slug}).exec(function(err, post){
				if (err) {
					res.render('404.ejs',{err : err});
				}
				else {
					if(post != null){
						var genres_slug = [];
						var len = post.genres.length;
						for (var i = 0; i < len; i++) {
							genres_slug[i] = slug(post.genres[i]).toLowerCase();
						};
						res.render('details.ejs',{post : post, genres : post.genres, genres_slug : genres_slug});
					} else{
						res.render('404.ejs',{err: 'Có cái đéo gì lỗi thì phải'});
					}
				}
			});
		});

	
	return router_doctruyen;
}
module.exports = router;
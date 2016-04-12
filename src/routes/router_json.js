var express = require('express');

var router_json = express.Router();

var Post = require('models/post.js')
var Chap = require('models/chap.js');

var router = function(){
	router_json.route('/random')
		.get(function(req, res){
			Post.count().exec(function(err, count){
				var random = Math.floor(Math.random()*count);
				Post.findOne()
				.skip(random)
				.select('name slug lastChap summary genres')
				.exec(function(err, post){
					res.json(post);
				})
			})
		        
		});

	router_json.route('/moi-update/:num')
		.get(function(req, res){
			var num = Number(req.params.num);
			Post.find({}).limit(num)
		        .sort('-lastChap.id')
		        .select('name slug lastChap genres')
		        .exec(function(err, posts){
		            if(err){
		                res.send('err');
		            } else {
		                res.json(posts);
		            }
		        });
		});

	router_json.route('/moi-dang/:num')
		.get(function(req, res){
			var num = Number(req.params.num);
			Post.find().limit(num)
			.sort({'_id': -1})
			.select('name slug lastChap genres')
			.exec(function(err, posts){
				if(err){
					res.send('err');
				} else {
					res.json(posts);
				}
			});
		});

	router_json.route('/get-all-genres')
		.get(function(req, res){
			Post.distinct('genres')
				
				.exec(function(err, results){
					if(err){
			            res.send('err');
			        } else {
			            res.json(results);
			        }
				});
		});	
	router_json.route('/find-post-by-chap/:chap_slug')
		.get(function(req, res){
			Post.findOne({'chapter.slug': req.params.chap_slug})
			.select('chapter name slug')
			.exec(function(err, post){
	            if(err){
	                res.send('err');
	            } else {
	                res.json(post);
	            }
	        });
		        
		});	
	router_json.route('/search/:data')
		.get(function(req, res){
			Post.find({name:{$regex : req.params.data, $options:"$i"}})
			.exec(function(err, post){
	            if(err){
	                res.send('err');
	            } else {
	                res.json(post);
	            }
	        });
		        
		});	
	router_json.route("/follow")
		.post(function(req, res){
		var data = req.body.data;
		console.log(data);
		Post.find({"slug" : { $in : data } })
			.select("name slug lastChap")
			.exec( function(err, results){
				if(err){
	                res.send('err');
	            } else {
	                res.json(results);
	            }
			});
		});

	router_json.route("/top-of-week/:num")
		.get(function(req, res){
			var num = Number(req.params.num);
			Post.find().limit(num)
			.sort({'views.week': -1})
			.select('name slug lastChap genres')
			.exec(function(err, posts){
				if(err){
					res.send('err');
				} else {
					res.json(posts);
				}
			});
		});

	router_json.route("/top-of-month/:num")
		.get(function(req, res){
			var num = Number(req.params.num);
			Post.find().limit(num)
			.sort({'views.month': -1})
			.select('name slug lastChap genres')
			.exec(function(err, posts){
				if(err){
					res.send('err');
				} else {
					res.json(posts);
				}
			});
		});


	
	return router_json;
}
module.exports = router;
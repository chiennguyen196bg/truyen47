var express = require('express');
var mongoose = require('mongoose');

var Post = require('models/post')
var Chap = require('models/chap');
var router_danhsach = express.Router();
var reslug = function(text){
	if(text=='huyen-huyen') 
		return 'Huyền Huyễn';
	else{
		text = text.replace('-',' ');
		var text1 = text.substr(0,1);
		text1 = text1.toUpperCase();
		var text2= text.slice(1);
		return text1 + text2;
	}
};

var convert = function(text){
	if (text == 'moi-update')
		return {
			find : {},
			sort :'-lastChap.id',
			realName : 'Mới cập nhập'
		}
	else if (text == 'moi-dang')
		return {
			find : {},
			sort : '-id',
			realName : "Mới đăng"
		}
	else if (text == 'hot-update')
		return {
			find : {},
			sort : '-views',
			realName : "Hot update"
		}
	else if (text == 'hoan-thanh')
		return {
			find : {'status':"Hoàn thành"},
			sort : '-id',
			realName : "Hoàn thành"
		}
	else{
		return {
			find : {},
			sort : '-id',
			realName : text
		}
	}
	
};

var router = function(){

	router_danhsach.route('/the-loai/:name')
		.get(function(req, res){
			var name = req.params.name;
			var realName = reslug(name);
			var arg = {'genres' : realName}
			Post.find(arg)
			.limit(15)
			.sort('-lastChap.id')
			.select('name genres lastChap.name lastChap.id thumb lastChap.date _id slug lastChap.slug')
			.exec(function(err, post){
				if (err) {
					res.render('404.ejs',{err : err});
					
				}
				else {
					res.render('list.ejs',{post : post, number : 1, name : name, title: realName});
				}
			});
		});
	router_danhsach.route('/the-loai/:name/page/:num')
		.get(function(req, res){
			var name = req.params.name;
			var num = Number(req.params.num);
			var realName = reslug(name);
			var arg = {'genres' : realName}
			Post.find(arg)
			.skip((num -1)*15)
			.limit(15)
			.sort('-lastChap.id')
			.select('name genres lastChap.name lastChap.id thumb lastChap.date _id slug lastChap.slug')
			.exec(function(err, post){
				if (err) {
					res.render('404.ejs',{err : err});
					
				}
				else {
					res.render('list.ejs',{post : post, number : num, name : name, title: realName});
				}
			});
		});

	router_danhsach.route('/:name')
		.get(function(req, res){
			var name = req.params.name;
			var resultConvert = convert(name);
			Post.find(resultConvert.find)
			.limit(15)
			.sort(resultConvert.sort)
			.select('name genres lastChap.name lastChap.id thumb lastChap.date _id slug lastChap.slug')
			.exec(function(err, post){
				if (err) {
					res.render('404.ejs',{err : err});
					
				}
				else {
					res.render('list.ejs',{post : post, number : 1, name : name, title: resultConvert.realName});
				}
			});
		});
	router_danhsach.route('/:name/page/:num')
		.get(function(req, res){
			var name = req.params.name;
			var num = Number(req.params.num);
			var resultConvert = convert(name);
			Post.find(resultConvert.find)
			.skip((num -1)*15)
			.limit(15)
			.sort(resultConvert.sort)
			.select('name genres lastChap.name lastChap.id thumb lastChap.date _id slug lastChap.slug')
			.exec(function(err, post){
				if (err) {
					res.render('404.ejs',{err : err});
					
				}
				else {
					res.render('list.ejs',{post : post, number : num, name : name, title: resultConvert.realName});
				}
			});
		});

	

	return router_danhsach;
};
module.exports = router;
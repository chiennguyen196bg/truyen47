'use strict';
 
// require thư viện tương tác với mongo
 
var mongoose = require('mongoose');
 
// tạo cấu trúc bảng posts dùng hàm Schema&amp;nbsp;
 
var ChapSchema = mongoose.Schema({
	content: [String],
	name: String,
	slug: String,
	type: String
},{collection: 'chap'});
 
// export vào app với tên model là Post
 
module.exports = mongoose.model('Chap', ChapSchema);
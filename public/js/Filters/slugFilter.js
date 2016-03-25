app.filter('slug', function() {
	return function(x) {
	   	return getSlug(x);
	};
});
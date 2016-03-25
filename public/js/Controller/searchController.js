app.controller('searchController', function($scope, $http) { 
	
    var timeout = null;
    $scope.search = function(){
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            $http.get("/json/search/"+$scope.data)
    			.then(function(response) {
        			$scope.itemSearch = response.data;
    			});
        }, 500);
    };
});
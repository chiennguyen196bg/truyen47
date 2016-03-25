app.controller('postController', function($scope, $http) { 
	$http.get("/json/moi-update/20")
    .then(function(response) {
        $scope.postsUpdate = response.data;
        // $scope.statuscode = response.status;
       	// $scope.statustext = response.statustext;
    });

	$scope.clickUpdate = function(){
		$http.get("/json/moi-update/20")
    	.then(function(response) {
        	$scope.postsUpdate = response.data;
    	});
    };
	
	$scope.clickHot = function(){
		$http.get("/json/moi-update/12")
    	.then(function(response) {
        	$scope.postsHot = response.data;
    	});
	};

	$scope.clickNew = function(){
		$http.get("/json/moi-dang/20")
    	.then(function(response) {
        	$scope.postsNew = response.data;
    	});
	};
});
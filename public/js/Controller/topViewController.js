app.controller('topViewController', function($scope, $http) { 
	$http.get("/json/moi-update/5")
    .then(function(response) {
        $scope.itemTopTuan = response.data;
        // $scope.statuscode = response.status;
       	// $scope.statustext = response.statustext;
    });

	$scope.clickTopTuan = function(){
		$http.get("/json/moi-update/6")
    	.then(function(response) {
        	$scope.itemTopTuan = response.data;
    	});
    };
	
	$scope.clickTopThang = function(){
		$http.get("/json/moi-update/6")
    	.then(function(response) {
        	$scope.itemTopThang = response.data;
    	});
	};

});
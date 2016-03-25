app.controller('randomController', function($scope, $http) { 
	$http.get("/json/random")
    .then(function(response) {
        $scope.itemRandom = response.data;
        // $scope.statuscode = response.status;
       	// $scope.statustext = response.statustext;
    });

});
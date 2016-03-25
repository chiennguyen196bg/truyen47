app.controller('sideController', function($scope, $http) { 
	$http.get("/json/moi-update/10")
    .then(function(response) {
        $scope.itemSide = response.data;
        // $scope.statuscode = response.status;
       	// $scope.statustext = response.statustext;
    });

});
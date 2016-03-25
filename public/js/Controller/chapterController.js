app.controller('genresController', function($scope, $http) { 
	$http.get("/json/")
    .then(function(response) {
        $scope.itemGenres = response.data;
        // $scope.statuscode = response.status;
       	// $scope.statustext = response.statustext;
    });

});
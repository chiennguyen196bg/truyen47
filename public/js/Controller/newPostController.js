app.controller('newPostController', function($scope, $http) { 
	$http.get("/json/moi-dang/9",{ cache : true})
    .then(function(response) {
        $scope.itemNew = response.data;
        // $scope.statuscode = response.status;
       	// $scope.statustext = response.statustext;
    });

});
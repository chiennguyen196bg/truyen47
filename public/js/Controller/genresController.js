app.controller('genresController', function($scope, $http) { 
	$http.get("/json/get-all-genres", {cache : true})
    .then(function(response) {
        $scope.itemGenres = response.data;
        $scope.itemGenres = $scope.itemGenres.sort();
        var len = response.data.length;
        $scope.itemGenres1 = [];
        var temp = [];
        var k=0;
        for(var i = 0; i< len; i++){
        	temp[k] = $scope.itemGenres[i];
        	if(k == 2){
        		k = 0;
        		$scope.itemGenres1.push(temp);
        		temp = [];
        	} else{
        		k++;
        	}
        }
        if (temp.length != 0){
        	$scope.itemGenres1.push(temp);
        	temp = [];
        }
        // $scope.statuscode = response.status;
       	// $scope.statustext = response.statustext;
    });

});
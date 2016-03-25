app.controller("followListController", function($scope, $window, $http){
		if(!($window.localStorage.followedItems)){
			$window.localStorage.followedItems = "[]";
		}

		$scope.showFollowedList = function(){
			if($window.localStorage.followedItems != "[]"){
				var data = JSON.parse($window.localStorage.followedItems);
				$http.post("/json/follow", {data : data}, {cache: true})
					.then(function(response){
						$scope.followedList = response.data;
					});
			}
			else {
				$window.alert("Khong co gi trong danh sach");
			}
		};

		$scope.unfollow = function(slug){
			$window.alert(slug);
			$scope.tempList = JSON.parse($window.localStorage.followedItems);
			var index = $scope.tempList.indexOf(slug);
			if(index > -1){
				$scope.tempList.splice(index, 1);
				$window.localStorage.followedItems = JSON.stringify($scope.tempList);
			}
			for(var i = 0; i < $scope.followedList.length; i++){
				if ($scope.followedList[i].slug == slug){
					$scope.followedList.splice(i, 1);
					break;
				}
			}
		};
	});

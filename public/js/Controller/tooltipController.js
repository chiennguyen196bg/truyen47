// app.controller('tooltipController', function($scope) { 
// 	$scope.tooltip = function(){
// 		$('[data-toggle="tooltip"]').tooltip({html : true, placement: "right"});
// 	}

// });
app.controller("tooltipController",function($scope){})
.directive('toggle', function(){
  return {
    restrict: 'A',
    link: function(scope, element, attrs){
      if (attrs.toggle=="tooltip"){
        $(element).tooltip({html: true, placement: "right"});
      }
      if (attrs.toggle=="popover"){
        $(element).popover({html : true});
      }
    }
  };
})

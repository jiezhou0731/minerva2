

app.controller('dialogCtrl', function($scope, $mdDialog, $rootScope) {
	$scope.alert = '';

	$scope.$on('showDialog', function(event, args) {
		$scope.showDialog(args);
	},true);

	$scope.showDialog = function(event) {
		trackballControls.enabled = false;
		$mdDialog.show({
			controller: DialogController,
			templateUrl: 'app/view/spheres/docDetail.html',
			parent: angular.element(document.body),
			targetEvent: event,
			clickOutsideToClose:true
		});
	};

});

app.controller('MoviesCtrl', function ($scope,Movie,AppleEvent) {
    $scope.movies = AppleEvent.getList().$object;
});

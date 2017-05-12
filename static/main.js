var app = angular.module('myApp', [])

app.controller('main-controller', ['$scope', function($scope)
{
	$scope.submit = function()
	{
		if ($scope.frm.$valid)
		{
		    $scope.submitted = true;
		}
	};
	$scope.password = null;
  	$scope.passwordConfirmation = null;
  	//$("#country_selector").countrySelect({});
	$scope.EMAIL_REGEXP = /^\w+([.-]?\w+)@\w+([.-]?\w+)(.\w{2,3})+$/;
}]);




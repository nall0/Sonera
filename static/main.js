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

app.directive('passwordConfirm', ['$parse', function ($parse) {
 return {
    restrict: 'A',
    scope: {
      matchTarget: '=',
    },
    require: 'ngModel',
    link: function link(scope, elem, attrs, ctrl) {
      var validator = function (value) {
        ctrl.$setValidity('match', value === scope.matchTarget);
        return value;
      }
 
      ctrl.$parsers.unshift(validator);
      ctrl.$formatters.push(validator);
      
      // This is to force validator when the original password gets changed
      //scope.$watch('matchTarget', function(newval, oldval) {
        //validator(ctrl.$viewValue);
      //});

    }
  };
}]);


/*app.directive('checkEmail', function() {
	return {
	    restrict: 'A',
	    require: 'ngModel',
	    link: function(scope, elm, attrs, model) {
	    //change this:
			var EMAIL_REGEXP = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/;
			var emailValidator = function(value) {
			if (!value || EMAIL_REGEXP.test(value)) {
				model.$setValidity('email', true);
				return value;
			}
			else {
				model.$setValidity('email', false);
				return undefined;
			}
			model.$parsers.push(emailValidator);
			model.$formatters.push(emailValidator);
		}
	};
});*/




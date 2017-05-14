var app = angular.module('myApp', ['UserValidation']);

app.controller('myappCtrl', ['$scope', function($scope)
{
  $scope.formAllGood = function () {
      return ($scope.usernameGood && $scope.passwordGood && $scope.passwordCGood)
  }
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

angular.module('UserValidation', []).directive('validUsername', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (viewValue) {
                // Any way to read the results of a "required" angular validator here?
                var isBlank = viewValue === ''
                var invalidChars = !isBlank && !/^[A-z0-9]+$/.test(viewValue)
                var invalidLen = !isBlank && !invalidChars && (viewValue.length < 5 || viewValue.length > 20)
                ctrl.$setValidity('isBlank', !isBlank)
                ctrl.$setValidity('invalidChars', !invalidChars)
                ctrl.$setValidity('invalidLen', !invalidLen)
                scope.usernameGood = !isBlank && !invalidChars && !invalidLen

            })
        }
    }
});

app.directive('validPassword', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (viewValue) {
                var isBlank = viewValue === ''
                var invalidLen = !isBlank && (viewValue.length < 8 || viewValue.length > 20)
                var isWeak = !isBlank && !invalidLen && !/(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z])/.test(viewValue)
                ctrl.$setValidity('isBlank', !isBlank)
                ctrl.$setValidity('isWeak', !isWeak)
                ctrl.$setValidity('invalidLen', !invalidLen)
                scope.passwordGood = !isBlank && !isWeak && !invalidLen

            })
        }
    }
});

app.directive('validPasswordC', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (viewValue, $scope) {
                var isBlank = viewValue === ''
                var noMatch = viewValue != scope.myform.password.$viewValue
                ctrl.$setValidity('isBlank', !isBlank)
                ctrl.$setValidity('noMatch', !noMatch)
                scope.passwordCGood = !isBlank && !noMatch
            })
        }
    }
})


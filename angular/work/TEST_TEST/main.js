var app = angular.module('myApp', [])

app.controller('main-controller', ['$scope', function($scope)
{
	$scope.countries = [ 
    { 
        name: "Belgium",
        value: "belgium",
    }, 
    {
        name: "Croatia",
        value: "croatia",
    },
    {
        name: "Czech Republic",
        value: "cr",
    },
    {
        name: "Denmark",
        value: "denmark",
    }, 
    {
        name: "Estonia",
        value: "estonia",
    },
	{
        name: "Finland",
        value: "finland",
    },
	{ 
        name: "France",
        value: "france",
    }, 
    {
        name: "Georgia",
        value: "georgia",
    },
    {
        name: "Germany",
        value: "germany",
    },
    {
        name: "Ireland",
        value: "ireland",
    }, 
    {
        name: "Italy",
        value: "italy",
    },
	{ 
        name: "Luxembourg",
        value: "luxembourg",
    }, 
    {
        name: "Netherlands",
        value: "netherlands",
    },
    {
        name: "Poland",
        value: "poland",
    },
    {
        name: "Portugal",
        value: "portugal",
    }, 
    {
        name: "Spain",
        value: "spain",
    },
	{
		name: "United Kingdom",
		value: "uk",
	}
	];

	$scope.submitted = false;

	$scope.form = null;

	$scope.submit = function()
	{
		if ($scope.frm.$valid)
		{
		    $scope.submitted = true;
		}
	};
	
	$scope.checkAge = function()
	{
		if(Number.isInteger($scope.form.age)==true)
		{
			console.log("THE AGE IS A NUMBER : OK");
			required = "required";
		}
		else
		{
			console.log("THE AGE IS NOT A NUMBER : FUCK OFF BIATCH");
			required = "fuckyou"; 
		}
	};

	$scope.password = null;
  	$scope.passwordConfirmation = null;
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
		scope.$watch('matchTarget', function(newval, oldval) {
			validator(ctrl.$viewValue);
		});
    }
  };
}]);




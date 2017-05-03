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
	{
		name: "United State of America",
		value: "us",
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

}]);


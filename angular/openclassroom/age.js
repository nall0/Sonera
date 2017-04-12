var myApp = angular.module('myApp',[]);

myApp.controller("exemple1Ctrl", function($scope){
    $scope.age = 0;
    $scope.majeurOrMineurText = function(){
        return ($scope.age >= 18) ? "of age" : "underage";    
    };
});


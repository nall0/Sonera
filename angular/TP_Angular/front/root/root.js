angular.module('BlankApp').component('root', {
   templateUrl: 'root/root.html',
   controller: ['$scope', 'WebQuest', function($scope, WebQuest) {
     $scope.hello = function() {
       console.log("Hey my bro");
       WebQuest.call(); }
     $scope.title3 = "Click on me, I'm the directive";
   }]
})

//root.js gère le template root.js

//Declaration d'une application BlankApp
var myModule = angular.module('BlankApp', [])

.controller('MyController', ['$scope', 'WebQuest', function($scope, WebQuest) {
  	$scope.hello = function() { console.log("Hey my bro"); }
  	$scope.title1 = "Click on me my bro if you got balls";
	$scope.Search = function() {  WebQuest.searchSearch(); }
	$scope.title2 = "Click here to go on the HTML test page";
}])


.factory('WebQuest', ['$http', function($http) {
  return {
    searchSearch: function() {
      $http.get('http://localhost:3000/test')
      .then(res => {console.log('-->', res)});
    },
	display: function() {
		console.log("You asked for the test object page");
	} 
  }
}])

.filter('reverse', function() {
  return function(input, uppercase) {
	console.log("->", input);
    input = input || '';
    var out = '';
    for (var i = 0; i < input.length; i++) {
      out = input.charAt(i) + out;
    }
    // conditional based on optional argument
    if (uppercase) {
      out = out.toUpperCase();
    }
    return out;
  };
})
;	

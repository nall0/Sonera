/*Une dernière solution est d'utiliser dans le contrôleur l'événement viewContentLoaded,
 qui correspond à la fin du chargement du code des vues. Il faut paramétrer une fonction
 qui sera exécutée lorsque cet événement se produit avec la fonction $watch() :
*/

$scope.$watch('$viewContentLoaded', function(){
	// traitement à effectuer au chargement de la page
});


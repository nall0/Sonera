var express = require('express');
var app = express();


app.use(express.static('front')); //je me lie au dossier front et je vais chercher index
app.use('/lib', express.static('./node_modules')); //route de récupération des modules angular
app.use('/test', express.static('./front/test.json'));

app.listen(3000, function () {
  console.log('The server is listening on port 3000!');
})

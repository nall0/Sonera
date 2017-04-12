var express = require('express');
var app = express();

app.use(express.static('front')); //je me lie au dossier front
app.use('/lib', express.static('./node_modules')); //route de récupération des modules angular

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
})

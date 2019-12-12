var express = require('express');
var app = express();
port = process.env.PORT || 3000;
//init express

const routes = require('./routes/routes'); //importing route
routes(app); //register the route

app.listen(port, function () {
  console.log('Example app listening on port 3000!');
});
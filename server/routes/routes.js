'use strict';
module.exports = function(app) {
  const controllers = require('../controllers/controllers');

  // todoList Routes
  app.route('/')
    .get(controllers.init);

};



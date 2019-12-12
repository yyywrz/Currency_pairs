const mongoose = require('mongoose');
const model = new mongoose.Schema({});
const dataModel = mongoose.model('weatherByCity', model,'weatherByCity')

mongoose.connect('mongodb://127.0.0.1:27017/weatherDatabase',{ useNewUrlParser: true });

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log('database connected!')
});
mongoose.Promise = global.Promise;
module.exports = dataModel;
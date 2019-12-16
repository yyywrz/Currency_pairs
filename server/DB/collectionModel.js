const mongoose = require('mongoose');
const exchangeSchema = require('./currencySchema')
const model = new mongoose.Schema(exchangeSchema);
const dataModel = mongoose.model('weatherByCity', model,'weatherByCity')

mongoose.connect('mongodb://127.0.0.1:27017/currency_database',{ useNewUrlParser: true });

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log('database connected!')
});
mongoose.Promise = global.Promise;
module.exports = dataModel;
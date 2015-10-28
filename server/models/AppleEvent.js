var mongoose = require('mongoose');

// Create the AppleEventSchema.
var AppleEventSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  time: {
    type: String,
    required: true
  },
  address: {
    type: String,
    required: true
  },
  discription: {
    type: String,
    required: false
  },
  price: {
    type: Number,
    required: false
  },
  participants:{
	type: [],
    required: false
  }
});

// Export the model schema.
module.exports = AppleEventSchema;

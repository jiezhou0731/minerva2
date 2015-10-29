var mongoose = require('mongoose');

// Create the UserSchema.
var UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: false
  },
  firstName: {
    type: String,
    required: false
  },
  lastName: {
    type: String,
    required: false
  },
  password: {
    type: String,
    required: false
  }
});

// Export the model schema.
module.exports = UserSchema;

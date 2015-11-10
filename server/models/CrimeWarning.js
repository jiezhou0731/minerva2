var mongoose = require('mongoose');

var CrimeWarningSchema = new mongoose.Schema({
  title: {
    type: String,
    required: false
  },
  entity: {
    type: String,
    required: false
  },
  docs: {
    type: mongoose.Schema.Types.Mixed,
    required: false
  },
  duration: {
    type: String,
    required: false
  },
  time: {
    type: String,
    required: false,
    default: Date.now 
  },
  status:{
    type: String,
    required: false,
    default: "new" 
  }
});

// Export the model schema.
module.exports = CrimeWarningSchema;

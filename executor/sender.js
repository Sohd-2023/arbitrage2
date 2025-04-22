require('dotenv').config();
const { executeArbitrage } = require("./sender");

// Use environment variables for sensitive data
const PRIVATE_KEY = process.env.PRIVATE_KEY;

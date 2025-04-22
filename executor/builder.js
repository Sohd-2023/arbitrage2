require('dotenv').config();
const { ethers } = require("ethers");

module.exports = {
  buildTransaction: (opportunity) => {
    const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
    // Transaction building logic...
  }
}

const { ethers } = require("ethers");
const FlashLoanArbitrage = require("../artifacts/contracts/FlashLoanArbitrage.sol/FlashLoanArbitrage.json");
const config = require("../config.json");

// Setup provider and signer
const provider = new ethers.providers.JsonRpcProvider(config.rpcUrl);
const wallet = new ethers.Wallet(config.privateKey, provider);

// Contract setup
const arbitrageContract = new ethers.Contract(
  config.contractAddress,
  FlashLoanArbitrage.abi,
  wallet
);

async function executeArbitrage(opportunity) {
  try {
    // Convert amounts to wei
    const loanAmount = ethers.utils.parseUnits(
      opportunity.amount.toString(),
      6 // USDC has 6 decimals
    );
    
    const minProfit = ethers.utils.parseUnits(
      config.minProfit.toString(),
      6
    );

    // Determine router codes (0 = Uniswap, 1 = Sushiswap)
    const buyRouterCode = opportunity.buy_dex === "uniswap" ? 0 : 1;
    const sellRouterCode = opportunity.sell_dex === "uniswap" ? 0 : 1;

    // Build token path
    const [token0, token1] = opportunity.pair.split("-");
    const path = [
      config.tokens[token0],
      config.tokens[token1],
      config.tokens["USDC"] // Always end with USDC to repay loan
    ];

    console.log(`Executing arbitrage with ${opportunity.amount} USDC`);

    // Send transaction
    const tx = await arbitrageContract.initiateArbitrage(
      loanAmount,
      buyRouterCode,
      sellRouterCode,
      path,
      minProfit,
      { gasLimit: 500000 }
    );

    const receipt = await tx.wait();
    console.log(`Transaction mined: ${receipt.transactionHash}`);
    
    return {
      success: true,
      txHash: receipt.transactionHash
    };
  } catch (error) {
    console.error("Execution failed:", error);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = { executeArbitrage };

const { executeArbitrage } = require("./executor/sender");
const { monitorPrices } = require("./searcher/monitor");
const config = require("./config.json");

// Main execution loop
async function main() {
  console.log("Starting arbitrage bot...");
  
  // Start price monitoring
  const opportunities = await monitorPrices();
  
  // Process each opportunity
  opportunities.subscribe(async (opp) => {
    if (opp.profit > config.minProfit) {
      console.log(`Found profitable opportunity: ${opp.profit} USD`);
      const result = await executeArbitrage(opp);
      
      if (result.success) {
        console.log(`Arbitrage executed successfully: ${result.txHash}`);
      } else {
        console.error(`Failed to execute: ${result.error}`);
      }
    }
  });
}

main().catch(console.error);

import asyncio
from web3 import Web3
import json
import time

# Configuration
CONFIG = {
    "rpc_url": "https://mainnet.infura.io/v3/YOUR_INFURA_KEY",
    "dexes": {
        "uniswap": {
            "router": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "factory": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
        },
        "sushiswap": {
            "router": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
            "factory": "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
        }
    },
    "tokens": {
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    },
    "polling_interval": 5  # seconds
}

class ArbitrageSearcher:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(CONFIG['rpc_url']))
        self.opportunities = []
        
        # Load ABIs
        with open('abis/erc20.json') as f:
            self.erc20_abi = json.load(f)
        with open('abis/uniswap_router.json') as f:
            self.router_abi = json.load(f)
            
        # Initialize contracts
        self.dex_routers = {
            name: self.w3.eth.contract(
                address=Web3.toChecksumAddress(dex['router']),
                abi=self.router_abi
            )
            for name, dex in CONFIG['dexes'].items()
        }
        
    async def monitor_prices(self):
        """Continuously monitor DEX prices"""
        while True:
            try:
                # Check all token pairs
                for pair in [("USDC", "WETH"), ("WETH", "DAI"), ("DAI", "USDC")]:
                    token0, token1 = pair
                    prices = await self.get_prices(token0, token1)
                    
                    # Find arbitrage between DEXs
                    for dex1, price1 in prices.items():
                        for dex2, price2 in prices.items():
                            if dex1 == dex2:
                                continue
                                
                            # Calculate potential profit
                            profit = self.calculate_profit(
                                token0, token1,
                                dex1, price1,
                                dex2, price2
                            )
                            
                            if profit > 0:
                                self.opportunities.append({
                                    "pair": f"{token0}-{token1}",
                                    "buy_dex": dex1,
                                    "sell_dex": dex2,
                                    "profit": profit,
                                    "timestamp": int(time.time())
                                })
                                print(f"Found opportunity: {profit} USD profit")
                
                await asyncio.sleep(CONFIG['polling_interval'])
                
            except Exception as e:
                print(f"Error in monitoring: {e}")
                await asyncio.sleep(10)

    async def get_prices(self, token_in, token_out):
        """Get prices across all DEXs for a token pair"""
        prices = {}
        amount_in = self.w3.toWei(1, 'ether')  # 1 ETH worth
        
        for dex_name, router in self.dex_routers.items():
            try:
                path = [
                    Web3.toChecksumAddress(CONFIG['tokens'][token_in]),
                    Web3.toChecksumAddress(CONFIG['tokens'][token_out])
                ]
                amounts = router.functions.getAmountsOut(amount_in, path).call()
                price = amounts[-1] / 10**18  # Convert to ETH
                prices[dex_name] = price
            except Exception as e:
                print(f"Error getting price from {dex_name}: {e}")
                
        return prices

    def calculate_profit(self, token0, token1, dex1, price1, dex2, price2):
        """Calculate potential arbitrage profit"""
        # Simplified calculation - in reality you'd account for:
        # - Exchange fees
        # - Gas costs
        # - Slippage
        return abs(price2 - price1) * 10000  # Example scaling

if __name__ == "__main__":
    searcher = ArbitrageSearcher()
    asyncio.run(searcher.monitor_prices())

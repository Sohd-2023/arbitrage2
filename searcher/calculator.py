def calculate_profit(amount_in, price_in, price_out, fees):
    """
    Calculate net profit after fees
    :param amount_in: Input amount (in wei)
    :param price_in: Buy price per token
    :param price_out: Sell price per token
    :param fees: Dictionary of {fee_type: amount}
    :return: net_profit (in USD)
    """
    gross_profit = (price_out - price_in) * amount_in
    total_fees = sum(fees.values())
    return gross_profit - total_fees

def adjust_for_slippage(amount, slippage_percent):
    """Reduce amount by slippage percentage"""
    return amount * (1 - slippage_percent / 100)

def estimate_gas_costs(tx_complexity

                      from decimal import Decimal

class ArbitrageCalculator:
    def __init__(self):
        self.aave_fee = Decimal('0.0009')  # 0.09%
        self.slippage_tolerance = Decimal('0.005')  # 0.5%

    def calculate_net_profit(self, buy_price, sell_price, amount):
        gross_profit = (sell_price - buy_price) * amount
        fees = self._calculate_fees(amount)
        return gross_profit - fees

    def _calculate_fees(self, amount):
        return (
            amount * self.aave_fee +
            amount * self.slippage_tolerance +
            self._estimate_gas_cost()
        )

    def _estimate_gas_cost(self):
        # Current mainnet average gas price
        return Decimal('0.05')  # $0.05 equivalent 

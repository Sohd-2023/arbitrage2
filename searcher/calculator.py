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

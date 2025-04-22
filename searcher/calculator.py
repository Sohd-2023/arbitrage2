def calculate_net_profit(gross_profit, fees):
    """Enhanced profit calculation"""
    total_fees = sum(fees.values())
    return gross_profit - total_fees

def adjust_for_slippage(amount, slippage_percent):
    return amount * (1 - slippage_percent/100)

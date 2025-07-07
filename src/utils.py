def get_balance(upbit, ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            return float(b['balance'])
    return 0
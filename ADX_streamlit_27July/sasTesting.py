# from alphatrade import AlphaTrade
# import config
# import pyotp
# from tradeAPI import Trade
# Totp = config.TOTP
# pin = pyotp.TOTP(Totp).now()
# totp = f"{int(pin):06d}" if len(pin) <= 5 else pin
# print(totp)
# sas = AlphaTrade(login_id=config.login_id, password=config.password,twofa=totp, access_token=config.access_token, master_contracts_to_download=['MCX', 'NFO','NSE','BSE','CDS'])
# print(sas.get_profile())
# print(sas.get_holding_positions())
# sas.get_holding_positions()
# sas.orders()
# print(sas.get_balance())
# usd_inr = sas.get_instrument_by_symbol('NSE', 'ONGC')
# print(usd_inr)


from tradeAPI import Trade


stock = 'ONGC'
def main():
    trade_instance = Trade(stock)
    response = trade_instance.sellShare()
    print(response)  # You can do something with the response

if __name__ == '__main__':
    main()


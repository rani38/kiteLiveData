from alphatrade import AlphaTrade,TransactionType,OrderType,ProductType
import config
import pyotp

Totp = config.TOTP
pin = pyotp.TOTP(Totp).now()
totp = f"{int(pin):06d}" if len(pin) <= 5 else pin
print(totp)
sas = AlphaTrade(login_id=config.login_id, password=config.password,twofa=totp, access_token=config.access_token, master_contracts_to_download=['MCX', 'NFO','NSE','BSE'])

class Trade:
    def __init__(self,stock):
        self.INSTRUMENT = sas.get_instrument_by_symbol('NSE', stock)


    def sellShare(self):
        # sell api
        # Get the opposite instrument (in this example, assuming you bought TATASTEEL earlier)

        # Place a sell order to close the position
        sell_order_response = sas.place_order(
            transaction_type=TransactionType.Sell,
            instrument=self.INSTRUMENT,
            quantity=1,
            order_type=OrderType.Market,
            product_type=ProductType.Intraday,
            price=0.0,
            trigger_price=175.6,
            stop_loss=None,
            square_off=None,
            trailing_sl=None,
            is_amo=False
        )
        return sell_order_response

    def buyShare(self):
        # buy shre api
        buy_response = sas.place_order(transaction_type=TransactionType.Buy,
                                   instrument=self.INSTRUMENT,
                                   quantity=1,
                                   order_type=OrderType.Market,
                                   product_type=ProductType.Intraday,
                                   price=0.0,
                                   order_side="BUY",
                                   trigger_price=175.6,
                                   stop_loss=None,
                                   square_off=None,
                                   trailing_sl=None,
                                   is_amo=False)
        return buy_response



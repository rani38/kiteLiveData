import logging
from kiteconnect import KiteConnect,KiteTicker
import os
import mysql.connector
import webbrowser
logging.basicConfig(level=logging.DEBUG)
from dotenv import load_dotenv
from datetime import datetime,timedelta
import json
load_dotenv()

class KiteInitializer:
    ACCESS_TOKEN = None
    kite = KiteConnect(api_key=os.getenv("API_KEY"))
    login_url = kite.login_url()
    @staticmethod
    def _get_cache_token():
        f = open("token.json")
        data = json.load(f)
        access_token, login_time = data["access_token"], data["login_time"]
        # extracting next date  and prev_date
        next_day = datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
        prev_day = datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S")
        # till 6AM of today and 6AM of next
        till_6AM = next_day.replace(hour=6, minute=0, second=0)
        from_6AM = prev_day.replace(hour=6, minute=0, second=0)
        # acees_token usage time
        current_time = datetime.now()
        # if current_time is within range or not
        if current_time <= till_6AM and current_time >= from_6AM:
            return True
        else:
            print("Token is Expired. Generating New Token......")
            return False
    @staticmethod
    def _get_access_token():
        try:
            if KiteInitializer._get_cache_token():
                token_data = json.loads(open("token.json").read())
                access_token = token_data["access_token"]
                print(token_data)
                KiteInitializer.ACCESS_TOKEN = access_token
            else:
                webbrowser.open(KiteInitializer.login_url)
                request_token = input("Enter the request token: ")
                data = KiteInitializer.kite.generate_session(request_token, api_secret=os.getenv("API_SECRET"))
                print(f"This is data from: {data}")
                KiteInitializer.ACCESS_TOKEN = data["access_token"]
                login_time = datetime.now()
                token_data = {"access_token": data["access_token"],"login_time": login_time}
                print(token_data)
                with open("token.json", "w") as file:
                    json.dump(token_data, file)
        except Exception as e:
            logging.error(f"Error in generating Token: {e}")


class KiteLiveFeed(KiteInitializer):
    __access__ = KiteInitializer._get_access_token()
    kws = KiteTicker(os.getenv("API_KEY"), KiteInitializer.ACCESS_TOKEN)
    def _insert_feedToDB(self,ticks):
        print(ticks)
        last_trade_time = ticks[0]['exchange_timestamp']
        instrument_token = ticks[0]['instrument_token']
        last_price = ticks[0]['last_price']

        ohlc_data = [
            (instrument_token, last_price, str(last_trade_time))
        ]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(current_time, last_trade_time)
        query = """
            INSERT INTO ohlc (instrument_token, last_price, last_traded_time)
            VALUES (%s,%s,%s);
            """
        if self.conn.is_connected():
            # sleep for some time
            # time.sleep(1)
            # Execute the query for each set of data
            self.cursor.execute(query, ohlc_data[0])
            self.conn.commit()
            print("executed the insert query")
        else:
            self._dbConnect()
            self.cursor.execute(query, ohlc_data[0])
            self.conn.commit()
            print("executed the insert query")

    def _on_ticks(self,ws, ticks):
        print(ticks)
        # extracting values of ohlc , last_price , token and time
        self._insert_feedToDB(ticks)
    def _on_connect(self,ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        ws.subscribe([256265])

        # Set RELIANCE to tick in `full` mode.
        ws.set_mode(ws.MODE_FULL, [256265])

    def _on_close(self,ws, code, reason):
        # On connection close stop the main loop
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()
    def run(self,**kwargs):
        self.DB_INFO = kwargs
        self._dbConnect()
        self.kws.on_ticks = self._on_ticks
        self.kws.on_connect = self._on_connect
        self.kws.on_close = self._on_close
        self.kws.connect()

    def _dbConnect(self):
        try:
            kwargs = self.DB_INFO
            print(kwargs)
            conn = mysql.connector.connect(host=kwargs["HOST"], user=kwargs["USER"], passwd=os.getenv("DB_PASSWORD"), db=kwargs["DATABASE"])
            cursor = conn.cursor()
            if conn.is_connected():
                print("Successfully Connected to the database")
                self.conn,self.cursor = conn,cursor
        except Exception as e:
            raise e


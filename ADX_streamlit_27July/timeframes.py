from mysql_connection import connection
class TimeFrames:
    def __init__(self,timeframe):
        self.timeframe = timeframe
    def last_n_prices(self):
        conn, cur = connection()
        query = f'''SELECT ROUND(last_price, 2) AS rounded_last_price,last_traded_time FROM ohlc ORDER BY last_traded_time DESC LIMIT {self.timeframe};'''
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    def create_n_sec_data(self,last_n_data: list,datetime:float) -> tuple:
        open_price = last_n_data[-1]
        high = max(last_n_data)
        low = min(last_n_data)
        close = last_n_data[0]
        return open_price,high, low,close,datetime

    def insert_feed(self,**kwargs):
        conn, cur = connection()
        rows = self.last_n_prices()
        print(rows)
        last_n_data = [row[0] for row in rows]
        datetime = rows[0][1]
        data = self.create_n_sec_data(last_n_data,datetime)
        query = """INSERT INTO 5sec_ohlc(open,high,low,close,datetime) 
                    VALUES(%s, %s, %s, %s, %s)"""
        cur.execute(query, data)
        conn.commit()


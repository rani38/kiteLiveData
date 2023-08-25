import mysql.connector
from datetime import datetime
import numpy as np

host = "localhost"
username = "root"
db = "test"
DB_PASSWORD = ""

def get_data(limit):
    '''BEFORE STREAMING ADX VALUE WE NEED TO GET THE FIRST 14 DATA
    SO WE WILL GET THE FIRST 14 DATA ie: starts at 9:15 and wait till 1:10 mins to fill 14 data(We are assuming the data is coming in every 5 seconds so considering that only.
    In future we will optimize it for each cases'''
    '''
    Code to get first 14 data from a table
    return first 14'''

    conn = mysql.connector.connect(host=host, user=username, passwd=DB_PASSWORD, db=db)
    cursor = conn.cursor()
    query = f"""(SELECT * FROM 5sec_ohlc ORDER BY datetime DESC LIMIT {limit})
            ORDER BY datetime ASC;"""
    # query = f"""(SELECT * FROM caldata ORDER BY timestamp DESC LIMIT {limit})
    #         ORDER BY timestamp ASC;"""
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    print("get_data returned rows",rows)
    return rows

def get_live_data():
    '''Here we will write the code to get live data in 5 seconds interval it can be through web socket or from database'''
    while True:
        row = get_data(1)
        print(row)
        high = row[0][1]
        low = row[0][2]
        close = row[0][3]
        datetime = row[0][-1]
        print("get_live_data returned high,low,close",high,low,close,datetime)
        yield high,low,close,datetime

def get_first_14_data():
    rows =  get_data(14)
    highs = [row[1] for row in rows]
    lows = [row[2] for row in rows]
    closes = [row[3] for row in rows]
    # datetime is remaining
    # datetime = rows[0][-1]
    print("get_first_14_data returned,highs,lows,closes",highs,lows,closes)
    return highs,lows,closes



def insert_firs14(highs,lows,closes,adxs,plus_DIs,minus_DIs):
    conn = mysql.connector.connect(host=host, user=username, passwd=DB_PASSWORD, db=db)
    cursor = conn.cursor()
    query = """INSERT INTO adxdis (high,low,close,ADX,DI_plus,DI_minus,datetime) VALUES(%s,%s,%s,%s,%s,%s,%s);"""
    current_time = datetime.now()

    for i in range(len(highs)):
        high = highs[i]
        low = lows[i]
        close = closes[i]
        adx = adxs[i]
        plus_DI = plus_DIs[i]
        minus_DI = minus_DIs[i]

        # Insert the current row into the table.
        cursor.execute(query, (high, low, close, adx, plus_DI, minus_DI, current_time))

    conn.commit()
    cursor.close()
    conn.close()
    print("insert_firs14 a successfully inserted string message")
    return "first14 inserted"

def insert_next(highs, lows, closes, adxs, plus_DIs, minus_DIs,current_time):
    conn = mysql.connector.connect(host=host, user=username, passwd=DB_PASSWORD, db=db)
    cursor = conn.cursor()
    query = """INSERT INTO adxdis (high, low, close, ADX, DI_plus, DI_minus, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    adxs[-1] = float(adxs[-1] if not np.isnan(adxs[-1]) else 0)
    plus_DIs[-1] = float(plus_DIs[-1] if not np.isnan(plus_DIs[-1]) else 0)
    minus_DIs[-1] = float(minus_DIs[-1] if not np.isnan(minus_DIs[-1]) else 0)
    print("control ", (float(highs[-1]), float(lows[-1]), float(closes[-1]), float(adxs[-1]), float(plus_DIs[-1]), float(minus_DIs[-1])))
    cursor.execute(query, (float(highs[-1]), float(lows[-1]), float(closes[-1]), float(adxs[-1]), float(plus_DIs[-1]), float(minus_DIs[-1]),current_time))
    conn.commit()
    cursor.close()
    conn.close()
    print("insert_next successfully inserted the data")
    print("inserted nexts")
    return "inserted next"

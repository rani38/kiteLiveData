from datetime import datetime
import pandas as pd
from mysql_connection import connection

current_time = datetime.now()
starttime = "2023-08-01 9:15:00"
endtime = "2023-08-30 16:15:00"
starttime = datetime.strptime(starttime,"%Y-%m-%d %H:%M:%S")
endtime = datetime.strptime(endtime,"%Y-%m-%d %H:%M:%S")
conn,cur = connection()
closes = []
margin = 0

# Create an empty DataFrame with columns
columns = ["Trade", "Type", "Date", "Price", "cum_profit", "profit"]
data_frame = pd.DataFrame(columns=columns)

def insert_into_dataframe(data):
    try:
        global data_frame
        df1 = pd.DataFrame(data,index=[0])
        data_frame = pd.concat([data_frame,df1])
    except Exception as e:
        print(e)


def setOffset(offset):
    adx = []
    plusDI = []
    minusDI = []
    timeframe = []

    query = f"SELECT * FROM adxdis LIMIT 3 OFFSET {offset};"
    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:

        adx.append(row[4])
        plusDI.append((row[5]))
        minusDI.append(row[6])
        timeframe.append(row[-1])
        closes.append(row[3])
    # closes.append(rows[0][2])
    first_close = rows[0][3]
    # last close would be
    last_close = rows[-1][3]
    # first timeframe
    first_timeframe = rows[0][-1]
    # last timeframe i.e, time at which the last close was saved
    last_timeframe = rows[-1][-1]
    return  adx,plusDI,minusDI,timeframe,closes,first_close,last_timeframe


def process_trade():
    LE = False
    SE = False
    offset = 27
    count = 1
    total = 0
    while True:
        offset += 1
        # we will get all the data i.e, adx,plusDI...close,.. timeframe etc from setOffest function
        adx,plusDI,minusDI,timeframe,close_price,first_close,last_timeframe = setOffset(offset)
        try :
            if current_time >= starttime and current_time <= endtime:
                # Entry conditions
                if adx[0] > 20 and adx[0]<35 and adx[2] > adx[1] and adx[1] > adx[0]:
                    if plusDI[2] > minusDI[2] and not LE:
                        print("Long Entry",adx[0],plusDI[0],minusDI[0],timeframe[0])
                        LE = True
                        long_entry_close = close_price[-1]
                        print(long_entry_close,"at",last_timeframe)
                        print(f"current_time is{datetime.now()}")
                        # append the data into the dataframe
                        data = {"Trade":count,"Type":"LE","Date":last_timeframe,"Price":close_price[-1],"cum_profit":"-","profit":"-"}
                        insert_into_dataframe(data)

                    if minusDI[2] > plusDI[2] and not SE:
                        print("Short Entry",adx[0],plusDI[0],minusDI[0],timeframe[0])
                        SE = True
                        short_entry_close = close_price[-1]
                        print(short_entry_close,"at",last_timeframe)
                        print(f"current_time is{datetime.now()}")
                        # append the data into the dataframe
                        data = {"Trade": count, "Type": "SE", "Date": last_timeframe, "Price": close_price[-1],"cum_profit":"-","profit":"-"}
                        insert_into_dataframe(data)
                # Exit conditions
                if adx[1]>adx[2] and adx[1]<adx[0]:
                    if LE and long_entry_close:
                        print("Long Exit",adx[2],plusDI[2],minusDI[2],timeframe[2])
                        LE = False
                        long_exit_close = close_price[-1]
                        print(long_exit_close)
                        margin = long_exit_close-long_entry_close
                        print(f"margin is {margin} with entry at {long_entry_close} and exit at {long_exit_close}")
                        print(f"current_time is{datetime.now()}")
                        print("trade no.",count)
                        # adding margin to the total
                        total += margin
                        # append the data into the dataframe
                        data = {"Trade": "", "Type": "LX", "Date": last_timeframe, "Price": close_price[-1],"cum_profit":margin,"profit":total}
                        insert_into_dataframe(data)
                        count += 1
                        close_price.clear()
                        print("**********long exit**********")

                    if SE and short_entry_close:
                        print("Short Exit",adx[2],plusDI[2],minusDI[2],timeframe[2])
                        SE = False
                        short_exit_close = close_price[-1]
                        print(short_exit_close)
                        margin =  short_entry_close - short_exit_close
                        print(f"margin is {margin} with entry at {short_entry_close} and exit at {short_exit_close}")
                        print(f"current_time is{datetime.now()}")
                        print("trade no.",count)
                        # adding margin to the total
                        total += margin
                        # append the data into the dataframe
                        data = {"Trade": "", "Type": "SX", "Date": last_timeframe, "Price": close_price[-1],"cum_profit":margin,"profit":total}
                        insert_into_dataframe(data)
                        count += 1
                        close_price.clear()
                        print("**********short exit**********")

        except:
            print(total)
            print(data_frame.to_csv("myscript_trades.csv"))
            break

if __name__ == "__main__":
    process_trade()
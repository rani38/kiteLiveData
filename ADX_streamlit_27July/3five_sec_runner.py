from n_sec_REALTIME_stream_DATA import get_first_14_data ,get_data,get_live_data,insert_firs14,insert_next
import talib as ta
import pandas as pd
import numpy as np
import pandas as pd
import time
from datetime import datetime

highs,lows,closes = get_first_14_data()
adxs = [0 for i in range(len(highs))]
plus_DIs = [0 for i in range(len(highs))]
minus_DIs = [0 for i in range(len(highs))]

if len(highs) <= 14:
    insert_firs14(highs,lows,closes,adxs,plus_DIs,minus_DIs)

for data in get_live_data():
    high_value, low_value, close_value = data
    # popping the 1st values to make the lenght of OHLC 14
    # highs.pop(0)
    # lows.pop(0)
    # closes.pop(0)

    #convert list to array with updated open,high,low,close
    highs.append(float(high_value))
    highP = np.array(highs)
    closes.append(float(close_value))
    closeP = np.array(closes)
    lows.append(float(low_value))
    lowP = np.array(lows)
    adx = ta.ADX(highP, lowP, closeP, timeperiod=14)
    plus_di = ta.PLUS_DI(highP,lowP,closeP,timeperiod=14)
    minus_di = ta.MINUS_DI(highP,lowP,closeP, timeperiod=14)
    adx_value,plus_di_value,minus_di_value = adx[-1],plus_di[-1],minus_di[-1]  # Get the last ADX value
    # Store the ADX value
    print(plus_di,minus_di,adx)
    adxs.append(adx_value)
    plus_DIs.append(plus_di_value)
    minus_DIs.append(minus_di_value)
    current_time = datetime.now()
    # insert_firs14(highs, lows, closes, adxs, plus_DIs, minus_DIs)  # Call the function here after updating the lists
    insert_next(highs, lows, closes, adxs, plus_DIs, minus_DIs,current_time)
    print("high",highs)
    print("lows",lows)
    print("closes",closes)
    print("ADXs",adxs)
    print("plus_DIs",plus_DIs)
    print("minus_DIS",minus_DIs)
    print(f"Calculated ADX is: {adx_value}")
    print(f"Calculated adx is : {adx[-1]}")
    time.sleep(60)

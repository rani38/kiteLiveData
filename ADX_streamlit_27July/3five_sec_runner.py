from n_sec_REALTIME_stream_DATA import get_first_14_data ,get_data,get_live_data,insert_firs14,insert_next
import talib as ta
import numpy as np
import os
import time

# n seconds
time_frame = os.getenv("time_frame")


highs,lows,closes = get_first_14_data()
adxs = [0 for i in range(len(highs))]
plus_DIs = [0 for i in range(len(highs))]
minus_DIs = [0 for i in range(len(highs))]

if len(highs) <= 14:
    insert_firs14(highs,lows,closes,adxs,plus_DIs,minus_DIs)

for data in get_live_data():
    high_value, low_value, close_value,datetime = data

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
    adxs.append(adx_value)
    plus_DIs.append(plus_di_value)
    minus_DIs.append(minus_di_value)
    current_time = datetime
    # insert_firs14(highs, lows, closes, adxs, plus_DIs, minus_DIs)  # Call the function here after updating the lists
    insert_next(highs, lows, closes, adxs, plus_DIs, minus_DIs,current_time)
    print("high",highs)
    print("lows",lows)
    print("closes",closes)
    print("ADXs",adxs)
    print("plus_DIs",plus_DIs)
    print("minus_DIS",minus_DIs)
    print(f"Calculated adx is : {adx[-1]}")
    time.sleep(5)

from timeframes import TimeFrames
import time
from datetime import datetime,timedelta
while True:
    # wait till it gets 0 seconds for any minute
    now = datetime.now()
    next_min = now + timedelta(minutes=1)
    next_min = next_min.replace(second=0, microsecond=0)
    diff = next_min - now
    sec = int(diff.total_seconds())
    time.sleep(sec)
    print(datetime.now())
    instance = TimeFrames(60)
    instance.insert_feed()
    time.sleep(60)


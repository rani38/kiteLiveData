from livefeed import  KiteLiveFeed
from datetime import datetime,timedelta
import time

instance = KiteLiveFeed()
DATABASE = {
    "HOST": "localhost",
    "USER": "root",
    "DATABASE": 'test'
}


# wait till it gets 0 seconds for any minute
now = datetime.now()
next_min = now + timedelta(minutes=1)
next_min = next_min.replace(second=0, microsecond=0)
diff =  next_min - now
sec = int(diff.total_seconds())
time.sleep(sec+2)
instance.run(**DATABASE)



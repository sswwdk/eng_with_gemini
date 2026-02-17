from datetime import datetime
import pytz

try:
    tz = pytz.timezone('Australia/Melbourne')
    today_str = datetime.now(tz).strftime("%Y-%m-%d")
    print(f"Success! Current date in Melbourne: {today_str}")
except Exception as e:
    print(f"Error: {e}")

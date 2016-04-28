from datetime import datetime
import json
import svm
import pandas as pd
import datetime
import calendar
from flask import jsonify

data = []
predicted_data = svm.svm_predict(30, 0, 'AAPL')
for x in predicted_data:
    data.append(round(x,3))

utc = []

today = datetime.date.today()
thirtyday = datetime.timedelta(days=30)

daterange = pd.date_range(today, today + thirtyday)
for single_date in daterange:
    utc.append(calendar.timegm(single_date.timetuple()))

json_data =([[x, y] for x in utc for y in data])
print json_data

json.dumps(json_data)
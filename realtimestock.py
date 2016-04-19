import sqlite3 as lite
import datetime
from yahoo_finance import Share
import time as T

# find the date of yesterday
now = datetime.datetime.now()

# connect the sqlite
conn = lite.connect('StockHistory.db')
cursor = conn.cursor()
# every time empty data
cursor.execute('DELETE FROM TrueTimeValue')
conn.commit()
# get the records ranging from max date in DB to yesterday
BeginTime = now.replace(hour=9, minute=0, second=0, microsecond=0)
EndTime = now.replace(hour=16, minute=0, second=0, microsecond=0)
# LocalTime = T.strftime('%Y-%m-%d ',T.localtime(T.time()))
while now > BeginTime and now < EndTime:
    StockList = ['YHOO', 'GOOG', 'AAPL', 'TWTR', 'AMZN']
    for stock in StockList:
        Symbol = stock
        Company = Share(stock)
        Price = Company.get_price()
        Time = Company.get_trade_datetime()
        Volume = Company.get_volume()
        purchases = (Symbol, Price, Time, Volume)
        cursor.execute('INSERT INTO TrueTimeValue VALUES (?,?,?,?)', purchases)
        conn.commit()
        Company.refresh()
    cursor.execute('SELECT * FROM TrueTimeValue')
    print(cursor.fetchall())
    T.sleep(60)
cursor.close()
conn.close()

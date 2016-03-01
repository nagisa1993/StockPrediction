import sqlite3 as lite
import sys
import datetime 
from yahoo_finance import Share

################# find the date of yesterday
today = datetime.date.today()
oneday = datetime.timedelta(days=1)
yesterday = today - oneday
##################connect the sqlite
conn = lite.connect('StockHistory.db')
cursor = conn.cursor()

# ################## find the max date of the records in DB
cursor.execute('SELECT MAX(TadeTime) from HistoryValue')
# # cursor.execute('SELECT * from HistoryValue')
datelist = cursor.fetchall()
BeginDate = str(datelist[0]) 
BeginDate = BeginDate[3:13]
# # BeginDate = datetime.datetime.strptime(BeginDate, "%Y-%m-%d").date()

############### get the records ranging from max date in DB to yesterday
StockList = ['YHOO','GOOG','AAPL','TWTR','AMZN']
for stock in StockList:
	Company = Share(stock)
	stockarray = Company.get_historical(BeginDate, str(yesterday))
	#cursor.execute('delete from HistoryValue')
	stock_tuple = []
	for i in stockarray:
		dic = i
		Symbol = dic["Symbol"]
		Volume = int(dic["Volume"])
		TadeTime = dic["Date"]
		OpenPrice = float(dic["Open"])
		ClosePrice = float(dic["Close"])
		HighPrice = float(dic["High"])
		LowPrice = float(dic["Low"])
		purchases = (Symbol, TadeTime, OpenPrice, ClosePrice, HighPrice,LowPrice,Volume)
		stock_tuple.append(purchases)
	# print stock_tuple
	cursor.executemany('INSERT INTO HistoryValue VALUES (?,?,?,?,?,?,?)', stock_tuple)
# cursor.execute('drop table HistoryValue')
# cursor.execute('create table HistoryValue (Symbol varchar(20), TadeTime date, OpenPrice float, HighPrice float, LowPrice float, ClosePrice float, Volume int)')
# cursor.execute('create table TrueTimeValue (Symbol varchar(20), TradePrice float, TadeTime date, Volume int)')
# print "Opened database successfully";
# cursor.execute('select * from HistoryValue')
# print(cursor.fetchall())
conn.commit()
cursor.close()
conn.close()
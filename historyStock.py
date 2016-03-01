import sqlite3 as lite
from yahoo_finance import Share
yahoo = Share('YHOO')
print yahoo.get_open()
print yahoo.get_price()
stockarray = yahoo.get_historical('2016-02-26', '2016-02-28')
#print (type(yahoo.get_historical('2014-04-25', '2014-04-29')))
#print(type(stockarray))
conn = lite.connect('StockHistory.db')
cursor = conn.cursor()

for i in stockarray:
	dic = stockarray[0]
	StockID = dic["Symbol"]
	Volume = int(dic["Volume"])
	FullName = ""
	TadeTime = dic["Date"]
	OpenPrice = dic["Open"]
	ClosePrice = dic["Close"]
	HighPrice = dic["High"]
	LowPrice = dic["Low"]
	cursor.execute('insert into user (ID, Symbol,TradeTime,OpenPrice,ClosePrice,HighPrice,LowPrice ) values ('+1+ StockID +'')

#print(type(stockarray[0]))

#print(type(int(dic["Volume"])))

#cursor.execute('drop table TrueTimeValue')

cursor.execute('create table HistoryValue (ID INT PRIMARY KEY NOT NULL, Symbol varchar(20), TadeTime date, OpenPrice float, HighPrice float, LowPrice float, ClosePrice float, Volume int)')
cursor.execute('create table TrueTimeValue (ID INT PRIMARY KEY NOT NULL, Symbol varchar(20), TradePrice float, TadeTime date, Volume int)')
print "Opened database successfully";
cursor.close()
conn.close()

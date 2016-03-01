import sqlite3 as lite
from yahoo_finance import Share
yahoo = Share('YHOO')
print yahoo.get_open()
print yahoo.get_price()
StockArray = yahoo.get_historical('2016-02-24', '2016-02-28')
conn = lite.connect('stockHistory.db')
cursor = conn.cursor()

# creat HistoryPrice table, only needed for the first time
# cursor.execute("create table HistoryPrice (Adj_Close real, Close real, Date integer, High real, Low real, Open real, Symbol text, Volume integer)")

# turn [{}] into [()]
# print StockArray
stocktuple = []
for i in StockArray:
	stocktuple.append((tuple(i.values())))
# print StockArray
# print stocktuple
stocktuple2=[(3, 4, 5 ,6 ,7 ,7 ,8,8)]
cursor.execute("insert into HistoryPrice values (?, ?, ?, ?, ?, ?, ?, ?)", stocktuple2)

cursor.executemany("insert into HistoryPrice values (?, ?, ?, ?, ?, ?, ?, ?)", stocktuple)


# cursor.execute('drop table HistoryPrice')

# cursor.execute('create table TrueTimeValue (Symbol varchar(20), TradePrice float, TadeTime date, Volume int)')
# print "Opened database successfully";

cursor.close()
conn.close()
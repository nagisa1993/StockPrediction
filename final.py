import sqlite3 as lite
import sys
import datetime 
from yahoo_finance import Share
import datetime
import tables
from flask import Flask, session,request,redirect, url_for, abort, render_template, flash
from flask.ext.session import Session
import calendar

import numpy as np
import fetchdata
from sklearn.svm import SVR
#######################


app = Flask(__name__)

# Check Configuration section for more details
# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# Session(app)

@app.route('/')
def hello():
    return redirect(url_for('foo/<ts>/<123>'))

@app.route('/foo/<name>/<pwd>')
def foo():
    return 'Hello Foo!'

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/predict', methods=['GET'])
def predict_form():
    return '''<form action="/predict" method="post">
              <select id="ddlViewBy" name="s1">
              <option id="o1" value="AAPL">AAPL</option>
              <option id="o2" value="GOOG">GOOG</option>
              <option id="o3" value="AMZON">AMZN</option>
              </select>
              <p><input name="begindate"></p>
              <p><input name="enddate"></p>
              <input type="submit" name="add" value="Check">        
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
  conn = lite.connect('StockHistory.db')
  cursor = conn.cursor()
  cursor.execute('select Pwd from Users where UserID=' + request.form['username'])
  array = cursor.fetchall()
  conn.commit()
  cursor.close()
  conn.close()
  if  request.form['password']==array[0][0]:
      session['user'] =request.form['username']
      return redirect(url_for('predict'))
      #return render_template('problem2.html', form=form)   
  return '<h3>Bad username or password.</h3>'

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
      if session['user'] =="":
        #return session['user']
        return '<h3>please log in firstly.</h3>'
      session['name'] =request.form['s1']
      session['begindate'] =request.form['begindate']
      session['enddate'] =request.form['enddate']
      #return session['begindate']
      if 'Check' in request.form.values():
          return redirect(url_for('baz'))
            #return session['begindate']
    elif request.method == 'GET':
        return render_template('contact.html', form=form)
@app.route('/baz')
def baz():
    if session['user'] =="":
        #return session['user']
        return '<h3>please log in firstly.</h3>'
    name = session['name']
    conn = lite.connect('StockHistory.db')
    cursor = conn.cursor()
    #where Symbol ='"+ name +"' and TadeTime between '"+session['begindate'] +"'and '"+session['enddate']+"'"
    cursor.execute("select * from HistoryValue where Symbol ='"+ name +"' and TadeTime between '"+session['begindate'] +"'and '"+session['enddate']+"'")
    array = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('foo.html', my_list=array)

@app.route('/index')
def index(chartID = 'chart_ID', chart_type = 'line', chart_height = 350):
    liststock=svm_predict(days=10, offset=0, name='YHOO')
    listtime=[1,2,3,4,5,6,7,8,9,10]
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": liststock}]
    title = {"text": 'SVM'}
    xAxis = {"categories": listtime}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

########################
def beyes():
	return 10

def network():
	return 20
def svm_predict(days=10, offset=0, name='YHOO'):
    N = 30
    X = np.arange(N).reshape(N, 1)
    y = fetchdata.get_data(name).ravel()
    Z = np.arange(N+offset, N+days+offset).reshape(days, 1)
    svr_lin = SVR(kernel='linear', C=1e3)
    y_lin = svr_lin.fit(X, y).predict(Z)
    return list(y_lin)
########################
if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
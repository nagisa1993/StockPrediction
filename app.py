from flask import Flask, session, request, redirect, url_for, render_template, abort, jsonify
import sqlite3 as lite
from flask import make_response
import svm
import MLP
import bayes
import datetime
import json
import calendar
import pandas as pd
from dateutil.relativedelta import relativedelta

#####
import fetchdata
import numpy as np
from sklearn.svm import SVR

app = Flask(__name__)


# Check Configuration section for more details
# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# Session(app)

@app.route('/', methods=['GET', 'POST'])
def route():
    if request.method == 'POST':
        #pdb.set_trace()
        # return '<h3>please log in firstly.</h3>'
        if request.form.values():
            # return redirect(url_for('search', par=str(request.form['stockid'])))
            return render_template('search.html', par = str(request.form['stockid']))
    return render_template('base.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #pdb.set_trace()
        #return '<h3>please log in firstly.</h3>'
        if request.form.values():
            # json = createjson(request.form['stockid'])
            # return '<h3>please log in firstly.</h3>'
            # pdb.set_trace()
            # return render_template('predict.html', par = str(request.form['stockid']))
            # return str(request.form['stockid'])
            return redirect(url_for('predict', stockname=request.form['stockid']))

    return render_template('index.html')

@app.route('/search/')
def search():
    return render_template('search.html')

# @app.route('/predict')
# def predict():
#     return render_template('predict.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def createjson():
    # data = []
    # predicted_data = svm.svm_predict(30, 0, name)
    # for x in predicted_data:
    #     data.append(round(x, 3))
    #
    # utc = []
    #
    # today = datetime.date.today()
    # thirtyday = datetime.timedelta(days=30)
    #
    # daterange = pd.date_range(today, today + thirtyday)
    # for single_date in daterange:
    #     utc.append(calendar.timegm(single_date.timetuple()))
    #
    # json_data = []
    #
    # for x in range(1, 31):
    #     json_data.append([utc[x - 1], data[x - 1]])

    # b = '([1461110400000,107.13],[1461196800000,105.97],[1461283200000,105.68],[1461542400000,105.08],[1461628800000,104.35],[1461715200000,97.82]]);'
    b = [[1461110400000,107.13],[1461196800000,105.97],[1461283200000,105.68],[1461542400000,105.08],[1461628800000,104.35],[1461715200000,97.82]]
    # return json.dumps(b)
    # return json.dumps(json_data,separators=(',',','))


@app.route('/signin', methods=['POST'])
def signin():
    conn = lite.connect('StockHistory.db')
    cursor = conn.cursor()
    cursor.execute('select Pwd from Users where UserID=' + request.form['username'])
    array = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if request.form['password'] == array[0][0]:
        session['user'] = request.form['username']
        return redirect(url_for('predict'))
        # return render_template('problem2.html', form=form)
    return '<h3>Bad username or password.</h3>'

def getquery(strquery):
    conn = lite.connect('StockHistory.db')
    cursor = conn.cursor()
    #where Symbol ='"+ name +"' and TadeTime between '"+session['begindate'] +"'and '"+session['enddate']+"'"
    cursor.execute(strquery)
    array = cursor.fetchall()
    listPrice =[]
    # for i in array:
    #   listPrice.append(str(i[0]))
    conn.commit()
    cursor.close()
    conn.close()
    #pdb.set_trace()
    return array

lastdate = getquery("select Max(TadeTime) from HistoryValue")
tenday = datetime.timedelta(days=10)
requiredate = datetime.datetime.strptime(str(lastdate[0][0]), '%Y-%m-%d') - tenday
requiredate=str(requiredate)[:-9]
listquery2 = getquery("select Max(ClosePrice) from HistoryValue where Symbol = 'AAPL' and TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"'")
tenday = datetime.timedelta(days=365)
requiredate = datetime.datetime.strptime(str(lastdate[0][0]), '%Y-%m-%d') - tenday
requiredate=str(requiredate)[:-9]
listquery3 = getquery("select Avg(ClosePrice) from HistoryValue where Symbol = 'AAPL' and TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"'")

requiredate = datetime.datetime.strptime(str(lastdate[0][0]), '%Y-%m-%d')  - relativedelta(years=1)
requiredate=str(requiredate)[:-9]
listquery4 = getquery("select Symbol, min(ClosePrice) from HistoryValue where TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"' group by Symbol"  )

data = getquery("select Symbol, min(ClosePrice) from HistoryValue where Symbol ='GOOG' and TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"' group by Symbol"  )
listquery5 = getquery("select Symbol, Avg(ClosePrice) from HistoryValue where TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"' group by Symbol having Avg(ClosePrice) < '"+str(data[0][1])+"' "  )
listquery6 = createjson()
tasks = [
    {
        'id': 1,
        'query': "Show the list of all companies in the database along with their latest stock price.",
        'queryresult': getquery("Select distinct Symbol, ClosePrice from HistoryValue group by  Symbol "),
    },
    {
        'id': 2,
        'query': "Get the highest stock price of Google in the last ten days",
        'queryresult': listquery2
    },
    {
        'id': 3,
        'query': "Average stock price of Microsoft in the latest one year",
        'queryresult':  listquery3,
    },
    {
        'id': 4,
        'query':"Lowest stock price for each company in the latest one year",
        'queryresult': listquery4,
    },
    {
        'id': 5,
        'query': "List the ids of companies along with their name who have the average stock price lesser than the lowest of Google in the latest one year",
        'queryresult': listquery5
    }
    ,
    {
        'id': 6,
        'query': "jsondata",
        'queryresult': listquery6
    }
]

@app.route('/query/api/v1.0/get/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/query/api/v1.0/get/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        not_found("Not Found")
    return jsonify({'task': task[0]['queryresult']})

@app.route('/query/api/v1.0/getjson/tasks/<int:task_id>', methods=['GET'])
def get_task_json(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        not_found("Not Found")
    # return jsonify( task[0]['queryresult'])
    return listquery6

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/query/api/v1.0/post/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
##############################graph
@app.route('/predict/<stockname>')
def predict(stockname,chartID = 'chart_ID', chart_type = 'line', chart_height = 350):
    listtime=['2016-04-28','2016-05-01','2016-05-02','2016-05-03','2016-05-04','2016-05-05','2016-05-08','2016-05-09','2016-05-10','2016-05-11']
    # listtime =getdate()
    listtime=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # return '<h3>please log in firstly.</h3>'
    liststock=svm.svm_predict(15,0,stockname)
    # return '<h3>please log in firstly.</h3>'
    liststock1= MLP.mlp_predict(15,0,stockname)
    # liststock=[2,2,2,2,2,2,2,2,2,2]
    # pdb.set_trace()
    #return '<h3>please log in firstly.</h3>'
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'SVM', "data": liststock},{"name": 'MLP', "data": liststock1}]
    # return '<h3>please log in firstly.</h3>'
    title = {"text": 'Price in future 15 days'}
    xAxis = {"categories": listtime}
    yAxis = {"title": {"text": 'yAxis Label'}}
   # pdb.set_trace()
   #  return '<h3>please log in firstly.</h3>'
    return render_template('predict.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)



def getdate():
    name = session['name']
    conn = lite.connect('StockHistory.db')
    cursor = conn.cursor()
    #where Symbol ='"+ name +"' and TadeTime between '"+session['begindate'] +"'and '"+session['enddate']+"'"
    cursor.execute("select distinct TadeTime from HistoryValue where TadeTime between '2016-01-01'and '2016-01-10'")
    array = cursor.fetchall()
    listPrice =[]
    for i in array:
      listPrice.append(str(i[0]))
    conn.commit()
    cursor.close()
    conn.close()
########################
if __name__ == '__main__':
    # app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()

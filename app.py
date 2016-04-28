from flask import Flask, session, request, redirect, url_for, render_template,
import sqlite3 as lite
import svm
import MLP
import bayes
import datetime
import json
import calendar
import pandas as pd


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
            json = createjson(request.form['stockid'])

            # pdb.set_trace()
            return render_template('predict.html', par=str(request.form['stockid']))
    return render_template('index.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def createjson(name):
    data = []
    predicted_data = svm.svm_predict(30, 0, name)
    for x in predicted_data:
        data.append(round(x, 3))

    utc = []

    today = datetime.date.today()
    thirtyday = datetime.timedelta(days=30)

    daterange = pd.date_range(today, today + thirtyday)
    for single_date in daterange:
        utc.append(calendar.timegm(single_date.timetuple()))

    json_data = ([[x, y] for x in utc for y in data])
    return json.dumps(json_data)


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


# @app.route('/predict', methods=['POST'])
# def predict():
#     if request.method == 'POST':
#         if session['user'] == "":
#             # return session['user']
#             return '<h3>please log in firstly.</h3>'
#         session['name'] = request.form['s1']
#         session['begindate'] = request.form['begindate']
#         session['enddate'] = request.form['enddate']
#         # return session['begindate']
#         if 'Check' in request.form.values():
#             return redirect(url_for('baz'))
#             # return session['begindate']
#     elif request.method == 'GET':
#         return render_template('contact.html', form=form)




########################
if __name__ == '__main__':
    # app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()

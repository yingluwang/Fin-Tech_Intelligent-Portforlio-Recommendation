# all the imports
import psycopg2
import nltk
from robovest.portfolio import*
#nltk.download()
import tweepy
import os
import sqlite3
import datetime
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py




tickers = ["MINT","EMB","IAU","VCIT","MUB","SCHA","VEA","VYM","SCHH","VWO","FENY","VTIP","VGLT","ITE"]
Twitter_Average=.0091
Twitter_STD=.154
consumer_key = os.environ["TWITTER_API_KEY"]
consumer_secret = os.environ["TWITTER_API_SECRET"]
access_token = os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
# AUTHENTICATE
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# INITIALIZE API CLIENT
api = tweepy.API(auth)
startDate = datetime.datetime(2017, 7, 1, 0, 0, 0)
endDate =   datetime.datetime(2017, 8, 4, 0, 0, 0)



# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'robovest.db'),
    SECRET_KEY='development key',
    USERNAME='robo',
    PASSWORD='vest'
))
app.config.from_envvar('ROBOVEST_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def age_adj():
    db = get_db()
    cur = db.execute('select age from entries')
    age1 = cur.fetchone()[0]
    if age1 > 82 or age1  == 82:
        age1_adj = 0
    elif age1  < 35 or age1  == 35:
        age1_adj = 1
    else:
        age1_adj = (-0.021)*(age1 -35+1)+1.02
    return age1_adj

def income_adj():
    db = get_db()
    cur = db.execute('select income from entries order by id desc')
    income1 = cur.fetchone()[0]
    if income1 > 10500 or income1 == 10500:
        income_adj1 = 1
    elif income1 < 3750 or income1 == 3750:
        income_adj1 = 0
    else:
        income_adj1 = (-0.00015)*(10500-income1)+1
    return income_adj1

def worth_adj():
    db = get_db()
    cur = db.execute('select worth from entries order by id desc')
    worth1 = cur.fetchone()[0]
    if worth1 > 25000 or worth1 == 25000:
        worth_adj1 = 1
    elif worth1 < 5000 or worth1 == 5000:
        worth_adj1 = 0
    else:
        worth_adj1 = (-0.00005)*(25000-worth1)+1
    return worth_adj1

def pref_adj():
    db = get_db()
    cur = db.execute('select preference from entries order by id desc')
    pref1 = cur.fetchone()[0]
    if pref1 == "b":
        q1 = 1
    else:
        q1 = 2
    return q1

def house_adj():
    db = get_db()
    cur = db.execute('select household from entries order by id desc')
    house = cur.fetchone()[0]
    if house == "b" or house == "d":
        q2 = 1.5
    else:
        q2 = 2
    return q2

def action_adj():
    db = get_db()
    cur = db.execute('select action from entries order by id desc')
    action1 = cur.fetchone()[0]
    if action1 == "a":
        q3 = 1
    elif action1 == "b":
        q3 = 2
    elif action1 == "c":
        q3 = 2.5
    else:
        q3 = 3
    return q3

def adj_sentiment():
    db = get_db()
    cur = db.execute('select handle from entries order by id desc')
    handle1 = cur.fetchone()
    tweetxt=[]
    tweets = api.user_timeline(screen_name= handle1, count=1000, includerts=False)
    for tweet in tweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweetxt.append(tweet.text)
    sa = SentimentIntensityAnalyzer()
    scores_ind = []
    for twit in tweetxt:
        score = sa.polarity_scores(twit)
        scores_ind.append(score)
    diff_ind_list = [ ]
    for row in scores_ind:
        pos = row["pos"]
        neg = row["neg"]
        def dif(pos,neg):
            return float(pos-neg)
        diff_ind = dif(pos,neg)
        diff_ind_list.append(diff_ind)
    avg_ind = np.mean([diff_ind_list])
    adj1_sentiment= (avg_ind-Twitter_Average)/(1.96*Twitter_STD)
    return adj1_sentiment

def risk_tolerance():
    z=age_adj()
    y=income_adj()
    x=worth_adj()
    w=pref_adj()
    v=house_adj()
    u=action_adj()
    t=adj_sentiment()
    #risk_score=age_adj+income_adj+worth_adj+q1+q2+q3
    risk_score=z+y+x+w+v+u+t
    return risk_score

# def portfolio_recommendation(score):
#     weights_bl, return_bl, risk_bl = portfolio(score)
#     return weights_bl, return_bl, risk_bl




@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (alias, age, income, worth, preference, household, action, handle) values (?, ?, ?, ?, ?, ?, ?, ?)',
                 [request.form['alias'], request.form['age'], request.form['income'], request.form['worth'], request.form['preference'], request.form['household'], request.form['action'],request.form['handle']])
    risk1=risk_tolerance()
    db.execute('insert into entries (risk) values (?)',[risk1])
    weights_bl, return_bl, risk_bl = portfolio(risk1)
    db.execute('insert into entries (etf1, etf2, etf3, etf4, etf5, etf6, etf7, etf8, etf9, etf10, etf11, etf12, etf13, etf14, return, vol) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[weights_bl[0],weights_bl[1],weights_bl[2],weights_bl[3],weights_bl[4],weights_bl[5],weights_bl[6],weights_bl[7],weights_bl[8],weights_bl[9],weights_bl[10],weights_bl[11],weights_bl[12],weights_bl[13],return_bl,risk_bl])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/index', methods=['GET','POST'])
def image():
    return render_template('index.html')


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select alias, age, income, worth, preference, household, action, risk, etf1, etf2, etf3, etf4, etf5, etf6, etf7, etf8, etf9, etf10, etf11, etf12, etf13, etf14, return, vol from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Thanks for logging in, lets get started!')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

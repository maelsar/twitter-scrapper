from flask import Flask, render_template, request, redirect, Response
import re

import snscrape.modules.twitter as sntwitter
import pandas as pd
import sqlite3
import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('history.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def get_tweets():
    conn = get_db()
    data = conn.execute('SELECT * FROM (SELECT * FROM search_history ORDER BY "index" DESC limit 5) ORDER BY "index" ASC').fetchall()
    conn.close()

    return render_template('index.html', data=data)

@app.route('/', methods=['POST'])
def post_form():
    query = ''
    keywords = request.form.get('keywords')
    user = request.form.get('user')
    s_since = request.form.get('s_since')
    s_until = request.form.get('s_until')
    limits = int(request.form.get('limit'))
    t_header = []
    if keywords == '' or keywords == None:
        h_keywords = None
        keywords = ''
    else:
        keywords.rstrip().lstrip()
        h_keywords = keywords
        keywords = re.sub("\s+", ' ', keywords)
    
    if user == '' or user == None:
        h_user = None
        user = ''
    else:
        h_user = user
        user = ' (from:'+user+')'
    if s_since == '' or s_since == None:
        h_fsince = None
        fsince = ''
    else:
        fsince = ' since:'+s_since
    if s_until == '' or s_until == None:
        h_funtil = None
        funtil = ''
    else:
        funtil = ' until:'+s_until

    if limits <= 1:
        limits = 1
    elif limits > 500:
        limits = 500

    query = keywords + user + funtil + fsince
    
    #return parameters
    return1 = request.form.get('r_url')
    return2 = request.form.get('r_date')
    return3 = request.form.get('r_user')
    return4 = request.form.get('r_content')
    #return5 = request.form.get('r_raw')
    r_param = ''
    #if return5 == 'True':
    #    r_param = 'tweet'
    #else:
    if return1 == 'True': 
        return1 = 'tweet.url '
        t_header.append('URL')
    else: 
        return1 = ''
    if return2 == 'True': 
        return2 = 'tweet.date '
        t_header.append('Date')
    else: 
        return2 = ''
    if return3 == 'True': 
        return3 = 'tweet.user.username '
        t_header.append('User')
    else: 
        return3 = ''
    if return4 == 'True': 
        return4 = 'tweet.content '
        t_header.append('Content')
    else: 
        return4 = ''

    #Error Message if Return Parameter is None
    #if return1 == '' and return2 == '' and return3 == '' and return4 == '':
    #    flash('You must check at least 1 Return Parameters')
    #    return redirect('/')

    r_param = return1 + return2 + return3 + return4
    r_param = r_param.rstrip()
    r_param = re.sub(' ', ', ', r_param)
    '''x="thisisploky"
    y="x.upper()"
    z=eval(y)
    print(z)
    '''

    def get_tweets(query, r_param):
        query = query
        tweets = []
        r_param = r_param
        limit = 5

        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            #print(tweet)
            if len(tweets) == limit:
                break
            else:
                tweets.append([eval(r_param)])
                #tweets.append([tweet.date, tweet.content])
        #print(tweets)
        #df = pd.DataFrame(tweets, columns=["Date", "Tweet"])
        #df.to_csv("test.csv")
        #print(df)

        return tweets

    #sample = [[["https://twitter.com/EmperorBTC/status/1573551964591632384","Sat, 24 Sep 2022 05:56:38 GMT","EmperorBTC","Had breakfast with Duck and his family. \n\nI wish all of you a great weekend with the family. https://t.co/gbqCQplu23"]],[["https://twitter.com/EmperorBTC/status/1572936580171730946","Thu, 22 Sep 2022 13:11:19 GMT","EmperorBTC","WHAT INDICATORS ARE THE BEST? \n\nThere are 2 indicators I used to hate and found illogical. \n\nThen found a trader who spent so much screentime using it, they were consistently profitable.\n\nRealised that maybe even stupid indicators become useful when spent enough time with it."]],[["https://twitter.com/EmperorBTC/status/1572649809437392896","Wed, 21 Sep 2022 18:11:47 GMT","EmperorBTC","FED HIKES LENDING RATE BY 0.75%, LIQUIDATING EVERYONE WHO WAS LONG OR SHORT. 1K CANDLE PRINTED IN A MINUTE LIQUIDATING $30 MILLION CONTRACTS. https://t.co/Az2tfr3rZ0"]],[["https://twitter.com/EmperorBTC/status/1572588677595025408","Wed, 21 Sep 2022 14:08:52 GMT","EmperorBTC","Fibonacci Master-Class Cheat Sheet. Stick this on your brain and be ready for the next Lesson. https://t.co/1iIll1t0QT"]],[["https://twitter.com/EmperorBTC/status/1572468505592868865","Wed, 21 Sep 2022 06:11:21 GMT","EmperorBTC","The market is going to have a decisive day, here is one advice.\n\nThe worst thing you can do is to bet huge on one trade.\n\nAim should be to get as much experience and feedback from the market by betting small, more times.\n\nSmall bets but more bets &gt; Big Bets."]]]

    #Add to Search History
    if request.method == 'POST':
        now = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")
        conn = get_db()
        conn.execute('INSERT INTO search_history (date_searched, keywords_search, user_search, "limit", beginning_date, end_date) \
            VALUES (?,?,?,?,?,?)', (now, h_keywords, h_user, limits, h_fsince, h_funtil))
        conn.commit()
        conn.close()

    #return get_tweets(query, r_param)
    t_limit = str(limits)
    return render_template("results.html", tweets=get_tweets(query, r_param), query=query, r_param=r_param, t_header=t_header, t_limit=t_limit)
    #return redirect('/')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/results", methods=["GET", "POST"])
def download_tweets():
    if request.method == "GET":
        return render_template("results.html", tweets=get_tweets(query, r_param), query=query, r_param=r_param, t_header=t_header, t_limit=t_limit)
    else:
        dquery = request.form.get('query')
        d_param = request.form.get('r_param')
        dlimits = int(request.form.get('dlimit'))
        d_header = request.form.get('t_header')
        #keywords = re.sub("\s+", ' ', keywords)
        d_header = re.sub("[\[\]',]", "", d_header)
        col = d_header.split(" ")
        col = [x.lower() for x in col]
        #col = str(col)
        return Response(col, mimetype='text/csv', headers={"Content-disposition": "attachment; filename=tweets.csv"})

        dtweets = []
        #return d_param

        for tweet in sntwitter.TwitterSearchScraper(dquery).get_items():
            #print(tweet)
            if len(dtweets) == dlimits:
                break
            else:
                dtweets.append([eval(d_param)])
                #tweets.append([tweet.date, tweet.content])
            #print(tweets)
            #df = pd.DataFrame(tweets, columns=["Date", "Tweet"])
            #df.to_csv("test.csv")
            #print(df)
        return redirect("/results")
        #return Response(dtweets, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=tweets.csv"})

if __name__ == "__main__":
    app.run(debug=True)

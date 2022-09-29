from flask import Flask, render_template, request, redirect, make_response
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
    if query is None or query == "":
        query = "python"
    #return parameters
    return1 = request.form.get('r_url')
    return2 = request.form.get('r_date')
    return3 = request.form.get('r_user')
    return4 = request.form.get('r_content')
    r_param = ''
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
            if len(tweets) == limit:
                break
            else:
                tweets.append([eval(r_param)])

        return tweets

    #Add to Search History
    if request.method == 'POST':
        now = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")
        conn = get_db()
        conn.execute('INSERT INTO search_history (date_searched, keywords_search, user_search, "limit", beginning_date, end_date) \
            VALUES (?,?,?,?,?,?)', (now, h_keywords, h_user, limits, h_fsince, h_funtil))
        conn.commit()
        conn.close()

    t_limit = str(limits)
    return render_template("results.html", tweets=get_tweets(query, r_param), query=query, r_param=r_param, t_header=t_header, t_limit=t_limit)


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
        d_header = re.sub("[\[\]',]", "", d_header)
        col = d_header.split(" ")
        col = [x.lower() for x in col]

        dtweets = []
        for tweet in sntwitter.TwitterSearchScraper(dquery).get_items():
            #print(tweet)
            if len(dtweets) == dlimits:
                break
            else:
                dtweets.append(eval(d_param))
        dataframe = pd.DataFrame(dtweets, columns=col)
        output = make_response(dataframe.to_csv(index=False))
        output.headers["Content-Disposition"] = "attachment; filename=tweets.csv"
        output.headers["Content-Type"] = "text/csv"
        return output

if __name__ == "__main__":
    app.run()

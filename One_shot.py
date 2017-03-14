from flask import Flask,render_template,send_from_directory
from flask_tweepy import Tweepy
import apiai 
import json
import pandas as pd
import os

# Client Access Token for accessing the API AI Bot
CLIENT_ACCESS_TOKEN = "080ff7299dda438ba4906d6f312952b5"

app = Flask(__name__)
app.config.setdefault('TWEEPY_CONSUMER_KEY', "0qX8JlT1tD8YVwgrfjtFMi6dd")
app.config.setdefault('TWEEPY_CONSUMER_SECRET', "Qa63v78t4GDOqNENVXpovJSAZfOxhDHeYAKjGB2rCejbFLba5o")
app.config.setdefault('TWEEPY_ACCESS_TOKEN_KEY', "32907998-y27sQnXBeR9jaYUJ5ce99Fwj9ML5nGfBJYpazg0nt")
app.config.setdefault('TWEEPY_ACCESS_TOKEN_SECRET', "b2xHZTigMU25MrIx5uY3JBQWFUyhm6z1kwsZ1EJCiC2p1")

tweepy = Tweepy(app)

@app.route('/')

def show_tweets():

    Tweets = tweepy.api.search(q = 'Fabelle',count = 20)
    Content = []
    for tweet in Tweets:
    	if tweet.lang == 'en':
    		Content.append(tweet.text.encode('ascii','ignore'))
    
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    response = []
    
    
    for i in xrange(0,len(Content)):
    	request = ai.text_request()
        request.lang = 'en'
    	request.query = Content[i]
    	jresponse = request.getresponse().read().decode('utf-8')
    	response.append(str(json.loads(jresponse)['result']['fulfillment']['speech']))
    
    if len(Content)==len(response):
    	combine = dict(zip(Content,response))
    	data = pd.DataFrame.from_dict(combine,orient = 'index')
    	data.to_csv('Report.csv')
    else:
    	return "Something seems to be wrong with external factors, please refresh after some time"


    return render_template('Render2.html', data = data.to_html())#, send_from_directory(directory = app.config['~/'],filename = 'Report.csv')


if __name__=='__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
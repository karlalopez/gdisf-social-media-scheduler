# GDI Social Media Scheduler (for Twitter)

## What it does

- Reads the spreadhseet
- Gets information only from upcoming workshops
- Gets photos
- Randomly picks a message and a photo
- Posts message to Twitter every X seconds

## Running locally

First, get it ready to run locally:

- Install required dependencies:
```$ pip install -r requirements.txt``` 

- Export the needed credentials as variables:

```
export TWITTER_CKEY='your_twitter_consumer_key'
```
```
export TWITTER_CSECRET='your_twitter_consumer_secret'
```
```
export TWITTER_ATOKEN='your_twitter_app_token'
```
```
export TWITTER_ASECRET='your_twitter_app_secret'
```
```
export SPREADSHEET_ID='id_of_the_google_spreadsheet'
```
```
export SPREADSHEET_CREDENTIALS='json_credentials_from_google_apps'
```
- Add your photos to /photos

- Define your time interval (to post) in seconds. Ex: 3600 for 1 hour.
```
export INTERVAL=3600
```

- Run:
```$ python app.py``` 

## Deploying it to Heroku

- First, create a Heroku account: https://signup.heroku.com/

- Create a new app on Heroku: New >> Create new app

- Install the Heroku Toolbelt: https://toolbelt.heroku.com/

- Login to Heroku on Terminal:
```
$ heroku login
Enter your Heroku credentials.
Email: your@email.com
Password:
Authentication successful.
```

- Add Heroku's remote git repo
```
$ heroku git:remote -a name_of_your_heroku_app
```

- Export the needed credentials as variables:

```
$ heroku config:set TWITTER_CKEY='your_twitter_consumer_key'
```
```
$ heroku config:set TWITTER_CSECRET='your_twitter_consumer_secret'
```
```
$ heroku config:set TWITTER_ATOKEN='your_twitter_app_token'
```
```
$ heroku config:set TWITTER_ASECRET='your_twitter_app_secret'
```
```
$ heroku config:set SPREADSHEET_ID='id_of_the_google_spreadsheet'
```
```
$ heroku config:set SPREADSHEET_CREDENTIALS='json_credentials_from_google_apps'
```
- Define your time interval (to post) in seconds. Ex: 3600 for 1 hour.
```
$ heroku config:set INTERVAL=3600
```

- To deploy, push the code via Git:
```
$ git push heroku
```
- When the deploy is done, you will see something like this:
```
remote:
remote: -----> Discovering process types
remote:        Procfile declares types -> worker
remote:
remote: -----> Compressing...
remote:        Done: 50.1M
remote: -----> Launching...
remote:        Released v7
remote:        https://name_of_your_heroku_app.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
```
- Back to Heroku's web dashboard, click on Resources.

- On Free Dynos, on the right hand side, click on the little pencil icon

- Click on the toggle to turn it on, then click on Confirm.

- Check if it's working
```
$ git heroku logs
```
- It should look like this:
```
2017-06-22T21:18:40.816181+00:00 heroku[worker.1]: Starting process with command `python app.py --log-file=-`
2017-06-22T21:18:41.379091+00:00 heroku[worker.1]: State changed from starting to up
2017-06-22T21:19:16.556033+00:00 app[worker.1]:
2017-06-22T21:19:16.555956+00:00 app[worker.1]: SUCCESS: Thu Jun 22 21:19:15 2017 - Event Date Event message Event link
2017-06-22T21:19:46.386584+00:00 app[worker.1]: SUCCESS: Thu Jun 22 21:19:45 2017 - Event Date Event message Event link
2017-06-22T21:19:46.388149+00:00 app[worker.1]:
2017-06-22T21:20:16.592266+00:00 app[worker.1]: SUCCESS: Thu Jun 22 21:20:15 2017 - Event Date Event message Event link
```

### Logs - What you will see printed on Terminal or on Heroku Logs

- Successful tweet log:
```
LOG_TIME_DATE app[worker.1]: SUCCESS: DATE_POSTED - EVENT_DATE EVENT_MESSAGE EVENT_LINK
```
- Failed tweet log:
```
DATE app[worker.1]: ERROR: [{u'code': ERROR_CODE, u'message': u'ERROR_MESSAGE'}] - LOG_TIME_DATE - DATE_POSTED - EVENT_DATE EVENT_MESSAGE EVENT_LINK
```

### Troubleshooting common problems

- Variables are not exported. Check them with `$ printenv` if you're running it locally. If it's on Heroku, you can check them going to Settings > Reveal Config Vars.

- The SPREADSHEET_CREDENTIALS is the most likely to give you a headache, so make sure you validade your json before exporting it. You can always commit the json file and point to it on the code. It's simpler, but not very safe.

### Credentials

#### Google
- Go to https://console.developers.google.com/apis/credentials/
- Click Create credentials >> Service account key
- On Service account, select New service account
- Add Service account name and Service account ID
- JSON should be selected
- Click Create
- JSON will be downloaded. The contents of this JSON is your `SPREADSHEET_CREDENTIALS`

- Go to your spreadsheet
- On your JSON there's a key "client_email"
- Share your spreadhseet with that email. It looks like  `0123456789-compute@developer.gserviceaccount.com`
- Your spreadsheet URL look like this: `https://docs.google.com/spreadsheets/d/XXXXXXXXXXXXXXXXXXXXXXX/edit#gid=0`. Copy what's between `https://docs.google.com/spreadsheets/d/` and `/edit#gid=0`. That's your `SPREADSHEET_ID`

#### Twitter
- Go to https://apps.twitter.com/
- Click Create new app
- Fill out the required fields
- Click on Create your Twitter application
- Click on Keys and Access tokens
- Click on Create my access token
- On this screen:
Consumer Key (API Key) is your `TWITTER_CKEY`
Consumer Secret (API Secret) is your `TWITTER_CSECRET`
Access Token is your `TWITTER_ATOKEN`
Access Token Secret	is yout `TWITTER_ASECRET`

### About the spreadsheet format:

- You can make a copy of this spreadsheet: http://bit.ly/GDIpostscheduler
- To use it exactly as is is, add your event information to the green columns
- Always use URL shortner
- Make sure the Count is less than 140 chars

*IMPORTANT*
- Don't change the number of columns or rearrange them. Gspread goes off the index of the columns, so if you change it, you will have to change the indexes `getTweets()`
- You can get edit the Final message formula to create the message you want.
- Year, Date and Final Message are mandatory. The Date needs to be in the future, otherwise the message won't be tweeted.


### Based on:

- https://github.com/lagleki/schedule-post-to-twitter
- http://jennielees.github.io/full-stack/spread-the-love/
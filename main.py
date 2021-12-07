import tweepy
import praw
import hottakesauth

# Twitter Auth
CONSUMER_KEY = hottakesauth.CONSUMER_KEY
CONSUMER_SECRET = hottakesauth.CONSUMER_SECRET
ACCESS_TOKEN = hottakesauth.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = hottakesauth.ACCESS_TOKEN_SECRET
# Reddit Auth
reddit = praw.Reddit(
    client_id=hottakesauth.CLIENT_ID,
    client_secret=hottakesauth.CLIENT_SECRET,
    user_agent=hottakesauth.USER_AGENT,
)

for submission in reddit.subreddit("formula1").controversial("day", limit=1):
    submission.comment_sort = "controversial"
    if submission.comments[0].author == "automoderator":
        TWEET = submission.comments[0 + 1].body
    else:
        TWEET = submission.comments[0].body

# Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY,
                           CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN,
                      ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Check tweet is unique, and if it is, post it.
LASTTWEET = api.user_timeline(screen_name=hottakesauth.SCREEN_NAME,
                              count=1,
                              include_rts=False,
                              tweet_mode='extended')
for i in LASTTWEET:
    OLDTWEET = i.full_text

if TWEET != OLDTWEET:
    api.update_status(TWEET)
else:
    print("Duplicate")
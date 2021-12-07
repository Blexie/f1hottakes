import tweepy
import praw
import hottakesauth
from random import randrange

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
        COMMENT = submission.comments[0 + 1].body
    else:
        COMMENT = submission.comments[0].body

# Random @ Mention

with open("ats.txt") as file:
    ATS = file.readlines()
    ATS = [line.rstrip() for line in ATS]

NUM_ATS = len(ATS)

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

TWEET = COMMENT + " " + ATS[randrange(NUM_ATS)] + " #F1"
if COMMENT != OLDTWEET:
    api.update_status(TWEET)
    print("Tweeted" + TWEET)
else:
    print("Did not tweet: " + TWEET)
    print("Duplicate")
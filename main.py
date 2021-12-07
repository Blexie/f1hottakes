import tweepy
import praw
import hottakesauth
import string
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

# Generate tweet body.
def generatetweet():
    for submission in reddit.subreddit("formula1").controversial("day", limit=1):
        submission.comment_sort = "controversial"
        if submission.comments[0].author == "automoderator":
            COMMENT = submission.comments[0 + 1].body
        else:
            COMMENT = submission.comments[0].body
    return COMMENT


# Random @ Mention
def randomat():
    with open("ats.txt") as file:
        ATS = file.readlines()
        ATS = [line.rstrip() for line in ATS]

    NUM_ATS = len(ATS)
    return ATS[randrange(NUM_ATS)]


# Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY,
                           CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN,
                      ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Get last tweet for comparison.
LASTTWEET = api.user_timeline(screen_name=hottakesauth.SCREEN_NAME,
                              count=1,
                              include_rts=False,
                              tweet_mode='extended')
for i in LASTTWEET:
    OLDTWEET = i.full_text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

for i in LASTTWEET:
    OLDTWEET = strip_all_entities(i.full_text)

COMMENT = generatetweet()

RBRMATCHES = ["rbr", "RBR", "Max", "Red Bull"]

if any(x in COMMENT for x in RBRMATCHES):
    AT = "@redbullracing"
else:
    AT = randomat()

TWEET = COMMENT + " " + AT + " #F1"
if COMMENT != OLDTWEET:
    api.update_status(TWEET)
    print("Tweeted: " + TWEET)
    print(OLDTWEET)
elif len(TWEET) >280:
    print("Unable to tweet: " +TWEET)
    print("Tweet too long" + len(TWEET))
else:
    print("Did not tweet: " + TWEET)
    print("Duplicate: "+ OLDTWEET)
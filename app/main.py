import tweepy
import praw
import hottakesauth
from random import randrange, choice
from time import sleep

# Twitter Setup
CONSUMER_KEY = hottakesauth.CONSUMER_KEY
CONSUMER_SECRET = hottakesauth.CONSUMER_SECRET
ACCESS_TOKEN = hottakesauth.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = hottakesauth.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY,
                           CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,
                      ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Reddit Auth
reddit = praw.Reddit(
    client_id=hottakesauth.CLIENT_ID,
    client_secret=hottakesauth.CLIENT_SECRET,
    user_agent=hottakesauth.USER_AGENT,
)


# Generate tweet body (controversial threads)
def generatetweet():
    for submission in reddit.subreddit("formula1").controversial("day", limit=1):
        submission.comment_sort = "controversial"
        if submission.comments[0].author == "automoderator":
            COMMENT = submission.comments[0 + 1].body
            ID = submission.comments[0 + 1].id
        else:
            COMMENT = submission.comments[0].body
            ID = submission.comments[0].id
    return COMMENT, ID


# Generate tweet body (hot threads)
def generatetweethot():
    for submission in reddit.subreddit("formula1").hot(limit=10):
        submission.comment_sort = "controversial"
        if not submission.stickied:
            if submission.comments[0].author == "automoderator":
                print(submission.title)
                COMMENT = submission.comments[0 + 1].body
                ID = submission.comments[0 + 1].id
                break
            else:
                print(submission.title)
                COMMENT = submission.comments[0].body
                ID = submission.comments[0].id
                break
    return COMMENT, ID


# Random @ Mention
def randomat():
    with open("ats.txt") as file:
        ATS = file.readlines()
        ATS = [line.rstrip() for line in ATS]

    NUM_ATS = len(ATS)
    return ATS[randrange(NUM_ATS)]


def sendit():
    # Choose hot or controversial thread
    hotornot = [generatetweet, generatetweethot]
    COMMENT = choice(hotornot)()

    RBRMATCHES = ["rbr", "RBR", "Max", "Red Bull"]
    WILLIAMSMATCHES = ["williams"]
    RUSSELLMATCHES = ["Russell"]

    if any(x in COMMENT[0] for x in RBRMATCHES):
        AT = "@redbullracing"
    elif any(x in COMMENT[0] for x in WILLIAMSMATCHES):
        AT = "@WilliamsRacing"
    elif any(x in COMMENT[0] for x in RUSSELLMATCHES):
        AT = "@GeorgeRussell63"
    else:
        AT = randomat()
# Check for repetition
    with open("volume/" + "oldtweets.txt") as file:
        OLDTWEETS = file.readlines()

    OLDTWEETFILE = open('volume/' + 'oldtweets.txt', 'a')
    TWEET = COMMENT[0] + " " + AT + " #F1"
    if COMMENT[1] not in OLDTWEETS and len(TWEET) < 280:
        api.update_status(TWEET)
        print("Tweeted: " + TWEET)
        OLDTWEETFILE.write(COMMENT[1])
        OLDTWEETFILE.close()
    elif len(TWEET) > 280:
        print("Unable to tweet: " + TWEET)
        print("Tweet too long" + len(TWEET))
    elif COMMENT[1] in OLDTWEETS:
        print("Did not tweet: " + TWEET)
        print("Duplicate: " + COMMENT[1])
    else:
        print("Unknown error.")


try:
    while True:
        sendit()
        sleep(21600)
except KeyboardInterrupt:
    print("Interrupted!")

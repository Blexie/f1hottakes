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
    BREAKFLAG = None
    COMMENT = None
    ID = None
    for submission in reddit.subreddit("formula1").controversial(time_filter="day", limit=1):
        submission.comment_sort = "controversial"
        if BREAKFLAG is None:
            if "Race Discussion" in submission.title or not submission.stickied:
                for comment in submission.comments:
                    if comment.author == "automoderator" or comment.stickied or comment.body == "[removed]" or comment.body == "[deleted]" or len(comment.body) > 280:
                        print("Skipping comment: " + comment.permalink)
                        continue
                    else:
                        COMMENT = comment.body
                        ID = comment.id
                        BREAKFLAG = True
                        print("Comment selected: " + comment.permalink)
                        break
        else:
            break
    if COMMENT is not None:
        return COMMENT, ID
    else:
        return "REDDIT DOWN", 1


# Generate tweet body (hot threads)
def generatetweethot():
    BREAKFLAG = None
    COMMENT = None
    ID = None
    for submission in reddit.subreddit("formula1").hot(limit=10):
        submission.comment_sort = "controversial"
        if BREAKFLAG is None:
            if "Race Discussion" in submission.title or "Qualifying Discussion" in submission.title or not submission.stickied:
                for comment in submission.comments:
                    if comment.author == "automoderator" or comment.stickied or comment.body == "[removed]" or comment.body == "[deleted]" or len(comment.body) > 280:
                        print("Skipping comment: " + comment.permalink)
                        continue
                    else:
                        COMMENT = comment.body
                        ID = comment.id
                        BREAKFLAG = True
                        print("Comment selected: " + comment.permalink)
                        break
        else:
            break
    if COMMENT is not None:
        return COMMENT, ID
    else:
        return "REDDIT DOWN", 1


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
    if COMMENT[0] == "REDDIT DOWN":
        print("Reddit seems to be down. Sleeping...")
        return

    # Team and Driver Twitter Handles
    RBRMATCHES = ["rbr", "max", "red bull", "verstappen", "perez", "checo"]
    WILLIAMSMATCHES = ["williams", "sargeant", "logan", "alex", "albon"]
    RUSSELLMATCHES = ["russell", "george"]
    MERCEDESMATCHES = ["lewis", "mercedes", "merc", "hamilton"]
    ALPINEMATCHES = ["pierre", "gasly", "alpine", "ocon"]
    ASTONMATCHES = ["stroll", "fernando", "alonso", "aston"]
    FERRARIMATCHES = ["charles", "leclerc", "carlos", "sainz", "ferrari", "sbinalla"]
    MCLARENMATCHES = ["lando", "norris", "piastri", "oscar", "mclaren"]
    ALFAMATCHES = ["alfa", "bottas", "valtteri", "zhou", "guanyu"]
    HAASMATCHES = ["hulkenberg", "hulk", "kevin", "magnussen", "kmag", "haas", "steiner"]
    ALPHATMATCHES = ["de vries", "nyck", "yuki", "tsunoda", "alpha tauri"]

    if any(x in COMMENT[0] for x in RBRMATCHES):
        AT = "@redbullracing"
    elif any(x in COMMENT[0].lower() for x in WILLIAMSMATCHES):
        AT = "@WilliamsRacing"
    elif any(x in COMMENT[0].lower() for x in RUSSELLMATCHES):
        AT = "@GeorgeRussell63"
    elif any(x in COMMENT[0].lower() for x in MERCEDESMATCHES):
        AT = "@MercedesAMGF1"
    elif any(x in COMMENT[0].lower() for x in ALPINEMATCHES):
        AT = "@AlpineF1Team"
    elif any(x in COMMENT[0].lower() for x in ASTONMATCHES):
        AT = "@AstonMartinF1"
    elif any(x in COMMENT[0].lower() for x in FERRARIMATCHES):
        AT = "@ScuderiaFerrari"
    elif any(x in COMMENT[0].lower() for x in MCLARENMATCHES):
        AT = "@McLarenF1"
    elif any(x in COMMENT[0].lower() for x in ALFAMATCHES):
        AT = "@alfaromeoorlen"
    elif any(x in COMMENT[0].lower() for x in HAASMATCHES):
        AT = "@HaasF1Team"
    elif any(x in COMMENT[0].lower() for x in ALPHATMATCHES):
        AT = "@AlphaTauriF1"
    else:
        AT = randomat()
# Check for repetition
    with open("volume/" + "oldtweets.txt") as file:
        OLDTWEETS = file.read().splitlines()

    OLDTWEETFILE = open('volume/' + 'oldtweets.txt', 'a')
    TWEET = COMMENT[0] + " " + AT + " #F1"
    if COMMENT[1] not in OLDTWEETS and len(TWEET) < 280:
        api.update_status(TWEET)
        print("Tweeted: " + TWEET)
        OLDTWEETFILE.write(COMMENT[1] + "\n")
        OLDTWEETFILE.close()
    elif len(TWEET) > 280:
        print("Unable to tweet: " + TWEET)
        print("Tweet too long")
    elif COMMENT[1] in OLDTWEETS:
        print("Did not tweet: " + TWEET)
        print("Duplicate: " + COMMENT[1])
    else:
        print("Unknown error.")


try:
    while True:
        sendit()
        sleep(10800)
except KeyboardInterrupt:
    print("Interrupted!")

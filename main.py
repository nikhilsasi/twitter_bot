import tweepy, re, operator
import textblob
import paralleldots
from textblob import TextBlob
from paralleldots import set_api_key, sentiment
import nltk
from nltk.corpus import stopwords

# Authentication Consumer Key
CONSUMER_KEY = "89uJT3Ipc4SmJmHxqf6Omk4g6"
CONSUMER_SECRET = "	KnWLWEjISNupiso3HBl9ZuKFzq8gYuu2dv5geZgIEZZ4EwMigq"

# Authentication Access Tokens
ACCESS_TOKEN = "1361706008-UPdrAj7w70AMA6oZItR7yMbREQxZkEGgm9IZobS"
ACCESS_TOKEN_SECRET="30hPipvEw5WRFDSuvQvz9Fh7AgGIyiCtXCw4lnRzizedr"
#oauth handler
oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(oauth)
#######################################################################################################################
def getSearch():
    user_input = raw_input("Enter the query without Hashtag: ")

    hash_tag = "#" + user_input
    print(hash_tag)
    tweets = api.search(q=hash_tag, count=200)
    return tweets
##########################################################################################################################
def test_sentiments():
    list_sents = []
    tweets = getSearch()
    set_api_key("pIDFa4rmMonS93aFZ3ocGAW60ggqWnrhnhWsTzUtjAo")
    for tweet in tweets:
        list_sents.append(sentiment(tweet.text))
    return list_sents
######################################################################################################
def location():
    lang = {}
    loc = {}
    time = {}
    search = raw_input("Enter the query without the hashtag: ")
    hash_tag = "#" + search
    print(hash_tag)
    tweets = api.search(q=hash_tag, count=200)
    for tweet in tweets:
        if tweet.user.lang in lang.keys():
            lang[tweet.user.lang] += 1
        else:
            lang[tweet.user.lang] = 1

        if tweet.user.location in loc.keys():
            loc[tweet.user.location] += 1
        elif tweet.user.location != '':
            loc[tweet.user.location] = 1

        if tweet.user.time_zone in time.keys():
            time[str(tweet.user.time_zone)] += 1
        else:
            time[str(tweet.user.time_zone)] = 1

    top_location = sorted(loc, key=loc.get, reverse=True)
    top_timezones = sorted(time, key=time.get, reverse=True)
    top_lang = sorted(lang, key=lang.get, reverse=True)

    print("Top 5 Locations for this hashtag are:")
    i = 0
    for k in top_location[0:5]:
        i += 1
        print(i, k, loc[k])

    print("Top 5 timezones for this hashtag are:")
    i = 0
    for k in top_timezones[0:5]:
        i += 1
        print(i, k, time[k])
    i = 0
    print("Top 5 languages used:")
    for k in top_lang[0:5]:
        i += 1
        print(i, k, lang[k])
######################################################################################################
def tweet_match():
    trump = 0
    tweets = api.user_timeline(screen_name="@realdonaldtrump", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)   # Removing the URL texts
        if "India" in tweet_text or "INDIA" in tweet_text or "Bharat" in tweet_text or "Hindustan" in tweet_text or "india" in tweet_text:
            trump += 1

    modi = 0
    tweets = api.user_timeline(screen_name="@narendramodi", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)   # Removing the URL texts
        if "US" in tweet_text or "USA" in tweet_text or "America" in tweet_text or "United States Of America" in tweet_text or "america" in tweet_text:
            modi += 1

    # showing the comparison
    print("MOdi-" + str(modi))
    print("Trump-" + str(trump))
###################################################################################################################################################
def top_usage():

    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    dict = {}
    tweet_words = []
    tweet = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for x in tweet:
        y = x.full_text.split(" ")
        for z in y:
            tweet_words.append(z)
    for word in tweet_words:
        if word not in stop_words and "http" not in word:
            if word in dict.keys():
                dict[word] += 1
            else:
                dict[word] = 1

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    print("The Top Ten Words Are: ")
    for i in range(-1, -11, -1):
        print(sorted_dict[i][0], " - ", sorted_dict[i][1])

#################################################################################################################################################
def menu():
    show_menu = True
    menu_choices = """select an option from the given menu:  
     1.Check for the tweet
     2.Count number of followers
     3.Check sentiment level of the comment   
     4.Determine Location, Language, And Time Zone 
     5.Comparison Of the two Tweets
     6.Top Words Usage
     7.Tweet A Message
     8.Exit"""
    while show_menu:
        choice = input(menu_choices)  # getting the user choice

        #check for tweet
        if choice == "1":
            tweets = getSearch()   # getting the tweets from the other function
            print("Following tweets have been made by the people \n")
            for tweet in tweets:
                print(tweet.text)

        # Count number of followers
        elif choice == "2":
            tweets = getSearch()
            for tweet in tweets:
                print("User : %s \t Followers:%s " % (tweet.user.name, tweet.user.followers_count))
            print("\n")
            # check Sentiment level of comment
        elif choice == "3":
            list_sents = test_sentiments()
            p = 0
            n = 0
            nu = 0
            for x in list_sents:
                if x["sentiment"] == "neutral":
                    nu += 1
                elif x["sentiment"] == "negative":
                    n += 1
                elif x["sentiment"] == "positive":
                    p += 1
            print("Sentiment Result:\nWait for a minute(max 2 min xD)")
            print("Positive:%d \t Negative:%d \t Neutral:%d" % (p, n, nu))

        # Determine the location
        elif choice == "4":
            location()

        # Comparison of two tweets
        elif choice == "5":
            tweet_match()

        # Top Usage
        elif choice == "6":
            top_usage()

        # Tweet A Message
        elif choice == "7":
            status = input("Enter The Status update:")
            api.update_status(status)

        # Exit
        elif choice == "8":
            show_menu = False


menu()
import tweepy
import csv
# Twitter API credentials
consumer_key = 'UwJZUoWQCaMS3c1PXIi8qO2uQ'
consumer_secret = 'yf8uf1carejfVApWdqsREniY3plHqW4toXuejiddxkzIkOYkMN'
access_token = '366945338-P08Skpr8yQDmXayY4PRJCjOQYJFF90ZNO3ZGBVwm'
access_secret = 'goDJyRU4lLy5o5R4C2rH5raggIxQcf83n4zEC6FVosLRc'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
import time
# save our collecting tweets in the CSV file  :
def extractTweets(screen_name):
        for x in screen_name :
            result = tweepy.Cursor(api.search, q=x, lang="en", tweet_mode='extended').items(2000)
            nameOfThefile = str(screen_name) +'New.csv'
            with open('%s_tweets.csv' % screen_name, 'a') as file:
                writer = csv.writer(file)
                writer.writerow(["created_at", "id", "source" ,"text"])
                for tweet in result:
                    created_at = tweet.created_at
                    tweetID = tweet.id
                    full_text = withoutEmoj(tweet.full_text)
                    source = tweet.source
                    temp = [created_at, tweetID, source ,full_text]
                    writer.writerow(temp)
        pass

def withoutEmoj(text):
    returnString = ""
    for ch in text:
        try:
            ch.encode("ascii")
            returnString += ch
        except UnicodeEncodeError:
            returnString += ''
    return returnString

if __name__ == '__main__':

    list_of_key_first = ['gay', 'bitch', 'Emo', 'slut girl', 'slut', 'you ugly', 'ugly', 'nobody likes you', 'you are fat',
                   'hate you']
    extractTweets(list_of_key_first)
    time.sleep(900)

    list_of_key_secnd = ["loser", "fake", "fuck you", "stupid", "shut up", "kill you", "kill yourself", "weirdo",
                   "jerk", "you must die"]

    extractTweets(list_of_key_secnd)
    time.sleep(900)

    list_of_key_third = ["black girl", "brown girl", "shit"]
    extractTweets(list_of_key_third)



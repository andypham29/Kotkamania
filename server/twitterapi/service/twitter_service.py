import tweepy as tw

from server.twitterapi.model.twitter_tweet import Tweet
from setting import Setting


class TwitterService:
    consumer_key = Setting.CONSUMER_KEY
    consumer_secret = Setting.CONSUMER_SECRET
    access_token = Setting.ACCESS_TOKEN
    access_token_secret = Setting.ACCESS_TOKEN_SECRET

    def __init__(self):
        auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tw.API(auth, wait_on_rate_limit=True)

    def get_tweets_with_query(self, hashtag, count):
        tweepy_tweets = self.__get_tweets_with_query(hashtag, count)
        return [self.__convert_to_tweet_object(tweepy_tweet) for tweepy_tweet in tweepy_tweets]

    def get_tweets_by_user(self, user, count):
        tweepy_tweets = self.__get_tweets_by_user(user, count)
        return [self.__convert_to_tweet_object(tweepy_tweet) for tweepy_tweet in tweepy_tweets]

    def __get_tweets_with_query(self, search_words, count, date_since="2020-08-16"):
        return tw.Cursor(self.api.search,
                         q=search_words,
                         lang="en",
                         count=count,
                         since=date_since,
                         include_entities=True,
                         tweet_mode="extended").items(count)

    def __get_tweets_by_user(self, user, count, date_since="2020-08-16"):
        return self.api.user_timeline(
            screen_name=user,
            count=count,
            since=date_since,
            include_entities=True,
            tweet_mode="extended")

    @staticmethod
    def __convert_to_tweet_object(tweepy_tweet):
        text = tweepy_tweet.retweeted_status.full_text if hasattr(tweepy_tweet, "retweeted_status") else tweepy_tweet.full_text
        return Tweet(tweepy_tweet.author.screen_name, text, tweepy_tweet.created_at.strftime("%m/%d/%Y, %H:%M:%S"))


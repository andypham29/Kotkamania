from server.twitterapi.service.twitter_service import TwitterService


class TwitterServiceFacade:

    def __init__(self):
        self.twitter_service = TwitterService()

    def get_hockey_tweets(self):
        nhl_users = ["CapFriendly", "PuckReportNHL"]
        tweets = []

        tweets += self.__get_tweet_by_users(nhl_users)
        tweets.sort(key=lambda x: x.created_at, reverse=True)

        return tweets

    def __get_tweets_with_hashtags(self, hashtags, count=10):
        tweets = []
        for hashtag in hashtags:
            try:
                tweets += self.twitter_service.get_tweets_with_query(hashtag, count)
            except:
                raise Exception(f"Unable to retrieve tweet for hashtag \"{hashtag}\"")
        return tweets

    def __get_tweet_by_users(self, users, count=30):
        tweets = []
        for user in users:
            try:
                tweets += self.twitter_service.get_tweets_by_user(user, count)
            except:
                raise Exception(f"Unable to retrieve tweet for user \"{user}\"")
        return tweets

from server.twitterapi.model.twitter_tweet import Tweet
from server.twitterapi.service.facade.twitter_service_facade import TwitterServiceFacade


def test_get_tweets_with_query_then_return_tweets():
    tweets = TwitterServiceFacade().get_hockey_tweets()

    assert tweets is not None
    for tweet in tweets:
        assert type(tweet) is Tweet

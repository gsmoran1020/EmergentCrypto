import os
import tweepy
import data_hunter

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


def post_tweet():
    data = data_hunter.get_coin_data(5)

    token_content = [f"${data[i]['symbol'].upper()} {data[i]['name']} {data[i]['website']}" for i in range(len(data))]

    content = f"""Most recent tokens:
1. {token_content[0]}
2. {token_content[1]}
3. {token_content[2]}
4. {token_content[3]}
5. {token_content[4]}
#crypto #altcoin
    """

    api.update_status(content, card_uri='tombstone://card')


post_tweet()
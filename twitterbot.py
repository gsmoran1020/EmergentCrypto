import tweepy
import data_hunter

auth = tweepy.OAuthHandler('52kr4YqZRAoMknOS3mj2FAZsX', '3Kar3ZUJW3T5QQ0AIfq3SfuGHrK6trJJRC6kvwY63lCJChi6LH')
auth.set_access_token('1451325600858320904-NBHM5LRZEf39rXl6JnlWQcvHGb52si', 'kYfqKNcaleBdQqM1ndZ5FKAPMsLO54yqjPPThMHOagHaL')
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
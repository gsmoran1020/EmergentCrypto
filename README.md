# EmergentCrypto
The EmergentCrypto Bot project is a python script that manages a twitter account and makes posts about the latest crypto currencies being listed on https://www.coingecko.com/en for interested twitter users to stay up to date and see the latest tokens. 

## How It Works
The twitter bot begins with scraping the coingecko website's 'recently added' page in order to grab the five most recent crypto currency listings. After gathering this data the bot formats the data in an appropriate way to utilize the coingecko API. It will then make a request to the coingecko API for more information about the tokens that have been gathered by scraping. The bot takes this further information, formats it into content, checks length, and then checks to make sure it hasn't already made this exact post. If all these processes go through, the bot uses the tweepy module to interact with the twitter API and make a post to it's corresponding twitter account. 

The bot is hosted on Heroku and utilizes a built in Heroku module in order to run every hour, on the hour.

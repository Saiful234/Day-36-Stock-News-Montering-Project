import os
import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

twilio_account_sid = "AC54b0c580e051f106a1beb92bcfeb10d0"
twilio_auth_token = "96e20e75f26731c14818aa264f264985"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1:When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_api_key = "W4KLWXM5RBFPORML"
news_api_key = "20153cd172e14a4c90070566ed25e532"

parameter = {
    "function": 'TIME_SERIES_DAILY',
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,
}
endpoint_url = "https://www.alphavantage.co/query"
response = requests.get(endpoint_url, params=parameter)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]


yesterday_close = [value for (key, value) in stock_data.items()]
yesterday_close_last = yesterday_close[0]
yesterday_close_price = float(yesterday_close_last["4. close"])
print(yesterday_close_price)


day_before_close = float(yesterday_close[1]["4. close"])
print(day_before_close)

#Step 2:Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.

positive_Diff = yesterday_close_price-day_before_close

up_down = None
if positive_Diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percentage = round((positive_Diff/day_before_close)*100)


#Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
news_params = {
    "q": COMPANY_NAME,
    "apiKey": news_api_key,
}
if diff_percentage > 5:
    response = requests.get(NEWS_ENDPOINT, news_params)
    articles = response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)
    ## STEP 3:to send a separate message with each article's title and description to your phone number.


    formatted_news_list = [f"{STOCK_NAME}: {up_down}{diff_percentage}% \nHeadline: {article['title']}. " \
                           f"\nBrief: {article['description']}" for article in three_articles]

    client = Client(twilio_account_sid, twilio_auth_token)
    for article in formatted_news_list:
        message = client.messages.create(
            body=article,
            from_='+15017122661',
            to='+919489151903'
            )
        print(message.status)





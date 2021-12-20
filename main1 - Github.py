import requests
from twilio.rest import Client
import os

# stock_parameters setup
STOCK = "GME"
COMPANY_NAME = "GameStop"
API_KEY = os.environ.get("API_KEY")
FUNCTION = "TIME_SERIES_DAILY"
OUTPUTSIZE = "compact"
stock_parameters = {"function": FUNCTION, "symbol": STOCK, "outputsize": OUTPUTSIZE, "apikey": API_KEY}

# stock information setup
response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
response.raise_for_status()
info = response.json()
# key date name change everyday, NYSE not open everyday - easier to update and assign date variables
today = (list(info["Time Series (Daily)"])[0])
yesterday = (list(info["Time Series (Daily)"])[1])
# changed to float variables for simplicity
today_price = float(info["Time Series (Daily)"][today]["4. close"])
yesterday_price = float(info["Time Series (Daily)"][yesterday]["4. close"])

# check if significant change in stock price - used abs for simplicity (-5% or 5% both significant)
if int(abs((today_price - yesterday_price) / yesterday_price * 100)) > 5:
    print("get news")
    # News API
    NEWS_API = os.environ.get("NEWS_API")
    LANGUAGE = "en"
    news_parameters = {"apikey": NEWS_API, "language": LANGUAGE, "from_date": yesterday, "to_date": today, "q": STOCK or COMPANY_NAME}
    # limit of words for mobile is 160
    n = 155
    news_response = requests.get(url="https://newsdata.io/api/1/news", params=news_parameters)
    news_response.raise_for_status()
    news_info = news_response.json()
    content = (news_info["results"][0]["full_description"])
    gme_content = content.split(f"{COMPANY_NAME}", 2)
    out = [(gme_content[2][i:i+n]) for i in range(0, len(gme_content[2]), n)]
    text_message = (out[0] + "...")
    # twilio text message
    ACCOUNT_SID = "AC0329c5dd35b3a0ba313a23847a936369"
    AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    FROM = os.environ.get("SENDING_NUMBER")
    TO = os.environ.get("RECEIVING_NUMBER")
    message = client.messages.create(
        from_=FROM,
        to=TO,
        body=f"{text_message}"
    )
    print(message.status)

# stock_news_updater_V1
This app uses the Alphaadvantage API to compare the price of GME stock between yesterday and today. If there is an increase or decrease of 5%, then the app finds an article about the stock using the Newsdata API. Then using the Twilio API, 155 characters from the body of the article is emailed to a chosen phone number.  

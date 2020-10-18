# Abu
Financial chat bot leveraging BlackRock Aladdin API and Google Chat Bots

ABU:  Enhancing customer service and the financial acumen of our clients through their interaction with the Blackrock chatbot

<ins><b>INSPIRATION</b></ins>


In the Disney movie “Aladdin” the Kleptomaniacal monkey Abu is an inquisitive character. Hence, sticking with the Aladdin theme inspired from the name of the blackrock API we chose to name our chatbot 
PLEASE CHANGE THIS STUFF. I CANT THINK OF ANYTHING ELSE.

<ins><b>WHAT IT DOES</b></ins>

Abu helps users obtain vital information about the financial market and their portfolio while maintaining a human-like conversation experience. Some functionality of Abu include:
Portfolio Management:
Graphical and tabular representation of the customer’s portfolio.
Classification of portfolio in terms of security type and sector data.
Top and bottom performers in the portfolio.
Personalised information about specific securities within the portfolio.
Market Search:
Search the entire stock market based on tickers.
Provide top performers per sector in the stock market.
Overall market performance through S&P 500 and DOW indicators.
Custom Invest Portfolio:
Recommend stocks based on consumer goals.
Show top and bottom performers safe, medium, and risky stocks.

<ins><b>HOW WE BUILT IT</b></ins>

The back - end is built with python with the use of Numpy, Pandas, and matplotlib to generate custom graphs and tables. The heart of the back-end makes use  of the blackRock API in specific the performance data, portfolio analysis, and security search APIs. Furthermore we used the Alpha Vantage API to provide real-time data to the consumer and imgur API to transfer generated graphs from the back end to the front end. The front-end uses dialogflow hosted by google cloud to train a machine learning model through intent and entity  identification using natural language processing. We used to Flask to interact with the google cloud service.

<ins><b>CHALLENGES</b></ins>

It was difficult to get stock price data from the black rock API’s and hence we had to be creative and use different variables such as levels to calculate data that we wished to showcase.

<ins><b>ACCOMPLISHMENTS THAT WE ARE PROUD OF</b></ins>

The ability to integrate extended functionality of the financial market while delivering a very fun and rewarding user experience.

<ins><b>WHAT WE LEARNED</b></ins>

Blackrock APIs, Flask, Dialogflow, Github, Natural Language Processing, Financial knowledge

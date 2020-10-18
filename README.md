# Abu
Financial chat bot leveraging the BlackRock Aladdin API, the AlphaVantage API, and Google Chat Bots

ABU:  Enhancing customer service and the financial acumen of our clients through their interaction with the Blackrock chatbot


<ins><b>ABSTRACT</b></ins>
Our goal behind this project is to lower the cost of entry to financial markets by providing people with the tools and knowledge to make informed decisions with their money. Given the rise of chatbots, we felt that this was the best avenue allowing quick interactions and a direct flow of information to the user. We made many stylistic and design choices throughout our process to create a friendly, useful UI many of which you can see and experience. 



<ins><b>INSPIRATION</b></ins>
In the Disney movie “Aladdin” the Kleptomaniacal monkey Abu is an inquisitive character. Hence, sticking with the Aladdin theme inspired from the name of the blackrock API we chose to name our chatbot “Abu.”


<ins><b>WHAT IT DOES</b></ins>

Abu helps users obtain vital information about the financial market and their portfolio while maintaining a human-like conversation experience. Some functionality of Abu include:

<ol type="1">
  <li><b>Portfolio Management:</b></li>
  
  <span>&#8226;</span>Graphical and tabular representation of the customer’s portfolio.

  <span>&#8226;</span>Classification of portfolio in terms of security type and sector data.

  <span>&#8226;</span>Top and bottom performers in the portfolio.

  <span>&#8226;</span>Personalised information about specific securities within the portfolio.

  <li><b>Market Search:</b></li>
  
  <span>&#8226;</span>Search the entire stock market based on tickers.

  <span>&#8226;</span>Provide top performers per sector in the stock market.

  <span>&#8226;</span>Overall market performance through S&P 500 and DOW indicators.
  
  <li><b>Custom Investment Portfolio:</b></li>
  
  <span>&#8226;</span>Recommend stocks based on consumer goals.

  <span>&#8226;</span>Show top and bottom performers safe, medium, and risky stocks.
  
</ol>
<ins><b>HOW WE BUILT IT</b></ins>

The back - end is built with python with the use of Numpy, Pandas, and matplotlib to generate custom graphs and tables. The heart of the back-end makes use of the blackRock APIs, specifically the performance data, portfolio analysis, and security search APIs. Furthermore we used the Alpha Vantage API to provide real-time data to the consumer and imgur API to transfer generated graphs from the back end to the front end. The front-end uses dialogflow hosted by google cloud to train a machine learning model through intent and entity identification using natural language processing. The dialogue flow uses a webhook protocol to make JSON requests to our backend using Flask and Ngrok. These are processed in the backend and after gathering API information we make JSON responses back to Dialogflow. We chose to run our messaging on the platform Telegram as it’s simple UI and implementations made it powerful and practical. We have created a bot here which synchronously links to our Dialogflow.  

<ins><b>CHALLENGES</b></ins>

Some obstacles we ran into included getting stock price data from the Black Rock API’s, integrating an image posting API, and creating a webhook connection to allow our program to influence DialogFlow’s responses. We had to be creative and use different approaches to solve these challenges.We also ran into a difficult run timeout problem which caused problems when run with the Aladdin APIs.

<ins><b>ACCOMPLISHMENTS THAT WE ARE PROUD OF</b></ins>

We were very proud of our ability to troubleshoot many of the problems we faced. We collaborated effectively to come up with unique, easily-implementable solutions. For example, we troubleshooted our timeout problem by loading much of the data on-loading rather than when requested to ensure that we didn’t run into problems while the chatbot was operational. Additionally, we used other financial APIs to supplement and validate data that we got from the provided APIs. Most of all, we are proud of one another and our perseverance and ability to stand up to challenges rather than losing the will to continue, and we believe our final product exemplifies this resilient work ethic. 

<ins><b>WHAT WE LEARNED</b></ins>

Blackrock APIs, Flask, Dialogflow, Github, Natural Language Processing, Financial knowledge

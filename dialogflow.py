# import flask dependencies
from flask import Flask, request, make_response, jsonify, send_file
import json
import br_api_tests as br
import imgur as im
import securitySearch as ss
import plots as pl
import suggestions as sugg

# initialize the flask app
app = Flask(__name__)


# default route
@app.route('/')
def index():
    return 'Hello World!'



# function for responses
def results():
    risk = ''
    # build a request object given an action
    req = request.get_json(force=True)
    # gets the action from the JSON request
    action = req.get('queryResult').get('action')
    # if statement to choose response based on action
    print(action)
    if action == 'tick-search':
        # saves the parameter tick passed in the JSON request
        tick = req.get('queryResult').get('parameters').get('tick')
        # calls draw plot to re-write image 'searchedTicker.png'
        ss.drawTickerPlots(tick)

        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Here is {}'s performance: ".format(tick)
                        ]
                    },
                    "platform": "TELEGRAM"

                },
                {
                    "image": {
                        # uploads image using imgur and passed new URL
                        "imageUri": im.upload_image('Images/searchedTicker.png')
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "text": {
                        "text": [
                            "Enter another image or enter 'Main menu' to go to menu"
                        ]
                    },
                    "platform": "TELEGRAM"

                }
            ]
        }
    elif action == 'sector-search':
        # saves the parameter sector from the JSON request
        sector = req.get('queryResult').get('parameters').get('sector')
        # returns the dataframe for top performers in the sector
        txt = ss.drawSectorPlots(sector)
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            # string version of dataframe giving top 5 performers in given sector
                            txt
                        ]
                    },
                    "platform": "TELEGRAM"

                }
            ]
        }
    elif action == 'classify':
        # calls array of image URLs to return images
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Here is your breakdown by asset type: "
                        ]
                    },
                    "platform": "TELEGRAM"

                },
                {
                    "image": {

                        #"imageUri": "https://scontent-atl3-1.xx.fbcdn.net/v/t1.0-9/117774336_1044925022589847_8385272999349051066_n.jpg?_nc_cat=106&_nc_sid=85a577&_nc_ohc=J0wuYDR4fbYAX-U8UoN&_nc_ht=scontent-atl3-1.xx&oh=174104f237bbd56f3c35ff28b8120d92&oe=5FAF8958"
                        "imageUri": photos[0]
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "text": {
                        "text": [
                            "Here is the breakdown by sector: "
                        ]
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "image": {

                        #"imageUri": "https://i.imgur.com/B0r0aDA.png"
                        "imageUri": photos[2]
                    },
                    "platform": "TELEGRAM"
                }
            ],
            "fulfillmentText": "Happy to help :)"
        }
    elif action == 'high-low':
        # returns JSON response with text object full of highest and lowest performers
        return {'fulfillmentText': '{}\n\n {}'.format(perf, sec)}
    elif action == 'portfolio':
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Here are historical returns from your portfolio "
                        ]
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "image": {

                         # "imageUri": "https://i.imgur.com/B0r0aDA.png"
                         "imageUri": photos[3]
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "text": {
                        "text": [
                            table
                        ]
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "text": {
                        "text": [
                            "\nWould you like to search a particular asset, see top performers, or view your portfolio "
                            "classified? "
                        ]
                    },
                    "platform": "TELEGRAM"
                },

            ]
        }
    elif action == "marketData":
        # returns plots for DOW and S&P 500, indicative of marker strength
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Here is the Dow's Performance over Time: "
                        ]
                    },
                    "platform": "TELEGRAM"

                },
                {
                    "image": {
                        # "imageUri": "https://i.imgur.com/B0r0aDA.png"
                        "imageUri": photos[4]
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "text": {
                        "text": [
                            "Here is S&P's Performance: "
                        ]
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "image": {
                        #"imageUri": "https://i.imgur.com/B0r0aDA.png"
                        "imageUri": photos[5]
                    },
                    "platform": "TELEGRAM"
                },
            ],

        }
    elif action == "asset":
        # saves parameter ticker from JSON request
        sym = req.get('queryResult').get('parameters').get('ticker')
        # calls plots to get data for specific asset
        return {'fulfillmentText': pl.portfolioSpecificData(sym) + '\nEnter another ticker or "Main Menu" to go back to menu'}
    elif action == "poojan":
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "ooooo Pooojannnn"
                        ]
                    },
                    "platform": "TELEGRAM"

                },
                {
                    "image": {
                        "imageUri": "https://scontent-atl3-1.xx.fbcdn.net/v/t1.0-9/117774336_1044925022589847_8385272999349051066_n.jpg?_nc_cat=106&_nc_sid=85a577&_nc_ohc=J0wuYDR4fbYAX-U8UoN&_nc_ht=scontent-atl3-1.xx&oh=174104f237bbd56f3c35ff28b8120d92&oe=5FAF8958"
                       # "imageUri": photos[4]
                    },
                    "platform": "TELEGRAM"
                },

            ],

        }
    elif action == "suggest":
        risk = req.get('queryResult').get('parameters').get('risk').strip().lower()
        sect = req.get('queryResult').get('parameters').get('sector')
        # txt = 'Given your desire to take {} risk in the given sectors, we suggest these options: \n'.format(risk)
        if len(sect) > 0:
            txt = '\n'.join(sugg.generateSuggestions(risk, sect))
        else:
            txt = '\n'.join(sugg.generateSuggestions(risk))
        return {'fulfillmentText': txt}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


# run the app
if __name__ == '__main__':
    [perf, sec] = br.get_both()
    table = pl.tablePortfolio()
    photos = im.upload_all()
    app.run()

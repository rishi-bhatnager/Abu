# import flask dependencies
from flask import Flask, request, make_response, jsonify, send_file
import json
import br_api_tests as br
import imgur as im
import securitySearch as ss

# initialize the flask app
app = Flask(__name__)


# default route
@app.route('/')
def index():
    return 'Hello World!'


# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    print(action)
    if action == 'tick-search':
        tick = req.get('queryResult').get('parameters').get('tick')
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
                        "imageUri": im.upload_image('searchedTicker.png')
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "text": {
                        "text": [
                            "Enter another or enter 'Main menu' to return"
                        ]
                    },
                    "platform": "TELEGRAM"

                }
        ]
        }
    elif action == 'sector-search':
        sector = req.get('queryResult').get('parameters').get('sector')
        txt = ss.drawSectorPlots(sector)
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            txt
                        ]
                    },
                    "platform": "TELEGRAM"

                },
                {
                    "image": {
                        #"imageUri": im.upload_image('sectorPerformers.png')
                    },
                    "platform": "TELEGRAM"
                }
            ]
        }
    elif action == 'classify':
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

                        "imageUri": "https://i.imgur.com/B0r0aDA.png"

                        #"imageUri": photos[0]
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

                        "imageUri": "https://i.imgur.com/B0r0aDA.png"
          #"imageUri": photos[1]
                    },
                    "platform": "TELEGRAM"
                }
            ],
            "fulfillmentText": "Happy to help :)"
        }
    elif action == 'high-low':
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

                        "imageUri": "https://i.imgur.com/B0r0aDA.png"

                        #"imageUri": photos[3]
                    },
                    "platform": "TELEGRAM"
                },
                {
                    "text": {
                        "text": [
                            "Would you like to search a particular asset, see top performers, or view your portfolio "
                            "classified? "
                        ]
                    },
                    "platform": "TELEGRAM"
                },

            ]
        }

    elif action == "marketData":
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
                        "imageUri": "https://i.imgur.com/B0r0aDA.png"
                        #"imageUri": photos[4]
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
                        "imageUri": "https://i.imgur.com/B0r0aDA.png"
                        #"imageUri": photos[5]
                    },
                    "platform": "TELEGRAM"
                }
            ],
            "fulfillmentText": "Happy to help :)"
        }
        pass
    elif action == "asset":
        sym = req.get('queryResult').get('parameters').get('ticker')
        return {'fulfillmentText': 'You do not own {}'.format(sym)}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


# run the app
if __name__ == '__main__':
    [perf, sec] = br.get_both()
    # photos = im.upload_all()
    app.run()

# import flask dependencies
from flask import Flask, request, make_response, jsonify, send_file
import json
import br_api_tests as br


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
        print(tick)
        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": "Here's data for {}".format(tick)
                                }
                            },
                            {
                                "basicCard": {
                                    "title": "Showing  data for {}".format(tick),
                                    "formattedText": "This is a basic card.  Text in a basic card can include \"quotes\" and\n    most other unicode characters including emojis.  Basic cards also support\n    some markdown formatting like *emphasis* or _italics_, **strong** or\n    __bold__, and ***bold itallic*** or ___strong emphasis___ as well as other\n    things like line  \nbreaks",
                                    "image": {
                                        "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                                        "accessibilityText": "Image alternate text"
                                    },

                                    "imageDisplayOptions": "CROPPED"
                                }
                            },
                            {
                                "simpleResponse": {
                                    "textToSpeech": "Which response would you like to see next?"
                                }
                            }
                        ]
                    }
                }
            }
        }
    elif action == 'sector-search':
        sector = req.get('queryResult').get('parameters').get('sector')
        return {'fulfillmentText': 'Sector: {}'.format(sector)}
    elif action == 'classification':
        # fndsljfs
        pass
    elif action == 'high-low':
        return {'fulfillmentText': 'Here is your portfolio\n Would you like to see your top performers or a more advanced breakdown?'}
    elif action == 'portfolio':
        return {'fulfillmentText': 'Sector: {}'.format("fdsf")}
    elif action == "marketData":
        # show market data
        pass


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


# run the app
if __name__ == '__main__':
    txt = br.get_rank()
    app.run()


# import flask dependencies
from flask import Flask, request, make_response, jsonify

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
    if (action == 'tick-search'):
        tick = req.get('queryResult').get('parameters').get('tick')
        return {'fulfillmentText': 'Symbol: {}'.format(tick)}
    elif (action == 'sector-search'):
        sector = req.get('queryResult').get('parameters').get('sector')
        return {'fulfillmentText': 'Sector: {}'.format(sector)}
    elif(action == 'classification'):
        #classification image
        pass
    elif(action == 'high-low'):
        #high low image generation
        pass
    elif(action == 'portfolio'):
        #current portfolio image
        pass


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()
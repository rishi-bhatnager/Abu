import os
import json
import urllib
from flask import (Flask, request, make_response)

app = Flask(__name__)


@app.route('/')
def hello():
    return "hello world!"


if __name__ == "__main__":
    app.run()

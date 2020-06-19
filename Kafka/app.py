from flask import Flask, render_template, make_response
from Consumer import stock_prediction
import json
from datetime import datetime
import time

# creating flask application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# url data to get data on index page
@app.route('/data')
def data():
    stock_price, close_price, date_time = stock_prediction()

    date_time = int(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').strftime('%s')) * 1000

    data = [date_time, stock_price, close_price]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    time.sleep(2)
    return response


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000, passthrough_errors=True)
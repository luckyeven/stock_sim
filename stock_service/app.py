from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from graphene import ObjectType, String, Int, List, Float, Field, Schema
import threading
import random
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# mock data
stocks = [
    {
        "name": "Alpha Corporation",
        "ticker": "ALPHA",
        "price": 152.30,
        "historical_prices": [152.30, 153.20, 150.10, 155.50, 148.75],
        "highest_price": 155.50,
        "lowest_price": 148.75,
        "trading_volume": 10000,
        "current_price": 152.30,
    },
    {
        "name": "Beta Enterprises",
        "ticker": "BETA",
        "price": 97.85,
        "historical_prices": [97.85, 98.20, 96.75, 99.10, 95.60],
        "highest_price": 99.10,
        "lowest_price": 95.60,
        "trading_volume": 8000,
        "current_price": 97.85,
    },
    {
        "name": "Gamma Industries",
        "ticker": "GAMMA",
        "price": 223.74,
        "historical_prices": [223.74, 224.20, 222.50, 227.30, 221.90],
        "highest_price": 227.30,
        "lowest_price": 221.90,
        "trading_volume": 12000,
        "current_price": 223.74,
    },
    {
        "name": "Delta Services",
        "ticker": "DELTA",
        "price": 542.67,
        "historical_prices": [542.67, 545.30, 540.90, 548.20, 539.75],
        "highest_price": 548.20,
        "lowest_price": 539.75,
        "trading_volume": 15000,
        "current_price": 542.67,
    },
    {
        "name": "Epsilon Group",
        "ticker": "EPSLN",
        "price": 321.40,
        "historical_prices": [321.40, 323.10, 318.90, 326.50, 317.80],
        "highest_price": 326.50,
        "lowest_price": 317.80,
        "trading_volume": 11000,
        "current_price": 321.40,
    },
]


class StockType(ObjectType):
    name = String()
    ticker = String()
    price = Float()
    historical_prices = List(Float)
    highest_price = Float()
    lowest_price = Float()
    trading_volume = Int()
    current_price = Float()


class Query(ObjectType):
    stock = Field(StockType, ticker=String(required=True))

    def resolve_stock(self, info, ticker):
        for stock in stocks:
            if stock["ticker"] == ticker:
                return stock
        return None


schema = Schema(query=Query)


@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    query = data.get('query')
    result = schema.execute(query)
    return jsonify(result.data)


@app.route('/api/stocks', methods=['POST'])
def add_stock():
    stock_data = request.get_json()
    ticker = stock_data.get('ticker')
    name = stock_data.get('name')
    price = stock_data.get('price')    

    # Add new stock
    new_stock = {
        'name': name,
        'ticker': ticker,
        'price': price
    }
    stocks.append(new_stock)

    return jsonify(new_stock), 201


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'stocks API alive'})


@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    return jsonify(stocks)

@app.route('/api/stock/<string:ticker>', methods=['GET'])
def get_stock_by_ticker(ticker):
    for stock in stocks:
        if stock["ticker"] == ticker:
            return jsonify(stock)
    return jsonify({'message': 'stock not found'}), 404

def update_current_price():
    while True:
        for stock in stocks:

            price_change = random.uniform(-5.0, 5.0)
            stock["current_price"] += price_change
            time.sleep(0.1)
            emit_stock_update(stock)


update_thread = threading.Thread(target=update_current_price)
update_thread.daemon = True
update_thread.start()


def emit_stock_update(stock):
    socketio.emit("stock_update", {
        "ticker": stock["ticker"],
        "current_price": stock["current_price"],
    })


@socketio.on('connect')
def handle_connect():
    print('Client connected')


if __name__ == '__main__':
    socketio.run(app, debug=True)

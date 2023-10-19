from flask import Flask, request, jsonify

app = Flask(__name__)

# mock data
stocks = [
    {"name": "Alpha Corporation", "ticker": "ALPHA", "price": 152.30},
    {"name": "Beta Enterprises", "ticker": "BETA", "price": 97.85},
    {"name": "Gamma Industries", "ticker": "GAMMA", "price": 223.74},
    {"name": "Delta Services", "ticker": "DELTA", "price": 542.67},
    {"name": "Epsilon Group", "ticker": "EPSLN", "price": 321.40},
]


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


if __name__ == '__main__':
    app.run(debug=True)

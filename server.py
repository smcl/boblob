#!flask/bin/python
from flask import Flask
import logging
from order_book import OrderBook
from order import Order
import json

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

order_book = OrderBook()

@app.route('/')
def index():
    return "Hello, World!"

@app.route("/buy/<quantity>/<instrumentCode>/<price>")
@app.route("/buy/<quantity>/<instrumentCode>")
def buy(quantity, instrumentCode, price=None):
    order = Order("buy", quantity, instrumentCode, price)
    if (price):
        print("LIMIT BUY %s %s @ %s" % (quantity, instrumentCode, price))
    else:
        print("MARKET BUY %s %s" % (quantity, instrumentCode))
    if order_book.add(order):
        return "OK"
    return "NO MATCH"

@app.route("/sell/<quantity>/<instrumentCode>/<price>")
@app.route("/sell/<quantity>/<instrumentCode>")
def sell(quantity, instrumentCode, price=None):
    order = Order("buy", quantity, instrumentCode, price)
    if (price):
        print("LIMIT SELL %s %s @ %s" % (quantity, instrumentCode, price))
    else:
        print("MARKET SELL %s %s" % (quantity, instrumentCode))
    if order_book.add(order):
        return "OK"
    return "NO MATCH"

@app.route("/whole_book")
def whole_book():
    return order_book.toJson()

@app.route("/book_info")
def book_info():
    orders = [ (ins, len(order_book.book[ins])) for ins in order_book.book.keys() ]
    return json.dumps({
        "num_instruments": len(order_book.book.keys()),
        "total_num_orders": sum([ o[1] for o in orders ]),
        "num_orders_by_ins": [ o[0]+":"+str(o[1]) for o in orders ]
    })

if __name__ == '__main__':
    app.run(debug=True)

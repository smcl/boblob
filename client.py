import os
import requests
import random
import time
from order import Order

max_quantity = 100
max_price = 10

number_of_children = 40
number_of_orders = 1000
number_of_instruments = 5

def random_char():
    return chr(int(ord("A") + 26 * random.random()))

def generate_instruments():
    instruments = []
    for x in range(number_of_instruments):
        instruments.append("".join([
            random_char(),
            random_char(),
            random_char(),
            random_char()
        ]))
    return instruments

def generate_test_orders(instruments):
    orders = []

    for idx in range(number_of_children * number_of_orders):
        instrument_code = random.choice(instruments)
        quantity = int(random.random() * max_quantity)
        buy_sell = random.choice(["buy", "sell"])
        if random.random() > 0.9:
            price = random.random() * max_price
            orders.append(Order(buy_sell, quantity, instrument_code, price))
        else:
            orders.append(Order(buy_sell, quantity, instrument_code))

    return orders


def client(orders):
    times = []

    for o in orders:
        before = time.time()
        resp = None
        if o.price:
            resp = requests.get("http://localhost:5000/%s/%d/%s/%f" % (o.buy_sell, o.quantity, o.instrument_code, o.price))
        else:
            resp = requests.get("http://localhost:5000/%s/%d/%s" % (o.buy_sell, o.quantity, o.instrument_code))
        print(resp.text)
        after = time.time()
        times.append(after - before)

    print("avg: %d ms" % int(1000 * (sum(times)/len(times))))
    os._exit(0)

def main():
    print("parent: %d" % os.getpid())
    print("spawning %d children" % number_of_children)

    instruments = generate_instruments()
    orders = generate_test_orders(instruments)

    for x in range(number_of_children):
      newpid = os.fork()
      if newpid == 0:
          client(orders[x*number_of_orders : (x+1) *  number_of_orders])

main()

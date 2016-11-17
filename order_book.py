import json
from order import Order


class OrderBook(object):
    def __init__(self):
        self.book = {}
        pass

    def try_match(self, order):
        for i, limit_order in enumerate(self.book[order.instrument_code]):
            if (order.quantity >= limit_order.quantity):
                continue

            if ((order.price and order.can_match(limit_order))
                or not order.price):
                    return i
        return -1

    def match(self, order, order_idx):
        limit_order = self.book[instrument_code][order_idx]
        limit_order.quantity -= order.quantity
        if limit_order.quantity == 0:
            del(self.book[order.instrument_code][order_idx])

    def add(self, order):
        if order.instrument_code in self.book.keys():
            order_idx = self.try_match(order)
            if order_idx > 0:
                match(order, order_idx)
                return True
            elif order.price:
                self.book[order.instrument_code].append(order)
                return True
        else:
            if order.price:
                self.book[order.instrument_code] = [ order ]
                return True
        return False

    def toJson(self):
        json_obj = {}

        for instrument_code in self.book.keys():
            json_obj[instrument_code] = [ o.toJson() for o in self.book[instrument_code] ]

        return json.dumps(json_obj)

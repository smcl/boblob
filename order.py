class Order(object):
    def __init__(self, buy_sell, quantity, instrument_code, price=None):
        self.buy_sell = buy_sell
        self.quantity = quantity
        self.instrument_code = instrument_code
        self.price = price

    def can_match(self, limit_order):
        return (self.buy_sell != limit_order.buy_sell
                and (
                    (self.buy_sell == "buy" and self.price >= limit_order.price)
                    or (self.buy_sell == "sell" and self.price <= limit_order.price)
                ))

    def toJson(self):
        return {
            "buy_sell": self.buy_sell,
            "quantity": self.quantity,
            "instrument_code": self.instrument_code,
            "price": self.price
        }

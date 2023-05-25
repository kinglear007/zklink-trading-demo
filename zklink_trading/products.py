#!/usr/bin/env python
# encoding: utf-8


class Product(object):
    def __init__(self, product_id: str, base_scale: int, quote_scale: int):
        l = product_id.split("-")
        assert (len(l) == 2)
        self.product_id = product_id
        self.base_currency = l[0]
        self.base_scale = base_scale
        self.quote_currency = l[1]
        self.quote_scale = quote_scale


trading_products = [
    Product("wETH-USD", -14, -16),
    Product("wBTC-USD", -13, -16),
    Product("wMATIC-USD", -17, -14),
    Product("wAVAX-USD", -16, -16),
]

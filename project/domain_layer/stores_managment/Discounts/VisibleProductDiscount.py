from project.domain_layer.stores_managment import Product
from project.domain_layer.stores_managment.Discounts.DiscountPolicy import Discount
from datetime import date, datetime


class VisibleProductDiscount(Discount):
    def __init__(self, start_date, end_date, percent):
        super().__init__(start_date, end_date, percent)
        self.products_in_discount = {}  # {product_name: bool}

    def commit_discount(self, product_price_dict: dict):  # {product_name, (Product, amount, updated_price, original)}

        if self.start < datetime.today() < self.end:
            for product_name in product_price_dict.keys():
                product_tup = product_price_dict[product_name]

                if product_name in self.products_in_discount.keys():
                    new_product_tup = (self.get_product_object(product_tup), self.get_product_amount(product_tup),
                                       self.get_product_updated_price(product_tup, self.discount), self.get_product_object(product_tup).original_price * self.get_product_amount(product_tup))
                    product_price_dict[product_name] = new_product_tup #(self.discount * self.get_product_object(product_tup).original_price * self.get_product_amount(product_tup))
                    x=5

    def get_product_object(self, product):
        return product[0]

    def get_product_amount(self, product):
        return product[1]

    def get_product_updated_price(self, product, discount):
        new_price = product[2] - (self.discount * self.get_product_object(product).original_price * self.get_product_amount(product))
        return new_price

    def undu_discount(self):
        for product in self.products_in_discount.keys():
            if self.products_in_discount[product]:  # already comitted discount
                product.price_after_discounts += product.original_price * self.discount
                product.price_after_discounts = min(product.price_after_discounts, product.original_price)

    def is_valid_start_date(self, _date):
        super().is_valid_start_date(_date)

    def is_valid_end_date(self, end_date):
        super().is_valid_end_date(end_date)

    def is_valid_percent(self, percent):
        super().is_valid_percent(percent)

    def is_approved(self, original_price, amount):
        pass

    def edit_discount(self, start_date=None, end_date=None, percent=None):
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and is_valid_start_date(start_date):
            self.start = start_date
        if end_date is not None and is_valid_end_date(end_date):
            self.end = end_date
        if percent is not None and is_valid_percent(percent):
            self.discount = 1 - percent / 100

    def add_products(self, product: Product):
        self.products_in_discount[product] = False

    def remove_product(self, product: Product):
        if self.products_in_discount[product]:
            product.price_after_discounts += product.original_price * self.discount
            product.price_after_discounts = min(product.price_after_discounts, product.original_price)
        self.products_in_discount.pop(product)

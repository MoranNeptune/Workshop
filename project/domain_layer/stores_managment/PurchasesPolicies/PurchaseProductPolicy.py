from project.domain_layer.stores_managment.PurchasesPolicies.PurchasePolicy import PurchasePolicy


class PurchaseProductPolicy(PurchasePolicy):
    def __init__(self, min_amount_products, max_amount_products, id):
        super().__init__()
        self.min_amount_products = min_amount_products
        self.max_amount_products = max_amount_products
        self.id = id
        self.products_int_policy = {}  # {product_name, bool}
        self.MAX_SIZE = 100000
        self.MIN_SIZE = 0

    def is_approved(self, product_price_dict: dict):    # {product_name, (Product, amount, updated_price, original)}
        outcome_description = ""
        is_approved = True
        for product_name in product_price_dict.keys():
            product_tup = product_price_dict[product_name]
            if not self.min_amount_products <= self.get_product_amount(product_tup) <= self.max_amount_products:
                outcome_description = outcome_description + (self.add_fail_description(product_name, self.get_product_amount(product_tup)))
                is_approved = False
        return is_approved, outcome_description

    def get_product_object(self, product):
        return product[0]

    def get_product_amount(self, product):
        return product[1]

    def add_fail_description(self, product_name: str, product_amount: int):
        min_string = ""
        max_string = ""
        if self.min_amount_products == self.MIN_SIZE:
            min_string = "no min limit"
        else:
            min_string = str(self.min_amount_products)

        if self.min_amount_products == self.MAX_SIZE:
            max_string = "no max limit"
        else:
            max_string = str(self.max_amount_products)

        desc = "{} can only be purchased in amount of minimum {} and maximum {} units, and you tried {}!\n".format\
            (product_name, min_string, max_string, str(product_amount))
        return desc

    def add_product(self, product_name: str):
        self.products_int_policy[product_name] = True
        return True

    def remove_product(self, product_name):
        if product_name in self.products_int_policy.keys():
            del self.products_int_policy[product_name]
            return True
        return False
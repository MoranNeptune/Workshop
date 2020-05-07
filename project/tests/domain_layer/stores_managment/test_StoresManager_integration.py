import datetime
import unittest

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies.VisibleProductDiscount import VisibleProductDiscount
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.users_managment.Basket import Basket
from project.domain_layer.users_managment.Cart import Cart


class test_StoresManager(unittest.TestCase):
    def setUp(self) -> None:
        self.store_manager = StoresManager()
        self.idx = 0
        self.store_id = self.store_manager.open_store("test store", "test owner")
        self.products = [
            ("t-shirt", 20, ["cloth"], ["green"], 7),
            ("apple", 1, ["food", "green"], ["vegetable"], 10),
            ("orange", 1, ["food", "orange"], ["fruits"], 10),
            ("iphone", 5000, ["electronics", "bad and expensive phone "], ["fruits"], 10)
        ]

        self.store_manager.get_store(self.store_id).inventory.products = {"Apple": Product("Apple", 20, ["Food"], ["Fruits"], 10),
                                         "Banana": Product("Banana", 20, ["Food"], ["Fruits"], 10),
                                         "Orange": Product("Orange", 20, ["Food"], ["Fruits"], 10),
                                         "Tomato": Product("Tomato", 20, ["Food"], ["Vegetables"], 10),
                                         "Cucumber": Product("Cucumber", 20, ["Food"], ["Vegetables"], 10),
                                         "Carrot": Product("Carrot", 20, ["Food"], ["Vegetables"], 10),
                                         "Iphone": Product("Iphone", 20, ["Electronics"], ["Computers"], 10),
                                         "Hard Disk": Product("Hard Disk", 20, ["Electronics"], ["Computers"], 10),
                                         "Keyboard": Product("Keyboard", 20, ["Electronics"], ["Computers"], 10)}

        self.discount = VisibleProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 10)
        self.discount1 = VisibleProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 30)

        self.store_manager.get_store(self.store_id).discounts[self.discount.id] = self.discount
        self.store_manager.get_store(self.store_id).discounts[self.discount1.id] = self.discount1

        self.discount.products_in_discount["Apple"] = self.store_manager.get_store(self.store_id).inventory.products["Apple"]
        self.discount.products_in_discount["Tomato"] = self.store_manager.get_store(self.store_id).inventory.products["Tomato"]
        self.discount1.products_in_discount["Apple"] = self.store_manager.get_store(self.store_id).inventory.products["Apple"]
        self.discount.products_in_discount["Carrot"] = self.store_manager.get_store(self.store_id).inventory.products["Carrot"]
        self.discount.products_in_discount["Keyboard"] = self.store_manager.get_store(self.store_id).inventory.products["Keyboard"]

        self.basket = Basket(self.store_manager.get_store(self.store_id).store_id)
        self.basket.products["Apple"] = (self.store_manager.get_store(self.store_id).inventory.products["Apple"], 10)
        self.basket.products["Keyboard"] = (self.store_manager.get_store(self.store_id).inventory.products["Keyboard"], 5)
        self.basket.products["Carrot"] = (self.store_manager.get_store(self.store_id).inventory.products["Carrot"], 1)

    def test_update_product(self):
        self.test_add_product_to_store()
        # check regular update

        for attribute, value in Product(self.products[-1][0], 20, ["not so expensive now"], ["electronics"],
                                        1).__dict__.items():
            if attribute != "discount":
                self.assertTrue(
                    self.store_manager.update_product(self.idx - 1, "moshe" + str(self.idx - 1), self.products[-1][0],
                                                      attribute,
                                                      value))

                self.assertEqual(
                    self.store_manager.stores.get(self.idx - 1).inventory.products.get(
                        self.products[-1][0]).__getattribute__(attribute),
                    value)

        # update without permissions
        self.assertFalse(
            self.store_manager.update_product(self.idx - 1, "not moshe", self.products[-1][0],
                                              "price",
                                              73))

    def test_search(self):
        self.test_add_product_to_store()
        # regular search
        self.assertIn(self.idx - 1, self.store_manager.search("iphone").keys())

        # by category
        self.assertIn(self.idx - 2, self.store_manager.search("", categories=["food"]).keys())
        self.assertIn(self.idx - 3, self.store_manager.search("", categories=["food"]).keys())

        # by key words

        self.assertIn(self.idx - 1, self.store_manager.search("", key_words=["fruits"]).keys())
        self.assertIn(self.idx - 2, self.store_manager.search("", key_words=["fruits"]).keys())
        self.assertNotIn(self.idx - 3, self.store_manager.search("", key_words=["fruits"]).keys())

        # search for non - existing product
        self.assertTrue(len(self.store_manager.search("not real product")) == 0)

    def test_add_product_to_store(self):
        # check when store does not exit
        self.assertFalse(self.store_manager.add_product_to_store(-1, "moshe", "p", 1, "s", "e", 10))

        # add some products
        for product in self.products:
            self.test_open_store()
            self.assertTrue(
                self.store_manager.add_product_to_store(self.idx - 1, "moshe" + str(self.idx - 1), *product))
            # check if added successfully
            self.assertIn(product[0], self.store_manager.get_store(self.idx - 1).inventory.products.keys())

        # check add product without permission
        product = self.products[0]
        self.assertFalse(
            self.store_manager.add_product_to_store(self.idx - 1, "not moshe" + str(self.idx - 1), *product))

    def test_appoint_manager_to_store(self):
        self.test_open_store()
        self.assertFalse(self.store_manager.appoint_manager_to_store(self.idx + 1, "moshe" + str(self.idx - 1), "Amit"))
        self.assertTrue(self.store_manager.appoint_manager_to_store(self.idx - 1, "moshe" + str(self.idx - 1), "Amit"))
        self.assertIn("Amit", self.store_manager.get_store(self.idx - 1).store_managers.keys())
        self.assertFalse(
            self.store_manager.appoint_manager_to_store(self.idx - 1, "not moshe" + str(self.idx - 1), "Amit"))

    def test_appoint_owner_to_store(self):
        self.test_open_store()
        self.assertFalse(self.store_manager.appoint_owner_to_store(self.idx + 1, "moshe" + str(self.idx - 1), "Amit"))
        self.assertTrue(self.store_manager.appoint_owner_to_store(self.idx - 1, "moshe" + str(self.idx - 1), "Amit"))
        self.assertIn("Amit", self.store_manager.get_store(self.idx - 1).store_owners)
        self.assertFalse(
            self.store_manager.appoint_owner_to_store(self.idx - 1, "not moshe" + str(self.idx - 1), "Amit"))

    def test_remove_manager_from_store(self):
        self.test_appoint_manager_to_store()
        # not real store
        self.assertFalse(self.store_manager.remove_manager(self.idx + 1, "moshe" + str(self.idx - 1), "Amit"))
        self.assertTrue(self.store_manager.remove_manager(self.idx - 1, "moshe" + str(self.idx - 1), "Amit"))

    def test_remove_owner_from_store(self):
        self.test_appoint_owner_to_store()
        # not real store
        self.assertFalse(self.store_manager.remove_owner(self.idx + 1, "moshe" + str(self.idx - 1), "Amit"))
        self.assertTrue(self.store_manager.remove_owner(self.idx - 1, "moshe" + str(self.idx - 1), "Amit"))

    def test_add_permission_to_manager_in_store(self):
        self.test_appoint_manager_to_store()
        # not real store
        self.assertFalse(
            self.store_manager.add_permission_to_manager_in_store(self.idx + 1, "moshe" + str(self.idx - 1), "Amit",
                                                                  "add_product"))
        self.assertTrue(
            self.store_manager.add_permission_to_manager_in_store(self.idx - 1, "moshe" + str(self.idx - 1), "Amit",
                                                                  "add_product"))
        self.assertIn(Store.add_product, self.store_manager.get_store(self.idx - 1).store_managers.get("Amit"))

        self.assertFalse(
            self.store_manager.add_permission_to_manager_in_store(self.idx - 1, "not moshe" + str(self.idx - 1), "Amit",
                                                                  "add_product"))

    def test_remove_permission_from_manager_in_store(self):
        self.test_add_permission_to_manager_in_store()
        # not real store
        self.assertFalse(
            self.store_manager.remove_permission_from_manager_in_store(self.idx + 1, "moshe" + str(self.idx - 1),
                                                                       "Amit",
                                                                       "add_product"))
        self.assertTrue(
            self.store_manager.remove_permission_from_manager_in_store(self.idx - 1, "moshe" + str(self.idx - 1),
                                                                       "Amit",
                                                                       "add_product"))
        self.assertNotIn(Store.add_product, self.store_manager.get_store(self.idx - 1).store_managers.get("Amit"))

    def test_add_purchase_to_store(self):
        self.test_add_product_to_store()
        purchase = Purchase({self.products[-1][0]: (Product(*self.products[-1]), 2)}, "moshe", self.idx - 1, 0)
        self.assertTrue(self.store_manager.add_purchase_to_store(self.idx - 1, purchase))
        self.assertFalse(self.store_manager.add_purchase_to_store(self.idx + 1, purchase))

    def test_open_store(self):
        self.assertEqual(self.idx,
                         self.store_manager.open_store("moshe" + str(self.idx), "moshe's store" + str(self.idx)))

        self.assertIn(self.idx, self.store_manager.stores.keys())
        self.idx += 1

    def test_buy(self):
        self.test_add_product_to_store()
        cart = Cart()
        cart.baskets = {self.idx - 1: Basket(self.idx - 1)}
        cart.get_basket(self.idx - 1).add_product(Product(*self.products[-1]), 2)
        self.assertTrue(self.store_manager.buy(cart))
        cart = Cart()
        cart.baskets = {self.idx + 1: Basket(self.idx + 1)}
        cart.get_basket(self.idx + 1).add_product(Product(*self.products[-1]), 2)
        self.assertFalse(self.store_manager.buy(cart))
        cart = Cart()
        cart.baskets = {self.idx - 1: Basket(self.idx - 1)}
        cart.get_basket(self.idx - 1).add_product(Product(*self.products[-1]), 30)
        self.assertFalse(self.store_manager.buy(cart))

    def test_get_sales_history(self):
        self.test_add_purchase_to_store()
        self.assertEqual(len(self.store_manager.get_sales_history(self.idx - 1, "moshe" + str(self.idx - 1), False)), 1)
        self.assertEqual(len(self.store_manager.get_sales_history(self.idx - 1, "not moshe" + str(self.idx - 1), True)),
                         1)

    def test_add_discount_to_product(self):
        self.test_add_product_to_store()
        self.assertTrue(
            self.store_manager.add_visible_discount_to_product(self.idx - 1, self.products[-1][0], "moshe" + str(self.idx - 1),
                                                       datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
                                                       10))
        self.assertFalse(
            self.store_manager.add_visible_discount_to_product(self.idx + 1, self.products[-1][0], "moshe" + str(self.idx + 1),
                                                       datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
                                                       10))

    def test_calculate_basket_price(self):
        store = self.store_manager.get_store(self.store_id)
        view_cart_dict = self.store_manager.calculate_basket_price(self.basket)
        x = 5

if __name__ == '__main__':
    unittest.main()

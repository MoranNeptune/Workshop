from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.users_managment.UserManager import UserManager


class UsersManagerInterface:

    def __init__(self):
        self.user_manager = UserManager()

    def register(self, user, username, password):
        return self.user_manager.register(user,username,password)

    ##EVERYTIME SOMEONE OPENS THE SYSTEM A NEW USER IS CREATEDDDDDDDD
    def login(self, username: str, login_username: str, password) -> bool:
        return self.user_manager.login(username, login_username, password)

    def add_guest_user(self):
        self.user_manager.add_guest_user()

    # look up via usr id change user list to map of ids and user
    def view_cart(self, username) -> Cart:
        return self.user_manager.view_cart(username)

    def logout(self, username):
        return self.user_manager.logout(username)

    def view_purchases(self, username):
        return self.user_manager.view_purchases(username)

    def add_product(self, username, store_id, product, quantity):

        return self.user_manager.add_product(store_id, product, quantity)

    def remove_product(self, username, store_id, product, quantity):
        return self.user_manager.remove_product(store_id, product, quantity)

    def get_cart(self, username):
        return self.user_manager.get_cart()

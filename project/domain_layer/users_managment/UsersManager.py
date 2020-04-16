from project import service_layer
from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.users_managment.NullUser import NullUser
from project.domain_layer.users_managment.RegisteredUser import RegisteredUser
from project.domain_layer.users_managment.User import User
from project.service_layer.Security import Security


class UserManager:

    security = Security()
    incremental_id = 0

    def __init__(self):
        self.reg_user_list = {}
        self.guest_user_list = {}
        ##maybe dictionary {id, username}
        self.admins = []
        username = self.add_guest_user()
        self.register(username, "admin", "1234")
        self.admins.append("admin")

    def find_reg_user(self, username) -> RegisteredUser:
        user = self.reg_user_list[username]
        if user is None:
            user = self.guest_user_list[username]
            if user is None:
                user = NullUser()
        return user

    def find_user(self, username) -> User:
        user = self.reg_user_list[username]
        if user is None:
            user = NullUser()
        return user

    def register(self, username, new_username, password):
        check = self.find_reg_user(new_username)
        if isinstance(check, NullUser):
            registered = RegisteredUser(new_username)
            self.security.add_user(new_username, password)
            user = self.find_user(username)
            registered.cart = user.cart
            self.reg_user_list[new_username] = registered
            return True
        else:
            return False

    def login(self, username: str, login_username: str, password) -> bool:
        check = self.find_reg_user(login_username)
        if not (isinstance(check, NullUser)):
            if self.security.verify_password(login_username, password):
                check.loggedin = True
                self.guest_user_list.pop(username)
                return True
            else:
                return False
        else:
            return False

    def add_guest_user(self):
        user = User("guestUser" + str(self.incremental_id))
        self.incremental_id += 1
        self.guest_user_list[user.username] = user
        return user.username

    #look up via usr id change user list to map of ids and user
    def view_cart(self, username) -> Cart:
        user = self.find_user(username)
        return user.view_cart()

    def logout(self, username):
        user = self.find_reg_user(username)
        return user.logout()

    def view_purchases(self,username):
        return self.find_user(username).purchase_history
        ##if view purchases of username

    def add_product(self, username, store_id, product, quantity):
        user = self.find_user(username)
        return user.add_product(store_id, product, quantity)

    def remove_product(self, username, store_id, product, quantity):
        user = self.find_user(username)
        return user.remove_product(store_id,product, quantity)

    def get_cart(self, username):
        user = self.find_user(username)
        return user.get_cart()

    def view_purchases_admin(self, username, admin):
        if admin in self.admins:
            return self.find_reg_user(username).purchase_history

    def is_admin(self,username):
        return username in self.admins

    def add_managed_store(self, username, store_id):
        user = self.find_reg_user(username)
        return user.add_managed_store(store_id)

    def get_managed_stores(self, username):
        user = self.find_reg_user(username)
        return user.get_managed_store()

    def check_if_registered(self, username):
        return username in self.reg_user_list.keys()

    def check_if_loggedin(self, username):
        user = self.find_reg_user(username)
        return user.loggedin

    def add_purchase(self, username, purchase):
        user = self.find_user(username)
        user.add_purchase(purchase)

    def remove_cart(self, username):
        user = self.find_user(username)
        user.remove_cart()
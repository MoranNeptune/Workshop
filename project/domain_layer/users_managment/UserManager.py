from project import service_layer
from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.users_managment.NullUser import NullUser
from project.domain_layer.users_managment.RegisteredUser import RegisteredUser
from project.domain_layer.users_managment.User import User


class UserManager:

    security = service_layer.Security()
    incremental_id = 0

    def __init__(self):
        self.reg_user_list = {}
        self.guest_user_list = {}
        ##maybe dictionary {id, username}
        self.admins = []

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

    def register(self, user, username, password):
        check = self.find_reg_user(username)
        if isinstance(check, NullUser):
            registered = RegisteredUser(username)
            self.security.add_user(username, password)
            registered.cart = user.cart
            self.reg_user_list[username] = registered
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
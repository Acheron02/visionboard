from db import load_user_data, save_user_data, hash_password

class AuthManager:
    def __init__(self):
        self.is_logged_in = False
        self.current_user = None

    def login(self, email, password):
        users = load_user_data()
        hashed_password = hash_password(password)
        if email in users and users[email]["password"] == hashed_password:
            self.is_logged_in = True
            self.current_user = {"email": email, **users[email]}
            return True
        return False

    def logout(self):
        self.is_logged_in = False
        self.current_user = None

    def register(self, email, password, user_type):
        users = load_user_data()
        if email in users:
            return False, "Email already exists."
        users[email] = {
            "password": hash_password(password),
            "user_type": user_type
        }
        save_user_data(users)
        return True, "Registration successful!"

    def delete_account(self):
        if self.current_user:
            users = load_user_data()
            del users[self.current_user["email"]]
            save_user_data(users)
            self.logout()

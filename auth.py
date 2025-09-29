from db import load_user_data, save_user_data, hash_password

class AuthManager:
    def __init__(self):
        self.is_logged_in = False
        self.current_user = None

    def login(self, identifier, password):
        """
        identifier can be either email OR username.
        """
        users = load_user_data()
        hashed_password = hash_password(password)

        # 1. Try direct email login
        if identifier in users:
            if users[identifier]["password"] == hashed_password:
                self.is_logged_in = True
                self.current_user = {"email": identifier, **users[identifier]}
                return True
            return False

        # 2. Otherwise, search by username
        for email, user_data in users.items():
            if user_data.get("username") == identifier and user_data["password"] == hashed_password:
                self.is_logged_in = True
                self.current_user = {"email": email, **user_data}
                return True

        return False

    def logout(self):
        self.is_logged_in = False
        self.current_user = None

    def register(self, username, email, password, user_type):
        users = load_user_data()

        # Ensure unique email
        if email in users:
            return False, "Email already exists."

        # Ensure unique username
        for u in users.values():
            if u.get("username") == username:
                return False, "Username already taken."

        # Save new user
        users[email] = {
            "username": username,
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

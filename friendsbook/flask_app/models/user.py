from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re
from flask_bcrypt import Bcrypt
# from PIL import Image

bcrypt = Bcrypt(app) 


class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.band = []

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM users;"
        results = connectToMySQL("friendsbook").query_db(query,data)

        users = []
        for row in results:
            users.append(User(row))

        return users


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s; "
        results = connectToMySQL("friendsbook").query_db(query,data)

        if len(results) < 1: 
            return False

        return User(results[0])


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("friendsbook").query_db(query,data)

        if len(results) < 1: 
            return False

        return User(results[0])


    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUE (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL("friendsbook").query_db(query,data)
        print(results)
        return results


    @staticmethod
    def register_validator(post_data):
        is_valid = True


        if len(post_data["first_name"]) < 3:
            flash("First Name must be atleast 3 characters.")
            is_valid = False 

        if len(post_data["last_name"]) < 3:
            flash("Last Name must be atleast 3 characters.")
            is_valid = False 

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(post_data["email"]): 
            flash("Invalid email address!")
            is_valid = False

        else:
            user = User.get_by_email ({"email": post_data["email"]})
            if user:
                flash("Email is already in use!!")
                is_valid = False

        if len(post_data["password"]) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False

        if post_data["password"] != post_data["confirm_password"]:
            flash("Password and confirm password must match")
            is_valid = False
        return is_valid


    @staticmethod
    def login_validator(post_data):
        user = User.get_by_email ({"email": post_data["email"]})

        if not user:
            flash("Invalid Email")

            return False

        if not bcrypt.check_password_hash(user.password, post_data["password"]):
            flash("Invalid password")
            return False

        return True


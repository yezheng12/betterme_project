from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db="betterme_schema"
    def __init__ (self,data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password ) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    @classmethod
    def get_all_user(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])
    

    @staticmethod
    def validate_register(data):
        is_valid=True
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result=connectToMySQL(User.db).query_db(query,data)
        if len(result) >= 1:
            is_valid=False
            flash("Email already taken.","register")

        if len(data['first_name'])<2:
            is_valid = False
            flash("First Name must be at least 2 characters.","register")
        if len(data['last_name'])<2:
            is_valid = False
            flash("Last Name must be at least 2 characters.","register")
        if not EMAIL_REGEX.match(data['email']):
            is_valid=False
            flash("Invalid Email!","register")
        # if len(data['password'])<8:
        #     is_valid=False
        #     flash("Password must be at least 8 characters")
        if data['password'] != data['confirm_password']:
            is_valid=False
            flash("Password don't match.","register")
        return is_valid
from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # If adding tags, uncomment
        # self.tags = data['tags']
        self.vacations = []

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO nomadnirvana.users ( username, email, password )
        VALUES (%(username)s, %(email)s, %(password)s);
        """
        return connect_to_mysql(DATABASE).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * from nomadnirvana.users WHERE users.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM nomadnirvana.users WHERE users.email = %(email)s;"
        result = connect_to_mysql(DATABASE).query_db(query,data)
        
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM nomadnirvana.users WHERE users.username = %(username)s;"
        result = connect_to_mysql(DATABASE).query_db(query,data)
        
        if result:
            return cls(result[0])
        return False

    @staticmethod
    def validate_user(data):
        is_valid = True
        
        if len(data['username']) < 2:
            flash("Username must be at least 2 characters.", "reg")
            is_valid = False

        else:
            potential_user = User.get_by_username({'username': data['username']})
            if potential_user:
                is_valid = False
                flash("This username is taken", 'reg')
        
        if len(data['email']) < 6:
            flash("Email must be at least 6 characters.", "reg")
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']): 
            flash("Email must be in a valid format", "reg")
            is_valid = False
        
        else:
            potential_user = User.get_by_email({'email': data['email']})
            if potential_user:
                is_valid = False
                flash("Email is taken", 'reg')
            
        if len(data['password']) < 1:
            is_valid = False
            flash("Please provide password.", "reg")
        
        elif len(data['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.", "reg")
        
        elif data['password'] != data['confirm']:
            is_valid = False
            flash("Passwords do not match", 'reg')

        return is_valid
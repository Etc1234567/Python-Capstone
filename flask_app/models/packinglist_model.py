from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import DATABASE

class PackingListItem:
    def __init__(self,data):
        self.id = data['id']
        self.category = data['category']
        self.name = data['name']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.vacation_id = data['vacation_id']
        self.ispacked = False

        
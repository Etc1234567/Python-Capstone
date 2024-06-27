from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import DATABASE
from flask import flash

class PackingListItem:
    def __init__(self,data):
        self.id = data['id']
        self.category = data['category']
        self.name = data['name']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.vacation_id = data['vacation_id']
        self.vacation_user_id = data['vacation_user_id']
        
    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM nomadnirvana.packing_list_items WHERE id = %(id)s;"
        results = connect_to_mysql(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_all_for_trip(cls, data):
        query= """
            SELECT * from nomadnirvana.packing_list_items
            WHERE packing_list_items.vacation_id = %(id)s;
        """

        results = connect_to_mysql(DATABASE).query_db(query, data)

        all_items = []
        for row_from_db in results:
            pl_instance = cls(row_from_db)
            all_items.append(pl_instance)
        return all_items
    
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO nomadnirvana.packing_list_items ( category, name, quantity, vacation_id, vacation_user_id )
        VALUES (%(category)s, %(name)s, %(quantity)s, %(vacation_id)s, %(vacation_user_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query= """ 
        DELETE FROM nomadnirvana.packing_list_items WHERE packing_list_items.id = %(id)s;
        """

        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE nomadnirvana.packing_list_items
        SET
        category = %(category)s,
        name = %(name)s, 
        quantity = %(quantity)s
        WHERE packing_list_items.id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate_pl(data):
        is_valid = True

        if len(data['name']) < 1:
            flash("Please add a name for the packing list item.", "packing_list")
            is_valid = False

        if len(data['category']) < 1:
            flash("Please select a category for your item.", "packing_list")
            is_valid = False

        if len(data['quantity']) < 1:
            flash("How many of this item will you need?", "packing_list")
            is_valid = False

        return is_valid


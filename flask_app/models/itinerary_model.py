from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import DATABASE
from flask import flash

class Itinerary:
    def __init__(self,data):
        self.id = data['id']
        self.day = data['day']
        self.time = data['time']
        self.address = data['address']
        self.description = data['description']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.vacation_id = data['vacation_id']
        self.vacation_user_id = data['vacation_user_id']

    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM nomadnirvana.itinerarys WHERE id = %(id)s;"
        results = connect_to_mysql(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_all_for_trip(cls, data):
        query= """
            SELECT * from nomadnirvana.itinerarys
            WHERE itinerarys.vacation_id = %(id)s;
        """

        results = connect_to_mysql(DATABASE).query_db(query, data)

        all_items = []
        for row_from_db in results:
            itinerary_instance = cls(row_from_db)
            all_items.append(itinerary_instance)
        return all_items
    
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO nomadnirvana.itinerarys ( day, time, address, description, notes, vacation_id, vacation_user_id )
        VALUES (%(day)s, %(time)s, %(address)s, %(description)s, %(notes)s, %(vacation_id)s, %(vacation_user_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query= """ 
        DELETE FROM nomadnirvana.itinerarys WHERE itinerarys.id = %(id)s;
        """

        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE nomadnirvana.itinerarys
        SET
        day = %(day)s,
        time = %(time)s, 
        address = %(address)s,
        description = %(description)s,
        notes = %(notes)s
        WHERE itinerarys.id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate_itinerary(data):
        is_valid = True

        if (data['day']) == "":
            is_valid = False
            flash("Please add the date of your activity.", "itinerary")

        if (data['time']) == "":
            is_valid = False
            flash("Please add the start time of your activity.", "itinerary")

        if len(data['address']) < 1:
            flash("Please add an address or location name for your activity.", "itinerary")
            is_valid = False

        if len(data['description']) < 1:
            flash("Please add a description.", "itinerary")
            is_valid = False

        return is_valid
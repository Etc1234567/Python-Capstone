from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import DATABASE
from flask import flash

class Inspiration:
    def __init__(self,data):
        self.id = data['id']
        self.link = data['link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.vacation_id = data['vacation_id']
        self.vacation_user_id = data["vacation_user_id"]
        self.vacation = None
        self.edited_link = data["edited_link"]

    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM nomadnirvana.inspiration WHERE id = %(id)s;"
        results = connect_to_mysql(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_all(cls):
        query= """
            SELECT * from nomadnirvana.inspiration;
        """

        results = connect_to_mysql(DATABASE).query_db(query)

        all_videos = []
        for row_from_db in results:
            video_instance = cls(row_from_db)
            all_videos.append(video_instance)
        return all_videos

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO nomadnirvana.inspiration ( link, vacation_id, vacation_user_id, edited_link )
        VALUES (%(link)s, %(vacation_id)s, %(vacation_user_id)s, %(edited_link)s);
        """
        return connect_to_mysql(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query= """ 
        DELETE FROM nomadnirvana.inspiration WHERE inspiration.id = %(id)s;
        """

        return connect_to_mysql(DATABASE).query_db(query,data)  

    @classmethod
    def get_all_for_trip(cls, data):
        query= """
            SELECT * from nomadnirvana.inspiration
            WHERE nomadnirvana.inspiration.vacation_id = %(id)s;
        """

        results = connect_to_mysql(DATABASE).query_db(query, data)

        if results:
            all_videos = []
            for row_from_db in results:
                video_instance = cls(row_from_db)
                all_videos.append(video_instance)
            return all_videos
        
        return False
    
    @staticmethod
    def validate_video(data):
        is_valid = True

        if len(data['link']) < 1:
            flash("Please add a YouTube link.", "inspiration")
            is_valid = False

        elif ("youtube.com") not in (data['link']):
            flash("Please add a valid YouTube link.", "inspiration")
            is_valid = False

        return is_valid

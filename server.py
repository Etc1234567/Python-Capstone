from flask_app import app
from flask_app.controllers import user_controller, vacation_controller, video_controller

if __name__=="__main__": 
    app.run(debug=True, host="localhost", port=8000) 

from flask_app import app
from flask import render_template, request, session, redirect, flash, jsonify
from flask_app.models import inspiration_model, vacation_model

@app.route('/video/add/<int:vacation_id>')
def render_add_video(vacation_id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "id": vacation_id
    }

    this_vacation = vacation_model.Vacation.get_one(data)

    return render_template("add_video.html", this_vacation=this_vacation)

@app.route('/video/new/<int:vacation_id>', methods=["POST"])
def process_add_video(vacation_id):
    if not inspiration_model.Inspiration.validate_video(request.form):
        return redirect(f'/video/add/{vacation_id}')
        
    user_id = session['user_id']

    splitlink = request.form['link'].split("=")

    edited_link = splitlink[1]

    data = {
        "link": request.form["link"],
        "vacation_user_id": user_id,
        "vacation_id": vacation_id,
        "edited_link": edited_link
        }
        
    inspiration_model.Inspiration.save(data)
        
    return redirect(f'/trip/view/{vacation_id}')
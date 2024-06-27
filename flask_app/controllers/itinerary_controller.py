from flask_app import app
from flask import render_template, request, session, redirect, flash, jsonify
from flask_app.models import itinerary_model, vacation_model

@app.route('/itinerary/add/<int:vacation_id>')
def render_add_itinerary(vacation_id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "id": vacation_id
    }

    this_vacation = vacation_model.Vacation.get_one(data)

    itinerary = itinerary_model.Itinerary.get_all_for_trip(data)

    return render_template("itinerary.html", this_vacation=this_vacation, itinerary=itinerary)

@app.route("/itinerary/add/added/<int:vacation_id>", methods=["POST"])
def process_add_itinerary(vacation_id):
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session['user_id']

    data = {
        **request.form,
        "vacation_id": vacation_id,
        "vacation_user_id": user_id
    }

    if not itinerary_model.Itinerary.validate_itinerary(request.form):
        return redirect(f'/itinerary/add/{vacation_id}')

    itinerary_model.Itinerary.save(data)

    return redirect(f"/trip/view/{vacation_id}")
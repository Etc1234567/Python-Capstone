from flask_app import app
from flask import render_template, request, session, redirect, flash, jsonify
from flask_app.models import vacation_model, inspiration_model
from flask_app.models import user_model

# Add trip routes
@app.route('/trip/add')
def render_add_trip():
    if "user_id" not in session:
        return redirect("/")
    return render_template("addtrip.html")

@app.route('/trip/new', methods=['POST'])
def process_add_trip():
    if not vacation_model.Vacation.validate_vacation(request.form):
        return redirect('/trip/add')
    
    user_id = session['user_id']

    data = {
        "city": request.form["city"],
        "country": request.form["country"],
        "date": request.form["date"],
        "user_id": user_id
    }
    
    vacation_model.Vacation.save(data)
    
    return redirect('/dashboard')

@app.route("/trip/view/<int:vacation_id>")
def render_view_trip(vacation_id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "id" : vacation_id
    }
    
    this_vacation = vacation_model.Vacation.get_one(data)

    vacations = vacation_model.Vacation.get_all()

    inspirationvideos = inspiration_model.Inspiration.get_all_for_trip(data)

    logged_user = user_model.User.get_by_id({"id": session['user_id']})
    
    return render_template("trip_dashboard.html", this_vacation=this_vacation, vacations=vacations, logged_user=logged_user, inspirationvideos=inspirationvideos)

@app.route("/trip/delete/<int:vacation_id>")
def delete_trip(vacation_id):
    if 'user_id' not in session:
        return redirect('/')
    
    data= {
        "id": vacation_id
    }

    this_vacation = vacation_model.Vacation.get_one(data)

    vacation_model.Vacation.delete(data)
    return redirect("/dashboard")

@app.route("/api/vacations/<int:vacation_id>")
def api_get_all(vacation_id):
    data = {
        "id": vacation_id
    }
    return vacation_model.Vacation.get_one_dict(data)

@app.route("/trip/edit/<int:vacation_id>")
def render_edit_trip(vacation_id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": vacation_id
    }

    this_vacation = vacation_model.Vacation.get_one(data)

    if this_vacation.user_id != session['user_id']:
        flash("The vacation you are trying to edit is owned by another user and cannot be updated.", 'add')
        return redirect("/dashboard")


    return render_template("edittrip.html", this_vacation=this_vacation)

@app.route("/vacation/edit/<int:vacation_id>", methods=["POST"])
def process_edit_trip(vacation_id):

    data = {
        **request.form,
        "id": vacation_id
    }

    if not vacation_model.Vacation.validate_vacation(request.form):
        return redirect(f'/trip/edit/{vacation_id}')
    
    vacation_model.Vacation.update(data)

    return redirect(f"/trip/view/{vacation_id}")
    


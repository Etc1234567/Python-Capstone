from flask_app import app
from flask import render_template, request, session, redirect, flash, jsonify
from flask_app.models import packinglist_model, vacation_model

@app.route('/packinglist/add/<int:vacation_id>')
def render_add_pl(vacation_id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "id": vacation_id
    }

    this_vacation = vacation_model.Vacation.get_one(data)

    packinglist = packinglist_model.PackingListItem.get_all_for_trip(data)

    return render_template("packinglist.html", packinglist=packinglist, this_vacation=this_vacation)

@app.route("/packinglist/added/<int:vacation_id>", methods=["POST"])
def process_add_pl(vacation_id):
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session['user_id']

    data = {
        **request.form,
        "vacation_id": vacation_id,
        "vacation_user_id": user_id
    }

    if not packinglist_model.PackingListItem.validate_pl(request.form):
        return redirect(f'/packinglist/add/{vacation_id}')

    packinglist_model.PackingListItem.save(data)

    return redirect(f"/trip/view/{vacation_id}")
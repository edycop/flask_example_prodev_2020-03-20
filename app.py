from flask import (Flask, render_template, abort, jsonify, request,
                   redirect, url_for)
import datetime

from model import db, save_db

app = Flask(__name__)
# __name__ hace referencia al nombre del módulo actual


@app.route('/')
def welcome():
    return render_template("welcome.html",
                           message="Con el apoyo de la Fundación Universitaria de Popayán - FUP",
                           events=db)


@app.route('/event/<int:index>')
def event_view(index):
    try:
        event = db[index]
        return render_template("event.html",
                               event=event,
                               index=index,
                               max_index=len(db)-1)
    except IndexError:
        abort(404)


@app.route('/api/events/')
def api_event_list():
    try:
        return jsonify(db)
    except IndexError:
        abort(404)


@app.route('/add_event/', methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        event = {"name": request.form['name'], "date": request.form['date']}
        db.append(event)
        save_db()
        return redirect(url_for("event_view", index=len(db)-1))
    else:
        return render_template("add_event.html")


@app.route('/remove_event/<int:index>', methods=["GET", "POST"])
def remove_event(index):
    if request.method == "POST":
        del db[index]
        save_db()
        return redirect(url_for('welcome'))
    else:
        return render_template("remove_event.html", card=db[index])


@app.route('/api/event/<int:index>')
def api_event_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)


@app.route('/date')
def date():
    return f'Fecha actual: <strong>{datetime.datetime.now()} </strong>'


if __name__ == '__main__':
    app.run(debug=True)

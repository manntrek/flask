from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
from model import db, save_db
from database import get_db
import os
import database
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

counter = 0

app = Flask(__name__)
app.config.from_prefixed_env()
database.init_app(app)

print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
print(f"Using Database: {app.config.get('DATABASE')}")

@app.route("/")
def welcome ():
    return render_template("welcome.html",
            cards=db)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',8080)))

@app.route('/add_card', methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        #user submited the form, it has to be processed
        card = {"question": request.form['question'],
        "answer" : request.form['answer']}
        db.append(card)
        save_db()
        #insert in DB as well
        
        question = request.form['question']
        answer = request.form['answer']
        
        try:
            dbs = get_db()
        
            dbs.execute (
                "INSERT INTO cards (question, answer) VALUES (?, ?)",
                (question, answer),
            )
            dbs.commit()
        except IndexError:
            print("dbs insert failed")

        
        return redirect(url_for('card_view', index=len(db)-1    ))
    else:
        return render_template("add_card.html") #in else case, the use wants to retrive the template in order to fill data

@app.route("/card/<int:index>")
def card_view (index):
    try:
        card = db[index]
        return render_template("card.html",
                               card=card, 
                               index=index,
                               max_index=len(db) - 1)
    except IndexError:
        abort(404)
#database
@app.route("/dbcard/<int:index>")
def card_view_dbs (index):
    try:        
        dbs = get_db()
        card = dbs.execute(

                "SELECT question, answer FROM cards WHERE id = 1"

            ).fetchall()

        return render_template("card.html",
                               card=card, 
                               index=index,
                               max_index=len(db) - 1)
    except IndexError:
        abort(404)


@app.route("/api/card/")
def api_card_list ():
    return jsonify(db)

@app.route("/time")
def time():
    return f"This page was displayed at: {datetime.now().time()}"

@app.route("/api/card/<int:index>")
def api_card_detail (index):
    try:
        return db[index]
    except IndexError:
        abort(404)



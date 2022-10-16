from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import flask
from firebase import firebase, db
from similarity import similarity
import requests



app = flask.Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev'
    )

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            data = {"password": password, "sleep": 0, "noise": 0, "roommate_num": 0, "phil_response": 0}
            db.child("users").child(username).set(data)
            return redirect(url_for('index'))

        flash(error)

    return render_template('register.html')
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = None
        pwd = None
        error = None
        for x in db.child("users").get().each():
            if(x.key() == username):
                user = username
                if(x.val()["password"] == password):
                    pwd = password

        if user is None:
            error = 'Incorrect username.'
        elif pwd is None:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/response', methods=('GET', 'POST'))
def response():
    if request.method == 'POST':
        if session.get('user_id') is None:
            return redirect(url_for('login'))
        name = request.form["name"]
        #number = request.form["number"]
        sleep = request.form["sleep"]
        age = request.form["age"]
        wakeup = request.form["wake"]
        phil = request.form["phil"]
        #roommate_num = request.form["roommate_num"]
        zipcode = request.form["zip"]
        noise = request.form["noise"]
        miles = request.form["miles"]
        
        db.child("users").child(session.get('user_id')).update({"name": name, "sleep":sleep, "age":age, "wakeup":wakeup, "phil":phil, "zip":zipcode, "miles":miles})
        db.child("corpus").update({session.get("user_id"): phil})
        corpus = db.child("corpus").get().val()
        corpus[session.get("user_id")] = phil
        similar = similarity(phil, corpus)
        user_data = db.child("users").get()
        scores = []
        
        for a in user_data.each():
            key = a.key()
            value = a.val()
            score = 0
            if(key != session.get("user_id")):
                other_zip = value["zip"]
                dist = requests.get("https://www.zipcodeapi.com/rest/FgQQQxR4uLE58w2JXSuAM9BNdY4AAOenBGIO9QhzecYJscUQAJAVTdZItlLz3bwO/distance.json/"+str(zipcode)+"/"+str(other_zip)+"/mile")
                if(dist.json()["distance"] < float(miles)):
                    score += abs(float(age)-float(value["age"]))/100
                    score += abs(float(noise)-float(value["noise"]))/float(noise)
                    score += abs(float(wakeup)-float(value["noise"]))/12.0
                    score += abs(float(sleep)-float(value["sleep"]))/12.0
                    print("Score: ", score)
                    
                    for i in range(similar.size):
                        if key == list(corpus.keys())[i]:
                            score+=(1-similar[i])
                    
                    scores.append({key: score})

        db.child("users").child(session.get('user_id')).update({"scores": scores})



            
        


        return redirect(url_for('index'))
    return render_template('response.html')



@app.before_request
def load_logged_in_user():
    g.user = session.get('user_id')


if __name__ == '__main__':
    app.run()
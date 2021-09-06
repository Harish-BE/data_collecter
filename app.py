from flask import *
from flask_pymongo import pymongo
from pymongo import MongoClient

app=Flask(__name__)
CONNECTION_STRING ='mongodb+srv://Harish:harish@cluster0.hpddk.mongodb.net/user?retryWrites=true&w=majority'

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('users')
user_collection = pymongo.collection.Collection(db, 'user_collection')

@app.route("/")
def render():
    return render_template("index.html")
##################################################################################
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/check",methods=['POST'])
def check():
    username=request.form['username']
    password=request.form['password']
    user_db=db.userDB.find_one({"username":username})
    if user_db:
        if(user_db["username"]==username and user_db["password"]==password):
            return redirect(url_for('user', username=username))
        else:
            return "Incorrect username or password"
    else:
        return "Incorrect username or password"


###################################################################################
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register_user',methods=['POST'])
def register_user():
    username=request.form['username']
    password=request.form['password']
    db.userDB.insert_one({"username":username,"password":password, "data":""})
    return redirect("/")

#################################################################################

@app.route('/user/<username>')
def user(username):
    ch=db.userDB.find_one({"username":username})
    if(ch['username']==username):
        return render_template("database.html", username=username, text=ch["data"])
    else:
        db.userDB.insert_one({"username":username})
        return render_template('database.html',username=username, text=ch["data"])

@app.route('/database',methods=['POST'])
def database():
    data=request.form['data']
    username=request.form['username']
    db.userDB.update({"username":username },{"$set" : {"data":data}})
    return "saved"

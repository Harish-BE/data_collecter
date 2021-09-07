from flask import *
from flask_pymongo import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
PSW=os.getenv("PSW")

app=Flask(__name__)
CONNECTION_STRING =f"mongodb+srv://Harish:{PSW}@cluster0.hpddk.mongodb.net/user?retryWrites=true&w=majority"

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
@app.route("/database",methods=['POST'])
def database():
    username=request.form['username']
    password=request.form['password']
    user_db=db.userDB.find_one({"username":username})
    if user_db:
        if(user_db["username"]==username and user_db["password"]==password):
            return render_template("database.html", username=username, text=user_db["data"])
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

@app.route('/save',methods=['POST'])
def save():
    data=request.form['data']
    username=request.form['username']
    db.userDB.update({"username":username },{"$set" : {"data":data}})
    return "saved"

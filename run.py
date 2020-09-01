import json
import os  
from flask import Flask, render_template, url_for, request, session, redirect
from datetime import datetime
from flask import Flask, json, redirect, render_template, request, session, url_for, flash, g
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
import bcrypt

app = Flask(__name__)
app.secret_key = "randomstring123"
messages = []


app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://root:RootUser@myfirstcluster.zhfps.mongodb.net/task_manager?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
def index():
    data = []
    with open("static/data/products.json", "r") as json_data:
        data = json.load(json_data)
        return render_template("index.html", page_title="Shop Online", products=data)


@app.route('/flyers')
def flyers():
    return render_template("flyers.html", page_title="Flyers")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})
        if login_user:
                if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                    session['username'] = request.form['username']
                return redirect(url_for('home'))
        return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')
@app.route('/home')
def home():
    return render_template("home.html", page_title="Start shopping")


@app.route('/contact')
def contact():
    return render_template("contact.html", page_title="Contact Us")


@app.route('/shoppingcart')
def shoppingcart():
    return render_template("shoppingcart.html", page_title="Shopping Cart")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)



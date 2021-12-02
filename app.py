from flask import Flask, request, render_template,jsonify,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_login import login_required, logout_user, login_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class User(UserMixin,db.Model):#User and profile
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True)
    name=db.Column(db.String(30))
    password=db.Column(db.String(30))
    image_link=db.Column(db.String(30))
    email=db.Column(db.String(30))
class Posts(db.Model):#This is both replies to posts and posts them selfs replies are treated as posts 
    id=db.Column(db.Integer,primary_key=True)
    head=db.Column(db.Boolean)#Represents if it is a replie or not for generating feed
    date=(db.String(30))#Can be used to sort feed by recenctcy 
    text=db.Column(db.String(30))
class Reply(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    post_id=db.Column(db.Integer)
    rep_id=db.Column(db.Integer)
class Likes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    post_id=db.Column(db.Integer)


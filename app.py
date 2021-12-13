from flask import Flask, request, render_template, jsonify, session, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_login import login_required, logout_user, login_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import date
import json

from werkzeug.utils import header_property


app = Flask(__name__)
today = date.today()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
admin = Admin(app)
app.secret_key = 'ASDASDDASDSAFA'

app.config['CORS_HEADERS'] = 'Content-Type'


class User(UserMixin, db.Model):  # User and profile
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(30))
    image_link = db.Column(db.String(30))
    email = db.Column(db.String(30))
    user_type = db.Column(db.Integer)


class Posts(db.Model):  # This is both replies to posts and posts them selfs replies are treated as posts
    id = db.Column(db.Integer, primary_key=True)
    # Represents if it is a reply or not for generating feed
    head = db.Column(db.Boolean)
    date = (db.String(30))  # Can be used to sort feed by recenctcy
    text = db.Column(db.String(30))
    user_id = db.Column(db.Integer)


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    rep_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    text = db.Column(db.String(30))


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)


login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class adminview(ModelView):
    def is_accessible(self):
        # print(current_user.user_type)
        try:
            if(int(current_user.user_type) == 1):
                # print("TRUE")
                return current_user.is_authenticated
            else:
                return False
        except:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect("login")


admin.add_view(adminview(User, db.session))
admin.add_view(adminview(Posts, db.session))
admin.add_view(adminview(Reply, db.session))
admin.add_view(adminview(Likes, db.session))

# Register function handler


@app.route('/register', methods=['GET', 'POST'])
def creatUser():
    if(request.method == "POST"):
        user = request.form['username']
        passs = request.form['password']
        email = request.form['email']
        name = request.form['name']
        #
        user = User(username=user, name=name, email=email,
                    password=passs, user_type=2)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("login")
        except:
            print("User Already Exists")
    return render_template("register.html")

@app.route('/getuserbyid', methods=['GET', 'POST'])
def getUserID():
    # TODO if statements to return filtered by user preference posts
    # returns all posts

    
    user = User.query.filter_by(id=request.form['text']).all()

    response = {}

    for count, row in enumerate(user):
        response[count] = {column: str(getattr(row, column))
                        for column in row.__table__.c.keys()}

    return jsonify(response)

@app.route('/getreplybyid', methods=['GET', 'POST'])
def getReplies():
    # TODO if statements to return filtered by user preference posts
    # returns all posts

    user = Reply.query.filter_by(post_id=request.form['text']).all()

    response = {}

    for count, row in enumerate(user):
        response[count] = {column: str(getattr(row, column))
                        for column in row.__table__.c.keys()}

    return jsonify(response)


@app.route('/getuser', methods=['GET'])
def getUser():
    if(request.method == "GET"):
        # TODO if statements to return filtered by user preference posts
        # returns all posts
        posts = User.query.all()

        response = {}

        for count, row in enumerate(posts):
            response[count] = {column: str(getattr(row, column))
                               for column in row.__table__.c.keys()}

        return jsonify(response)


@app.route('/posts', methods=['POST', 'GET', 'DELETE'])
def postAPI():
    if(request.method == "POST"):  # TAKE a given string and insert to database then return list of users to posts to update using ajax
        print("Text POST")
        post = request.form['text']
        insert = Posts(head=1, date=today.strftime("%d/%m/%Y"),
                       text=post, user_id=current_user.id)
        db.session.add(insert)
        db.session.commit()
        # user_id returns all posts for the user
        user_id = Posts.query.filter_by(user_id=current_user.id).all()

        # TODO update posts return something to the feed

        return 'Post Created'
    if(request.method == "GET"):
        # TODO if statements to return filtered by user preference posts
        # returns all posts
        posts = Posts.query.all()

        response = {}

        for count, row in enumerate(posts):
            response[count] = {column: str(getattr(row, column))
                               for column in row.__table__.c.keys()}

        return jsonify(response)

    if(request.method == "DELETE"):
        post_id = request.form['post_id']
        Posts.query.filter_by(id=post_id)



@app.route('/userposts', methods=['POST', 'GET', 'DELETE'])
def userpostAPI():
    if(request.method == "POST"):  # TAKE a given string and insert to database then return list of users to posts to update using ajax
        print("Text POST")
        post = request.form['text']
        insert = Posts(head=1, date=today.strftime("%d/%m/%Y"),
                       text=post, user_id=current_user.id)
        db.session.add(insert)
        db.session.commit()
        # user_id returns all posts for the user
        user_id = Posts.query.filter_by(user_id=current_user.id).all()

        # TODO update posts return something to the feed

        return 'Post Created'
    if(request.method == "GET"):
        # TODO if statements to return filtered by user preference posts
        # returns all posts
        posts = Posts.query.filter_by(user_id=current_user.id).all()

        response = {}

        for count, row in enumerate(posts):
            response[count] = {column: str(getattr(row, column))
                               for column in row.__table__.c.keys()}

        return jsonify(response)

    if(request.method == "DELETE"):
        post_id = request.form['post_id']
        Posts.query.filter_by(id=post_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == "POST"):
        user = request.form['username']
        passs = request.form['password']
        print(user)
        print(passs)
        try:
            session.pop('user_id', None)
            user = User.query.filter_by(username=user).first()
            print(user.user_type)
            if(user.password == passs):
                session['user_id'] = user.id
                login_user(user)
                if(int(user.user_type) == 1):
                    print("Valid Admin Login")
                    return redirect('/admin')
                if(int(user.user_type) == 2):
                    print("Valid User Login")
                    return redirect('/home')
            else:
                print("Wrong Password")
        except:
            print("User does not exist")
            pass

    return render_template("login.html")

# logout function


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    print(current_user.id)
    if(request.method == 'GET'):
        logout_user()
        return redirect('/login')

# home route


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", name=current_user.name)

# userprofile page


@app.route('/userprofile', methods=['GET', 'POST'])
def userprofile():

    return render_template("userprofile.html", name=current_user.name, user_posts=Posts.query.filter_by(user_id=current_user.id).all())


if __name__ == '__main__':
    app.debug = True

    app.run()

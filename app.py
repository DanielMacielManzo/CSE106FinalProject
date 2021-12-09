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
admin=Admin(app)
app.secret_key = 'ASDASDDASDSAFA'

class User(UserMixin,db.Model):#User and profile
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True)
    name=db.Column(db.String(30))
    password=db.Column(db.String(30))
    image_link=db.Column(db.String(30))
    email=db.Column(db.String(30))
    user_type=db.Column(db.Integer)
class Posts(db.Model):#This is both replies to posts and posts them selfs replies are treated as posts 
    id=db.Column(db.Integer,primary_key=True)
    head=db.Column(db.Boolean)#Represents if it is a reply or not for generating feed
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

login=LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class adminview(ModelView):
    def is_accessible(self):
        #print(current_user.user_type)
        try:
            if(int(current_user.user_type)==1):
                print("TRUE")
                return current_user.is_authenticated
            else:
                return False
        except:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect("login")

admin.add_view(adminview(User,db.session))
admin.add_view(adminview(Posts,db.session))
admin.add_view(adminview(Reply,db.session))
admin.add_view(adminview(Likes,db.session))


@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        user=request.form['username']
        passs=request.form['password']  
        print(user)
        print(passs)
        try:
            session.pop('user_id', None)
            user=User.query.filter_by(username=user).first()
            print(user.user_type)
            if(user.password==passs):
                session['user_id'] = user.id
                login_user(user)
                if(int(user.user_type)==1):
                    print("Valid Admin Login")
                    return redirect('/admin')
                if(int(user.user_type)==2):
                    print("Valid User Login")
                    return redirect('/home')
            else:
                print("Wrong Password")
        except:
            print("User does not exist")
            pass
    
    return render_template("login.html")
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if(request.method=='GET'):
        logout_user()
        return redirect('/login')

@app.route('/home',methods=['GET','POST'])
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.debug = True

    app.run()   

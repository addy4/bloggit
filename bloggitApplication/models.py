from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bloggitApplication import db
from bloggitApplication import login_init
from bloggitApplication import app
from flask_login import UserMixin

#this for reloading the user from the user ID stored in the session. 
@login_init.user_loader
def loaded_user(user_id_num):
    return User.query.get(int(user_id_num))

class User(db.Model, UserMixin):
      id = db.Column(db.Integer, primary_key = True) 
      username = db.Column(db.String(20), unique = True, nullable = False)
      email = db.Column(db.String(140), unique = True, nullable = False)
      image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')  
      password = db.Column(db.String(60), nullable = False) 
      permit = db.Column(db.Integer, nullable = False, default = 0)
      #relationship with 'Post' class
      #using backref feature, we can perform a query like - post_1.author despite the fact that 
      #author is not an attr. of Posts object. 
      posts = db.relationship('Post', backref = 'author', lazy = True) 

      def get_reset_token(self, exp_seconds=600):
          stoken = Serializer(app.config['SECRET_KEY'], exp_seconds)
          return stoken.dumps({'user_id':self.id}).decode('utf-8')

      @staticmethod
      def verify_token(token):
          stoken = Serializer(app.config['SECRET_KEY'])
          '''
          try:
              user_id = stoken.loads(stoken)['user_id']
          except:
              None
          '''
          user_id = stoken.loads(token)['user_id']
          return User.query.get(user_id)

      def __repr__(self):
          return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      title = db.Column(db.String(120), nullable = False)
      date_posted = db.Column(db.DateTime, default = datetime.utcnow) 
      content = db.Column(db.Text, nullable = False) 
      #Foreign key = user.id | user = table name for User | table names are in lowercase while class name can be uppercase
      #the user_id attr. of this table references to user.id of the user table / User class (for which user.id is primary key)
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)   

      def __repr__(self):
            return f"Post('{self.title}', '{self.date_posted}')"  


from datetime import datetime
from app import db
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

#followers table to be linked to the user table
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


#this ORM model defines how the users information is stored in the table
#the userMixin is used to get *is_authenticated, *is_active *is_anonymous *get_id() properties from flask_login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    
    #backref used to second rltshp to the mentioned table
    #lazy determines how object is loaded when querried 
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=robohash&s={}'.format(
            digest, size)

    # to give the table a particular name one could add a __tablename__ attrubute to the class

    #defines printing format for class User. More in the case of debugging
    def __repre__(self):
        return '<User {}>'.format(self.username)

    #add follow, unfollow and is following functionality
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repre__(self):
        return '<Post {}>'.format(self.body)

#this helps flask-login load a user. The decorator is registered with flask-login. 
#The id argument is pushed as string form flask-login and so has to be converted accordingly
#guess it populates the current_user variable
@login.user_loader
def load_user(id):
    return User.query.get(int(id))



#flask db migrate m "message"
#flask db upgrade
#user1.followed.append(user2)
#>>> from app import db
#>>> from app.models import User, Post
#u = User(username='john', email='john@example.com')
#>>> db.session.add(u)
#>>> db.session.commit()
from app import db
from passlib.apps import custom_app_context as pwd_context

from app.my_utils import DictSerializable


class Visitor(db.Model, DictSerializable):
    __tablename__ = "visitors"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return 'Email %r' % self.email

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Post(db.Model, DictSerializable):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text = db.Column(db.Text)

    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'))
    # visitor = db.relationship('Visitor', backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return 'Post %r' % self.title
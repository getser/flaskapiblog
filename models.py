from app import db
from app.my_utils import DictSerializable

class Visitor(db.Model, DictSerializable):
    __tablename__ = "visitors"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return 'Email %r' % self.email


class Post(db.Model, DictSerializable):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text = db.Column(db.Text)

    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'))
    visitor = db.relationship('Visitor', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, text, visitor):
        self.title = title
        self.text = text
        self.visitor = visitor

    def __repr__(self):

        # obj = "{'id': %r, 'title': %r, 'text': %r, 'visitor': %r}" % (self.id, self.title, self.text, self.visitor)
        # return obj
        return 'Post %r' % self.title
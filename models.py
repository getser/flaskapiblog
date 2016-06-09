from app import app
from app import db
from passlib.apps import custom_app_context as pwd_context

from app.my_utils import DictSerializable

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


class Visitor(db.Model, DictSerializable):
    __tablename__ = "visitors"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return 'Email %r' % self.email

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        visitor = Visitor.query.get(data['id'])
        return visitor


class Post(db.Model, DictSerializable):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text = db.Column(db.Text)

    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'))
    # visitor = db.relationship('Visitor', backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return 'Post %r' % self.title
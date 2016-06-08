from flask import jsonify
from flask import request, render_template
from app import app
from app import db
from app.models import Visitor, Post


@app.route('/')
def index():
    return "Api is going to be here."


# @app.route('/prereg', methods=['GET', 'POST'])
# def prereg():
#     email = None
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         # Check that email does not already exist (not a great query, but works)
#         if not db.session.query(Visitor).filter(Visitor.email == email).count():
#             reg = Visitor(email, password)
#             db.session.add(reg)
#             db.session.commit()
#             return 'success.html'

#     return "Want register?"


# posts = [
#     {
#         'id': 1,
#         'title': u'My First Post',
#         'body': u'This is my first post about development using FLASK', 
#         'visitor': 1
#     },
#     {
#         'id': 2,
#         'title': u'My Second Post',
#         'body': u'A post about exciting development using FLASK!', 
#         'visitor': 1
#     },
# ]

@app.route('/flaskapiblog/api/v1.0/posts', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    posts = []
    for rec in all_posts:
        posts.append(rec._asdict())
    return jsonify({'posts': posts})


@app.route('/flaskapiblog/api/v1.0/visitors', methods=['GET'])
def get_visitors():
    all_visitors = Visitor.query.all()
    visitors = []
    for rec in all_visitors:
        visitors.append(rec._asdict())
    return jsonify({'visitors': visitors})


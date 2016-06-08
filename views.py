from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import render_template # not used - delete
from app import app
from app import db
from app.models import Visitor, Post


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


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
    # {
        # 'id': 2,
        # 'title': u'My Second Post',
        # 'body': u'A post about exciting development using FLASK!', 
        # 'visitor': 1
    # },
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


@app.route('/flaskapiblog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
        # return "Post %r not found" % post_id
    return jsonify({'post': post._asdict()})


@app.route('/flaskapiblog/api/v1.0/posts', methods=['POST'])
def create_post():
    if not request.json or not 'title' in request.json or not 'text' in request.json or not 'visitor' in request.json :
        abort(400)

    # all_posts = Post.query.all()
    # last_used_id = all_posts[-1].id
    # post = {
    #     'id': last_used_id + 1,
    #     'title': request.json['title'],
    #     'text': request.json.['text'],
    #     'visitor': request.json.['visitor'],
    # }
    # posts.append(post)

    # visitor = Visitor.query.get(int(request.json['visitor']))

    post = Post(
        title=request.json['title'],
        text=request.json['text'],
        visitor_id=int(request.json['visitor'])
        )

    db.session.add(post)
    db.session.commit()

    return jsonify({'post': post._asdict}), 201

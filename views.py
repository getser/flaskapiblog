from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import render_template # not used - delete
from app import app
from app import db
from app.models import Visitor, Post
from app.my_utils import make_api_url # not used - delete

from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.get_password
def get_password(email):
    pass
    # if username == 'miguel':
    #     return 'python'
    # return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return "Api is going to be here."


@app.route('/flaskapiblog/api/v1.0/posts', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    posts = []
    for rec in all_posts:
        posts.append(rec._asdict())
    return jsonify({'posts': posts})


@app.route('/flaskapiblog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return jsonify({'post': post._asdict()})


@app.route('/flaskapiblog/api/v1.0/posts', methods=['POST'])
def create_post():
    if not request.json or not 'title' in request.json or not 'text' in request.json or not 'visitor' in request.json :
        abort(400)

    post = Post(
        title=request.json['title'],
        text=request.json['text'],
        visitor_id=int(request.json['visitor'])
        )

    db.session.add(post)
    db.session.commit()

    return jsonify({'post': post._asdict()}), 201, {'Location': url_for('get_post', post_id=post.id, _external = True)}


# deleting post 6:  curl -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/6
@app.route('/flaskapiblog/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/flaskapiblog/api/v1.0/visitors', methods=['GET'])
def get_visitor():
    all_visitors = Visitor.query.all()
    visitors = []
    for rec in all_visitors:
        visitors.append(rec._asdict())
    return jsonify({'visitors': visitors})


# adding  visitor: curl -i -H "Content-Type: application/json" -X POST -d '{"visitors_email":"email@gov.ua","password":"visitors_password"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors
@app.route('/flaskapiblog/api/v1.0/visitors', methods = ['POST'])
def new_visitor():
    email = request.json.get('email')
    password = request.json.get('password')
    if not (email and password):
        abort(400) # missing arguments
    if Visitor.query.filter_by(email=email).first() is not None:
        abort(400) # existing visitor
    visitor = Visitor(email=email)
    visitor.hash_password(password)
    db.session.add(visitor)
    db.session.commit()
    return jsonify({ 'email': visitor.email }), 201, {'Location': url_for('get_visitor', id = visitor.id, _external = True)}
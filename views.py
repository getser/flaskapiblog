from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import g

from app import app
from app import db
from app.models import Visitor, Post

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    visitor = Visitor.verify_auth_token(email_or_token)
    if not visitor:
        # try to authenticate with username/password
        visitor = Visitor.query.filter_by(email=email_or_token).first()
        if not visitor or not visitor.verify_password(password):
            return False
    g.visitor = visitor
    return True


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return "Api docs is going to be here."


# get all posts: curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts
@app.route('/flaskapiblog/api/v1.0/posts', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    posts = []
    for rec in all_posts:
        posts.append(rec._asdict())
    return jsonify({'posts': posts})


# get post 3: curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/3
@app.route('/flaskapiblog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return jsonify({'post': post._asdict()})


# add post: curl -u ss@gov.ua:ss -i -H "Content-Type: application/json" -X POST -d '{"title":"post title","text":"post text","visitor":"visitors id"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts
@app.route('/flaskapiblog/api/v1.0/posts', methods=['POST'])
@auth.login_required
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


# delete post 6 with email/password: curl -u ss@gov.ua:ss -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/6
# delete post 13 with token: curl -u "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NTQ2NDM1MywiaWF0IjoxNDY1NDYzNzUzfQ.eyJpZCI6NX0.y92RwpJKnfFV_N9GaKooSU9noOJmeK3wAZ0TAc58uuU":none -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/13
@app.route('/flaskapiblog/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'result': True})


# get all visitors: curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors
@app.route('/flaskapiblog/api/v1.0/visitors', methods=['GET'])
def get_visitors():
    all_visitors = Visitor.query.all()
    visitors = []
    for rec in all_visitors:
        visitors.append(rec._asdict())
    return jsonify({'visitors': visitors})


# get visitor 2: curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors/2
@app.route('/flaskapiblog/api/v1.0/visitors/<int:visitor_id>', methods=['GET'])
def get_visitor(visitor_id):
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        abort(404)
    return jsonify({'visitor': visitor._asdict()})


# add visitor: curl -i -H "Content-Type: application/json" -X POST -d '{"visitors_email":"email@gov.ua","password":"visitors_password"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors
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
    return jsonify({ 'email': visitor.email }), 201, {'Location': url_for('get_visitor', visitor_id = visitor.id, _external = True)}


# delete visitor ssss@gov.ua:  curl -u ssss@gov.ua:ssss -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors/6
@app.route('/flaskapiblog/api/v1.0/visitors/<int:visitor_id>', methods=['DELETE'])
@auth.login_required
def delete_visitor(visitor_id):
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        abort(404)
    elif visitor_id != g.visitor.id:
        return jsonify({'error': 'Not allowed'})
    db.session.delete(visitor)
    db.session.commit()
    return jsonify({'result': True})


# get token: curl -u ss@gov.ua:ss -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/token
@app.route('/flaskapiblog/api/v1.0/token')
@auth.login_required
def get_auth_token():
    token = g.visitor.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})
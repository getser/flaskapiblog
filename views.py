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

api_descr = 'This is the REST API based FLASK application. Current API version is 1.0.'
post_descr = 'Post resource gives access to "Post" objects and supports described actions.'
visitor_descr = 'Visitor resource gives access to "Visitor" objects and supports described actions.'
additional = 'Resource examples are explained using "curl" utility.'

post_actions = dict()
visitor_actions = dict()

INFO = {"Description":[api_descr, post_descr, visitor_descr, additional], 'post_actions':post_actions, 'visitors_actions':visitor_actions}

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


# get_all_posts: curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts
post_actions['get all posts'] = "curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts"
@app.route('/flaskapiblog/api/v1.0/posts', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    posts = []
    for rec in all_posts:
        posts.append(rec._asdict())
    return jsonify({'posts': posts})


# get_all_posts_paginated with email/password or token: curl -u ss@gov.ua:ss -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/paginated/<int:page>
# get_all_posts_paginated with email/password or token: curl -u "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NTQ2NDM1MywiaWF0IjoxNDY1NDYzNzUzfQ.eyJpZCI6NX0.y92RwpJKnfFV_N9GaKooSU9noOJmeK3wAZ0TAc58uuU":none -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/paginated/<int:page>
post_actions['get all posts paginated with email/password or token'] = "curl -u visitor_email@gov.ua:visitor_password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/paginated/<int:page>"
@app.route('/flaskapiblog/api/v1.0/posts/paginated/<int:page>', methods=['GET'])
@auth.login_required
def get_all_posts(page):
    all_posts = Post.query.all()
    posts = []
    for rec in all_posts:
        posts.append(rec._asdict())

    # paginator start
    items_per_page = 3       # !! can't be less than 1 !!
    num_items = len(posts)
    num_pages = num_items / items_per_page

    if num_items % items_per_page != 0:
        num_pages += 1

    if page < 1:
        page = 1
    elif page > num_pages:
        page = num_pages

    start = (page - 1) * items_per_page
    finish = page * items_per_page

    if finish > num_items:
        finish = num_items

    posts = posts[start:finish]
    # paginator end

    return jsonify({'posts': posts})


# get_visitors_posts with email/password or token: curl -u ss@gov.ua:ss -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/my_posts
post_actions['get visitors posts with email/password or token'] = 'curl -u visitor_email@gov.ua:visitor_password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/my_posts'
@app.route('/flaskapiblog/api/v1.0/posts/my_posts', methods=['GET'])
@auth.login_required
def get_my_posts():
    all_my_posts = Post.query.filter_by(visitor_id=g.visitor.id)
    posts = []
    for rec in all_my_posts:
        posts.append(rec._asdict())
    return jsonify({'posts': posts})


# get_post 3: curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/3
post_actions['get post'] = 'curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/<int:post_id>'
@app.route('/flaskapiblog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return jsonify({'post': post._asdict()})


# add_post with email/password or token: curl -u ss@gov.ua:ss -i -H "Content-Type: application/json" -X POST -d '{"title":"post title","text":"post text"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts
post_actions['add post with email/password or token'] = '''curl -u ss@gov.ua:ss -i -H "Content-Type: application/json" -X POST -d '{"title":"post title","text":"post text"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts'''
@app.route('/flaskapiblog/api/v1.0/posts', methods=['POST'])
@auth.login_required
def create_post():
    if not request.json or not 'title' in request.json or not 'text' in request.json:
        abort(400)

    post = Post(
        title=request.json['title'],
        text=request.json['text'],
        visitor_id=g.visitor.id
        )

    db.session.add(post)
    db.session.commit()

    return jsonify({'post': post._asdict()}), 201, {'Location': url_for('get_post', post_id=post.id, _external = True)}


# delete_post 6 with email/password: curl -u ss@gov.ua:ss -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/6
post_actions['delete post with email/password or token'] = 'curl -u visitor_token:none -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/13'
@app.route('/flaskapiblog/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'result': True})


# find_posts: curl -i -H "Content-Type: application/json" -X POST -d '{"text":"text to be found"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/find
post_actions['find posts'] = '''curl -i -H "Content-Type: application/json" -X POST -d '{"text":"text to be found"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/find'''
@app.route('/flaskapiblog/api/v1.0/posts/find', methods=['POST'])
def find_posts():
    text_to_find = request.json.get('text')
    found_posts = Post.query.whoosh_search(text_to_find).all()
    posts = []
    for rec in found_posts:
        posts.append(rec._asdict())
    return jsonify({'posts': posts})


# get_all_visitors: curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors
visitor_actions['get all visitors'] = 'curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors'
@app.route('/flaskapiblog/api/v1.0/visitors', methods=['GET'])
def get_visitors():
    all_visitors = Visitor.query.all()
    visitors = []
    for rec in all_visitors:
        visitors.append(rec._asdict())
    return jsonify({'visitors': visitors})


# get_profile with email/password or token: curl -u ss@gov.ua:ss -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors/my_profile
visitor_actions['get profile with email/password or token'] = 'curl -u visitor_email@gov.ua:visitor_password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors/my_profile'
@app.route('/flaskapiblog/api/v1.0/visitors/my_profile', methods=['GET'])
@auth.login_required
def get_profile():
    visitor = g.visitor
    return jsonify({'visitor': visitor._asdict()})


# add_visitor: curl -i -H "Content-Type: application/json" -X POST -d '{"email":"visitors_email@gov.ua","password":"visitors_password"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors
visitor_actions['add visitor'] = '''curl -i -H "Content-Type: application/json" -X POST -d '{"email":"visitors_email@gov.ua","password":"visitors_password"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors'''
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


# delete_visitor ssss@gov.ua:  curl -u ssss@gov.ua:password -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors/6
visitor_actions['delete visitor with email/password or token'] = 'curl -u visitor_token:none -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors/<int:visitor_id>'
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


# get_token: curl -u ss@gov.ua:password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/token
visitor_actions['get token with email/password only'] = 'curl -u visitor_email@gov.ua:visitor_password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/token'
@app.route('/flaskapiblog/api/v1.0/token')
@auth.login_required
def get_auth_token():
    token = g.visitor.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


# This view must be the last one
@app.route('/flaskapiblog/api')
def api_info():
    return jsonify(INFO)

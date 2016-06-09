import os

SECRET_KEY = 'this is my own very very secret key'

SQLALCHEMY_DATABASE_URI = "postgresql://apibloguser:grespas@localhost/apiblog"


basedir = os.path.abspath(os.path.dirname(__file__))
WHOOSH_BASE = os.path.join(basedir, 'search.db')
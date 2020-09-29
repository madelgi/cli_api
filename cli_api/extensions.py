from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_rq2 import RQ


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
redis_db = FlaskRedis()
rq = RQ()

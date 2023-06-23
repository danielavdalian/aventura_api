from datetime import timedelta
import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_cors import CORS
from resources.tributo import blp as TributoBlueprint
from dotenv import load_dotenv

from flask import Flask, render_template

from db import db

app = Flask(__name__)



UPLOAD_FOLDER = '/home/avdalian/img'
load_dotenv()
CORS(app)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Aventura 2023"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL","sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)

api.register_blueprint(TributoBlueprint)
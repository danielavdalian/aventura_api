from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import Flask, flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os

from db import db
from models import TributoModel

from schemas import GetTributosSchema, PostTributosSchema
from marshmallow import Schema, fields

class FileSchema(Schema):
    file = fields.Field(required=True, type="file", description="Archivo a subir")
    custom_filename = fields.Str()

blp = Blueprint("Tributo", __name__, description="Tributo operations") #swagger
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@blp.route("/Tributos")
class Tributos(MethodView):
    @blp.response(200, GetTributosSchema(many=True))
    def get(self):
        return TributoModel.query.order_by(TributoModel.total_points)

@blp.route("/tributo")
class AddTributo(MethodView):
    @blp.arguments(PostTributosSchema)
    @blp.response(201)
    def post(self, tributo_data):
        tributo = TributoModel(
            name=tributo_data["name"],
            district=tributo_data["district"],
            img_src=tributo_data["img_src"]
        )
        try:
            db.session.add(tributo)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Check data")

        return {"msg": f"Tributo with username {tributo.name} created"}, 201

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blp.route("/upload", methods=["POST"])
class UploadImage(MethodView):
    @blp.arguments(FileSchema, location="files")
    @blp.response(201)
    def post(self, file_data):
        if file_data:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                custom_filename = request.form['custom_filename']  # Obtener el valor del campo custom_filename desde el argumento file_data
                if custom_filename:
                    extension = os.path.splitext(filename)[1]
                    filename = secure_filename(custom_filename) + extension  # Usar el valor custom_filename como nombre de archivo
                directory = current_app.config['UPLOAD_FOLDER']
                if os.path.exists(os.path.join(directory, filename)):
                    abort(409, message="El archivo ya existe.")
                os.makedirs(directory, exist_ok=True)
                file.save(os.path.join(directory, filename))

                return {"msg": "Image uploaded"}, 201
            else:
                flash('Archivo no permitido')
                return redirect(request.url)
        else:
            abort(400, message="No se proporcionó ningún archivo")

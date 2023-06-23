from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import Flask, flash, request, redirect, url_for, current_app, send_file, jsonify
from werkzeug.utils import secure_filename
import os

from db import db
from models import TributoModel

from schemas import GetTributosSchema,FileSchema,PostTributosSchema,PuntosSchema
from marshmallow import Schema, fields



blp = Blueprint("Tributo", __name__, description="Tributo operations") #swagger
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@blp.route("/Tributos")
@blp.doc(description='Endpoint to get all the Tributes')
class Tributos(MethodView):
    @blp.response(200, GetTributosSchema(many=True))
    def get(self):
        return TributoModel.query.order_by(TributoModel.total_points)
    
@blp.route("/Tributo/<int:id>")
class TributoById(MethodView):
    @blp.response(200, GetTributosSchema(many=False))
    def get(self, id):
        tributo = TributoModel.query.get(id)
        if tributo is None:
            return {"message": "Tributo not found"}, 404
        else:
            return tributo

    
@blp.route("/tributo")
class AddTributo(MethodView):
    @blp.arguments(PostTributosSchema)
    @blp.doc(description='Endpoint to add a new tribute')
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

@blp.route('/tributo/suma-puntos', methods=['PUT'])
class SumaPuntos(MethodView):
    @blp.arguments(PuntosSchema, location='form')
    @blp.doc(description='Endpoint to add more points')
    @blp.response(201)
    def put(self, puntos):
        puntos_value = puntos['puntos']
        if puntos_value is None:
            return {'error': 'No se proporcionó el valor de puntos'}, 400
        
        errors = PuntosSchema().validate({'puntos': puntos_value})
        if errors:
            return {'error': 'Datos de entrada no válidos'}, 400
        
        id_value = puntos['id']
        tributo = TributoModel.query.get(id_value)
        if tributo is None:
            return {'error': 'El tributo no existe'}, 404
        
        tributo.total_points += int(puntos_value)
        db.session.commit()
        
        return {'msg': f'Se sumaron {puntos_value} puntos al tributo con ID {id_value}. Total de puntos: {tributo.total_points}'}, 200



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blp.route("/uploadImage", methods=["POST"])
class UploadImage(MethodView):
    @blp.arguments(FileSchema, location="files")
    @blp.doc(description='Endpoint to get all the Tributes')
    @blp.response(200)
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
                custom_filename = request.form['custom_filename']
                id = request.form['id']
                if custom_filename:
                    extension = os.path.splitext(filename)[1]
                    filename = secure_filename(custom_filename) + extension  # Usar el valor custom_filename como nombre de archivo
                directory = current_app.config['UPLOAD_FOLDER']
                if os.path.exists(os.path.join(directory, filename)):
                    abort(409, message="El archivo ya existe.")
                os.makedirs(directory, exist_ok=True)
                file.save(os.path.join(directory, filename))
                id_value = request.form['id']
                tributo = TributoModel.query.get(id_value)
                tributo.img_src = filename
                db.session.commit()
                return {"msg": "Image uploaded"}, 201
            else:
                flash('Archivo no permitido')
                return redirect(request.url)
        else:
            abort(400, message="No se proporcionó ningún archivo")


@blp.route('/images/<image_name>')
@blp.doc(description='Endpoint to get a image')
def get_image(image_name):
    # Ruta de la carpeta donde se encuentran las imágenes
    image_folder = current_app.config['UPLOAD_FOLDER']  
    try:
        return send_file(f"{image_folder}/{image_name}", mimetype='image/jpeg')
    except FileNotFoundError:
        return 'Imagen no encontrada', 404
    
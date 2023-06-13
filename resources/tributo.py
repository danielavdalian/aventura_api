from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import TributoModel

from schemas import GetTributosSchema
from schemas import PostTributosSchema

blp = Blueprint("Tributo", __name__, description="Tributo operations") #swagger

@blp.route("/Tributos")
class Tributos(MethodView):
    @blp.response(200,GetTributosSchema(many=True))
    def get(self):
        return TributoModel.query.order_by(TributoModel.total_points)
    


@blp.route("/tributo")
class AddTributo(MethodView):
    @blp.arguments(PostTributosSchema)
    @blp.response(201)
    def post(self,tributo_data):

        tributo = TributoModel(
            name = tributo_data["name"],
            district = tributo_data["district"],
            img_src = tributo_data["img_src"]
        )
        try:
            db.session.add(tributo)
            db.session.commit()
        except IntegrityError:
            abort(400,message="Check data")

        return {"msg" : f"Tributo with username {tributo.name} created"}, 201  

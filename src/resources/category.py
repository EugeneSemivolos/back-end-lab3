import uuid
from flask import Blueprint, jsonify, request
from ..schemas.Schemas import categorySchema
from sqlalchemy.exc import IntegrityError
from ..models.category import categoryModel
from ..db import db

category_blueprint = Blueprint('category', __name__)

@category_blueprint.get("/category")
def categories_get():
    categories_list = categoryModel.query.all()
    schema = categorySchema()
    return schema.dump(obj=categories_list, many=True)

@category_blueprint.post("/category")
def create_category():
    category_data = request.args
    category_schema = categorySchema()
    try:
        validated_data = category_schema.load(category_data)
    except Exception as e:
        return "Incorrect category data", 400
    validated_data["id"] = uuid.uuid4().hex
    category = categoryModel(**validated_data)
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "A category with this name already exists", 400
    return validated_data

@category_blueprint.delete("/category/<category_id>")
def category_delete(category_id):
    category = categoryModel.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return "", 204
    else:
        return "Category not found", 404
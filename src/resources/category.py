import uuid
from src import app
from flask import jsonify, request
from ..schemas.Schemas import categorySchema

categories = {}

@app.get("/category")
def categories_get():
    return list(categories.values())

@app.post("/category")
def create_category():
    category_data = request.args
    category_schema = categorySchema()
    try:
        validated_data = category_schema.load(category_data)
    except Exception as e:
        return "Incorrect category data", 400
    validated_data["id"] = uuid.uuid4().hex
    categories[validated_data["id"]] = validated_data
    return validated_data

@app.delete("/category/<category_id>")
def category_delete(category_id):
    if category_id in categories:
        del categories[category_id]
        return "", 204
    else:
        return "Category not found", 404
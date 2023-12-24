import uuid
from src import app
from flask import jsonify, request
import datetime

users = {}
categories = {}
records = {}

@app.get("/user/<user_id>")
def user_get(user_id):
    if(user_id in users):
        return users[user_id]
    else:
        return "User not found", 404

@app.get("/users")
def users_get():
    return list(users.values())

@app.post("/user")
def create_user():
    user_name = request.args.get("name")
    user_id = uuid.uuid4().hex
    user = {
        "id": user_id,
        "user_name":user_name
    }
    users[user_id] = user
    return user

@app.delete("/user/<user_id>")
def user_delete(user_id):
    if(user_id in users):
        del users[user_id]
        return "", 204
    else:
        return "User not found", 404


@app.get("/category")
def categories_get():
    return list(categories.values())

@app.post("/category")
def create_category():
    category_name = request.args.get("name")
    category_id = uuid.uuid4().hex
    category = {
        "id": category_id,
        "category_name":category_name
    }
    categories[category_id] = category
    return category

@app.delete("/category/<category_id>")
def category_delete(category_id):
    if category_id in categories:
        del categories[category_id]
        return "", 204
    else:
        return "Category not found", 404


@app.get("/record")
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")

    if user_id is None and category_id is None:
        return "Missing parameters", 400

    filtered_records = []
    for record in records.values():
        if (user_id is None or record.get("user_id") == user_id) and (category_id is None or record.get("category_id") == category_id):
            filtered_records.append(record)

    return jsonify(filtered_records)

@app.post("/record")
def create_record():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    record_id = uuid.uuid4().hex
    created_at = datetime.datetime.now().isoformat()
    amount = request.args.get("amount")

    record = {
        "id": record_id,
        "user_id":user_id,
        "category_id":category_id,
        "created_at": created_at,
        "amount": amount
    }
    records[record_id] = record
    return record

@app.delete("/record/<record_id>")
def record_delete(record_id):
    if record_id in records:
        del records[record_id]
        return "", 204
    else:
        return "Record not found", 404

if __name__ == "__main__":
    app.run()
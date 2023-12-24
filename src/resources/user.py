import datetime
import uuid
from src import app
from flask import jsonify, request
from ..schemas.Schemas import userSchema

users = {}

@app.post("/user")
def create_user():
    user_data = request.args
    user_schema = userSchema()
    try:
        validated_data = user_schema.load(user_data)
    except Exception as e:
        return "Incorrect user data", 404
    validated_data["id"] = uuid.uuid4().hex
    users[validated_data["id"]] = validated_data
    return validated_data

@app.delete("/user/<user_id>")
def user_delete(user_id):
    if(user_id in users):
        del users[user_id]
        return "", 204
    else:
        return "User not found", 404

@app.get("/user/<user_id>")
def user_get(user_id):
    if(user_id in users):
        return users[user_id]
    else:
        return "User not found", 404

@app.get("/users")
def users_get():
    return list(users.values())

@app.get("/healthcheck")
def healthcheck():
    time = datetime.datetime.now().isoformat()
    health = "It`s works!"
    data = {
        "time": time,
        "health": health
    }
    return jsonify(data)
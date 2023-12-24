import uuid
from src import app
from flask import jsonify, request
from ..schemas.Schemas import recordSchema
import datetime

records = {}

@app.post("/record")
def create_record():
    record_data = request.args
    record_schema = recordSchema()
    try:
        validated_data = record_schema.load(record_data)
    except Exception as e:
        return "Incorrect record data", 400

    validated_data["id"] = uuid.uuid4().hex
    validated_data["created_at"] = datetime.datetime.now().isoformat()
    records[validated_data["id"]] = validated_data

    return validated_data

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

@app.delete("/record/<record_id>")
def record_delete(record_id):
    if record_id in records:
        del records[record_id]
        return "", 204
    else:
        return "Record not found", 404
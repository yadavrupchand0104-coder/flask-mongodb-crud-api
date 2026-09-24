from flask import Flask, jsonify, request
from pymongo import MongoClient
import config

app=Flask(__name__)

#connecting to mongoDB

client = MongoClient(config.MONGO_URL)
db = client[config.DB_NAME]
collection = db[config.COLLECTION_NAME]

@app.route('/employees', methods=['POST'])
def add_emp():
    data = request.json

    if not data.get('name'):
        return {"error": "Name is required"}, 400

    result = collection.insert_one(data)
    return {"message": "Employee added successfully", "id": str(result.inserted_id)}, 201

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = []
    for emp in collection.find():
        emp["_id"] = str(emp["_id"])  # Convert ObjectId to string
        employees.append(emp)
    return jsonify(employees)

if __name__ == '__main__':
    app.run(debug=True)
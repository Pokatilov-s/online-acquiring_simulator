"""Взаимодействие с Mongodb напрямую через pymongo"""
import uuid
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mongo_db']
collection = db['description_payment']


def insert_description(description, payment_id):
    """Добавить запись описания"""
    data = {
        "_id": str(uuid.uuid4()),
        "payment_id": str(payment_id),
        "description": description
    }
    record = collection.insert_one(data)
    return record.inserted_id


def read_description(pk):
    """Прочитать запись описания"""
    record = collection.find_one({'_id': str(pk)})
    return record

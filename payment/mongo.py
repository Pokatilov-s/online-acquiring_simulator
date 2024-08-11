"""Взаимодействие с Mongodb напрямую через pymongo"""
import uuid
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mongo_db']


def insert_description(description, payment_id):
    """Добавить запись описания"""
    collection = db['description_payment']
    data = {
        "_id": str(uuid.uuid4()),
        "payment_id": str(payment_id),
        "description": description
    }
    record = collection.insert_one(data)
    return record.inserted_id


def read_description():
    """Прочитать запись описания"""
    pass

from app import mongo
from bson import ObjectId
from datetime import datetime

class Person:
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save person to MongoDB"""
        return mongo.db.people.insert_one({
            'name': self.name,
            'age': self.age,
            'job': self.job,
            'created_at': self.created_at
        })
    
    @staticmethod
    def get_all():
        """Get all people from MongoDB"""
        return list(mongo.db.people.find())
    
    @staticmethod
    def get_by_id(pid):
        """Get person by ID"""
        return mongo.db.people.find_one({'_id': ObjectId(pid)})
    
    @staticmethod
    def delete_by_id(pid):
        """Delete person by ID"""
        return mongo.db.people.delete_one({'_id': ObjectId(pid)})
    
    def __repr__(self):
        return f'Person with name {self.name} and age {self.age}'
# -*- coding:utf-8 -*-
from ext import db

class User(db.Model):
    __tablename__ = 'users2'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(128))

    def __init__(self, name, address):
        self.name = name
        self.address = address

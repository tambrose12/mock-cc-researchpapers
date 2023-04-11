import json
from os import environ
from flask import request

from app import app
from models import db, Restaurant, RestaurantPizza, Pizza

class TestApp:
    '''Flask application in app.py'''

    
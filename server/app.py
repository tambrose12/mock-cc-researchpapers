#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


# @app.route('/')
# def index():
#     return '<h1>Code challenge</h1>'

class Home(Resource):
    def get(self):
        msg = {'msg': 'Code Challenge'}

        response = make_response(msg, 200)
        return response


api.add_resource(Home, '/')


# @app.route('/research')
# def restaurants():
#     pass

class Researches(Resource):
    def get(self):
        research = [r.to_dict(only=('id', 'topic', 'year', 'page_count'))
                    for r in Research.query.all()]

        response = make_response(research, 200)
        return response


api.add_resource(Researches, '/researches')


class ResearchesById(Resource):
    def get(self, id):
        research = Research.query.filter_by(id=id).first()
        response = make_response(research.to_dict(), 200)
        return response


api.add_resource(ResearchesById, '/researches/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

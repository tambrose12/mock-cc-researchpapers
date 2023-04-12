#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

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
        if research == None:
            return make_response({"error": "Research paper not found"}, 404)

        response = make_response(research.to_dict(), 200)
        return response

    def delete(self, id):
        research = Research.query.filter_by(id=id).first()
        if research == None:
            return make_response({"error": "Research paper not found"}, 404)

        db.session.delete(research)
        db.session.commit()
        return make_response({"message": "Research paper Deleted"}, 201)


api.add_resource(ResearchesById, '/researches/<int:id>')


class Authors(Resource):
    def get(self):
        authors = [a.to_dict(only=('id', 'name', 'field_of_study'))
                   for a in Author.query.all()]
        return make_response(authors, 200)


api.add_resource(Authors, '/authors')


class ResearchAuthor(Resource):
    def get(self):
        research_auths = [ra.to_dict() for ra in ResearchAuthors.query.all()]

        return make_response(research_auths, 200)

    def post(self):
        data = request.get_json()
        new_research_auth = ResearchAuthors(
            author_id=data['author_id'], research_id=data['research_id'])

        db.session.add(new_research_auth)
        db.session.commit()

        if new_research_auth.authors == None:
            db.session.rollback
            return make_response({'errors': 'validation errors'}, 500)
        elif new_research_auth.researches == None:
            db.session.rollback
            return make_response({'errors': 'validation errors'}, 500)

        author = new_research_auth.to_dict(
            only=('authors.name', 'authors.id', 'authors.field_of_study'))
        return make_response(author, 201)


api.add_resource(ResearchAuthor, '/research_authors')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

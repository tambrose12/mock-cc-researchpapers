from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here


class Research(db.Model, SerializerMixin):
    __tablename__ = 'researches'

    serialize_rules = ('-research_authors.researches',
                       '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_authors = db.relationship('ResearchAuthors', backref='researches')

    @validates('year')
    def validate_year(self, key, year):
        if len(str(year)) < 4:
            raise AssertionError('Must be a 4 digit year.')

        return year


class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    serialize_rules = ('-research_authors.authors',
                       '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_authors = db.relationship('ResearchAuthors', backref='authors')

    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        studies = ['AI', 'Robotics', 'Machine Learning',
                   'Vision', 'Cybersecurity']
        if field_of_study not in studies:
            raise AssertionError(
                'Field of Study must be on the approved list.')

        return field_of_study


class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'

    serialize_rules = ('-created_at', '-updated_at',
                       '-authors.research_authors', '-research.research_authors')

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

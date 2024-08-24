from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    birth_year = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    homeworld = db.Column(db.Integer, db.ForeignKey('planet.id'))
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "homeworld": self.homeworld,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer)
    gravity = db.Column(db.String(40))
    climate = db.Column(db.String(40))
    terrain = db.Column(db.String(40))
    population = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    person = db.Column(db.Integer, db.ForeignKey('person.id'))
    planet = db.Column(db.Integer, db.ForeignKey('planet.id'))

    
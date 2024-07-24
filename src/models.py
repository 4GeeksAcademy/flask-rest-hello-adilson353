from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    # Relaciones corregidas
    favorites_people = db.relationship('People_Favorite', back_populates='user')
    favorites_planets = db.relationship('Planets_Favorite', back_populates='user')

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
            # no serializar la contraseña, es una brecha de seguridad
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    height = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    created = db.Column(db.String(80), unique=False, nullable=False)
    diameter = db.Column(db.String(80), unique=False, nullable=False)
    edited = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<Planets {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "climate": self.climate,
            "created": self.created,
            "diameter": self.diameter,
            "edited": self.edited,
            "name": self.name
        }

class People_Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='favorites_people')
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship('People')

    def __repr__(self):
        return f"{self.user.first_name} likes {self.people.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": self.user.first_name,
            "people_id": self.people_id,
            "people": self.people.name
        }

class Planets_Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='favorites_planets')
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets')

    def __repr__(self):
        return f"{self.user.first_name} likes {self.planets.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": self.user.first_name,
            "planet_id": self.planet_id,
            "planets": self.planets.name
        }

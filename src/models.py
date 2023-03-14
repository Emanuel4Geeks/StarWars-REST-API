from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    nombre = db.Column(db.String(255))
    apellido = db.Column(db.String(255))
    favoritos_user = db.relationship('Favoritos', backref='user', lazy=True)

    def __repr__(self):
        return '%r' % self.email

    def favorite_list(self):
        return list(map(lambda item: item.dataUserFav(), self.favoritos_user))

    def serialize(self):

        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "active": self.is_active
            # do not serialize the password, its a security breach
        }


class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.String, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    planeta_origen_id = db.Column(db.Integer, db.ForeignKey('planeta.id'))
    favoritos_personaje = db.relationship(
        'Favoritos', backref='personaje', lazy=True)

    def __repr__(self):
        return '%r' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "peso": self.peso,
            "fecha_nacimiento": self.fecha_nacimiento,
            "genero": self.genero
        }


class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    diametro = db.Column(db.Integer, nullable=False)
    clima = db.Column(db.String(100), nullable=False)
    terreno = db.Column(db.String(100), nullable=False)
    gravedad = db.Column(db.String(100), nullable=False)
    poblacion = db.Column(db.Integer, nullable=False)
    favoritos_planeta = db.relationship(
        'Favoritos', backref='planeta', lazy=True)
    personaje_planeta = db.relationship(
        'Personaje', backref='planeta', lazy=True)

    def __repr__(self):
        return '%r' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "diametro": self.diametro,
            "clima": self.clima,
            "terreno": self.terreno,
            "gravedad": self.gravedad,
            "poblacion": self.poblacion
        }


class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    personaje_id = db.Column(
        db.Integer, db.ForeignKey('personaje.id'), nullable=True)
    planeta_id = db.Column(
        db.Integer, db.ForeignKey('planeta.id'), nullable=True)

    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def dataUserFav(self):
        return {
            "id": self.id,
            "personaje_id": self.personaje_id,
            "planeta_id": self.planeta_id
        }

    def serialize(self):

        user = User.query.filter_by(id=self.user_id).first().serialize()

        personaje = Personaje.query.filter_by(id=self.personaje_id).first()
        if personaje is not None:
            personaje = planeta.serialize()
        else:
            personaje = ""

        planeta = Planeta.query.filter_by(id=self.planeta_id).first()
        if planeta is not None:
            planeta = planeta.serialize()
        else:
            planeta = ""

        return {
            "id": self.id,
            "user": user,
            "personaje": personaje,
            "planeta": planeta
        }

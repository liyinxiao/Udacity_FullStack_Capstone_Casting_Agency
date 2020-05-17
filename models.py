import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# database_name = "casting_agency"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = os.environ.get('DATABASE_URL')
db = SQLAlchemy()

def setup_db(app, db_path=database_path):
	app.config["SQLALCHEMY_DATABASE_URI"] = database_path
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)
	db.create_all()


def db_drop_and_create_all():
		db.drop_all()
		db.create_all()


class Actor(db.Model):
	__tablename__ = 'Actor'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	gender = db.Column(db.String, nullable=False)

	def get_name(self):
		return self.name

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'age': self.age,
			'gender': self.gender
		}


class Movie(db.Model):
	__tablename__ = 'Movie'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	release_date = db.Column(db.DateTime(), default=datetime.utcnow)

	def get_title(self):
		return self.title

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
			'id': self.id,
			'title': self.title,
			'release_date': self.release_date
		}

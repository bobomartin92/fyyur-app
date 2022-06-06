from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
		__tablename__ = 'Venue'

		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String, nullable=False, unique=True)
		city = db.Column(db.String(120), nullable=False)
		state = db.Column(db.String(120), nullable=False)
		address = db.Column(db.String(120), nullable=False)
		phone = db.Column(db.String(120), nullable=False)
		genres = db.Column(db.ARRAY(db.String), nullable=False)
		image_link = db.Column(db.String(500), nullable=False)
		facebook_link = db.Column(db.String(120), nullable=False)
		website = db.Column(db.String(120))
		seeking_talent = db.Column(db.Boolean, default=False)
		seeking_description = db.Column(db.String(120))
		shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")

		def __repr__(self) -> str:
			return f'<Venue name={self.name} >'
		

class Artist(db.Model):
		__tablename__ = 'Artist'

		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String)
		city = db.Column(db.String(120))
		state = db.Column(db.String(120))
		phone = db.Column(db.String(120))
		genres = db.Column(db.ARRAY(db.String), nullable=False)
		image_link = db.Column(db.String(500))
		facebook_link = db.Column(db.String(120))
		website = db.Column(db.String(120))
		seeking_venue = db.Column(db.Boolean, default=False)
		seeking_description = db.Column(db.String(120))
		shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")

		def __repr__(self) -> str:
			return f'<Artist name={self.name} >'


class Show(db.Model):
		__tablename__ = 'Show'
		
		id = db.Column(db.Integer, primary_key=True)
		venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
		artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
		start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


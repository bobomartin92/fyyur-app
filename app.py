#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
from datetime import datetime
import dateutil.parser
import babel
from flask import (
	Flask, 
	jsonify, 
	render_template, 
	request, 
	flash, 
	redirect, 
	url_for
)
from flask_moment import Moment
from flask_migrate import Migrate
from dotenv import load_dotenv
from logging import Formatter, FileHandler
from forms import *
from model import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

load_dotenv()
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):

	date = dateutil.parser.parse(value)

	if format == 'full':
			format="EEEE MMMM, d, y 'at' h:mma"
	elif format == 'medium':
			format="EE MM, dd, y h:mma"
	return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
	return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

	data = []
	venues = Venue.query.order_by('city').all()

	data.append({
					"city": venues[0].city,
					"state": venues[0].state,
					"venues": []
				})

	for venue in venues:
		for d in data:
			if d['city'] == venue.city:
				d['venues'].append({
					'id': venue.id,
					'name': venue.name,
					"num_upcoming_shows": len(
						[
							show for show in venue.shows 
							if show.start_time > datetime.now()
						]
					),
				})
				break
		else:
			data.append({
				"city": venue.city,
				"state": venue.state,
				"venues": [{
				'id': venue.id,
				'name': venue.name,
				"num_upcoming_shows": len(
						[
							show for show in venue.shows 
							if show.start_time > datetime.now()
						]
					),
				}]
			})

	return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():

	venues = Venue.query.filter(
		Venue.name.ilike(f'%{request.form["search_term"]}%')
	)
	
	response = {
		'count': venues.count(),
		'data': venues.all()
	}

	return render_template(
		'pages/search_venues.html', 
		results=response, 
		search_term=request.form.get('search_term', '')
	)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

	venue = Venue.query.get(venue_id)
	shows = venue.shows
	current_time  = datetime.now()
	
	venue.past_shows = [{
		'artist_id': show.artist_id,
		"artist_name": show.artist.name,
		"artist_image_link": show.artist.image_link,
		"start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
	} for show in shows if current_time > show.start_time]

	venue.upcoming_shows = [{
		'artist_id': show.artist_id,
		"artist_name": show.artist.name,
		"artist_image_link": show.artist.image_link,
		"start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
	} for show in shows if current_time < show.start_time]

	venue.past_shows_count = len(venue.past_shows)
	venue.upcoming_shows_count = len(venue.upcoming_shows)


	return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
	form = VenueForm()
	return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
	form = VenueForm(request.form)

	try: 
		venue = Venue()
		form.populate_obj(venue)
		venue.genres = request.form.getlist('genres')
		db.session.add(venue)
		db.session.commit()

		flash('Venue ' + request.form['name'] + ' was successfully listed!')
	except:
	
		db.session.rollback()
		print(sys.exc_info())
		flash(f'An error occurred. Venue {venue.name} could not be listed.')

	finally:
		db.session.close()
	return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):

	try:
		venue = Venue.query.get(venue_id)
		db.session.delete(venue)
		db.session.commit()
	except:
		db.session.rollback()
		print(sys.exc_info)
	finally:
		db.session.close()

	return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

	artists = Artist.query.all()

	return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():

	artists = Artist.query.filter(
		Artist.name.ilike(f'%{request.form["search_term"]}%')
	)
	
	response = {
		'count': artists.count(),
		'data': artists.all()
	}
	return render_template(
		'pages/search_artists.html', 
		results=response, 
		search_term=request.form.get('search_term', '')
	)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

	artist = Artist.query.get(artist_id)
	shows = artist.shows
	current_time  = datetime.now()
	
	artist.past_shows = [{
		'venue_id': show.venue_id,
		"venue_name": show.venue.name,
		"venue_image_link": show.venue.image_link,
		"start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
	} for show in shows if current_time > show.start_time]

	artist.upcoming_shows = [{
		'venue_id': show.venue_id,
		"venue_name": show.venue.name,
		"venue_image_link": show.venue.image_link,
		"start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
	} for show in shows if current_time < show.start_time]

	artist.past_shows_count = len(artist.past_shows)
	artist.upcoming_shows_count = len(artist.upcoming_shows)
	

	return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
	artist = Artist.query.get(artist_id)

	form = ArtistForm(
		name=artist.name,
		genres=artist.genres,
		city=artist.city,
		state=artist.state,
		phone=artist.phone,
		website_link=artist.website,
		facebook_link=artist.facebook_link,
		image_link=artist.image_link,
		seeking_venue=artist.seeking_venue,
		seeking_description=artist.seeking_description,
	)

	return render_template(
		'forms/edit_artist.html', form=form, artist=artist
	)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

	form = ArtistForm(request.form)
	try:
		artist = Artist.query.get(artist_id)
		form.populate_obj(artist)
		artist.genres = request.form.getlist('genres')
		db.session.commit()
	except:
		db.session.rollback()
		print(sys.exc_info())
	finally:
		db.session.close()

	return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
	
	venue = Venue.query.get(venue_id)
	form = VenueForm(
		name=venue.name,
		genres=venue.genres,
		address=venue.address,
		city=venue.city,
		state=venue.state,
		phone=venue.phone,
		website_link=venue.website,
		facebook_link=venue.facebook_link,
		image_link=venue.image_link,
		seeking_talent=venue.seeking_talent,
		seeking_description=venue.seeking_description,
	)
	
	return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

	form = VenueForm(request.form)
	try:
		venue = Venue.query.get(venue_id)
		form.populate_obj(venue)
		venue.genres = request.form.getlist('genres')
		db.session.commit()
	except:
		db.session.rollback()
		print(sys.exc_info())
	finally:
		db.session.close()
	return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
	form = ArtistForm()
	return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

	form = ArtistForm(request.form)

	try: 
		artist = Artist()
		form.populate_obj(artist)
		artist.genres = request.form.getlist('genres')
		db.session.add(artist)
		db.session.commit()

		flash('Artist ' + request.form['name'] + ' was successfully listed!')
	except:

		db.session.rollback()
		print(sys.exc_info())
		flash(f'An error occurred. Artist {artist.name} could not be listed.')

	finally:
		db.session.close()

	return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():


	shows = Show.query.order_by('start_time').all()
	data = [{
		"venue_id": show.venue_id,
		"venue_name": show.venue.name,
		"artist_id": show.artist_id,
		"artist_name": show.artist.name,
		"artist_image_link": show.artist.image_link,
		"start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
	} for show in shows]

	return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
	form = ShowForm()
	return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

	form = ShowForm(request.form)
	try:

		show = Show()
		form.populate_obj(show)
		db.session.add(show)
		db.session.commit()

		flash('Show was successfully listed!')
	except:
		db.session.rollback()
		print(sys.exc_info())
		flash('An error occurred. Show could not be listed.')

	finally:
		db.session.close()

	return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
		return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
		return render_template('errors/500.html'), 500


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
		app.run(debug=True)

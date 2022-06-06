## Fyyur - Project

## Introduction

This App is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

I built out the data models to power the API endpoints for this web application by connecting to a PostgreSQL database for storing, querying, and creating information about artists, venues and shows.

## Functionality

This is a web app with the backend built with Python Flask, the database was setup with relational database (Postgres) and with full CRUD functionality.

- creating new venues, artists, and shows.
- searching for venues and artists.
- get information about specific artist or venue.
- Updating venues and artist data
- Deleting Venues

## App Dependencies

Create a .env file and add SQLALCHEMY_DATABASE_URI = postgres uri
run "flask db init", "flask db migrate" and "flask db upgrade" to create tables and columns in created database.
The dependencies we need to install with "pip3 install -r requirements.txt"

Overall:

- Models are located in the `model.py`.
- Controllers are also located in `app.py`.

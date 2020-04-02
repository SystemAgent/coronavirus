# Coronavirus Bulgaria

## Purpose

The purpose of the project is to provide accurate and up-to date data and
analysis on the Coronavirus pandemic with a focus on Bulgaria.

## Development setup

	pip install virtualenv
	virtualenv -p python3 env
	source ./env/bin/activate
	python setup.py develop
	cp coronavirus/local_settings.py.example coronavirus/local_settings.py

Create database and populate defined constants in `coronavirus/local_settings.py`.

	./manage.py migrate

## Fill Database with virus spread for country:

	python manage.py country_spread <"country">

Example:

	python manage.py country_spread Bulgaria

## Fill Database with all Europe data

	bash scripts/fill_total_database.sh

## Fill Database with tweets from a user:

	python manage.py get_twitter_data <"user_id"> <'tweet_id'>

Example:

	python manage.py get_twitter_data 3769353255 1242365860980949002

The tweet_id is needed for querying the Twitter API usefully, 
and will provide all tweets since that tweet_id provided in the command.

## Run Development Server

	./manage.py runserver

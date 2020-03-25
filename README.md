# Coronavirus Bulgaria

## Purpose

The purpose of the project is to provide accurate and up-to date data and analysis on the Coronavirus pandemic 
with a focus on Bulgaria.

## Development setup
	```
	#Install virtualenv 
	pip install virtualenv

	#Create virtualenv for project
	virtualenv -p python3.7 env

	#Activate virtualenv
	source ./env/bin/activate
	
	python setup.py develop


Create `.env` file in root path replacing the bracketed values:

	POSTGRES_USER=<USERNAME>
	POSTGRES_PASS=<PASSWORD>
	POSTGRES_HOST=<HOST>
	POSTGRES_DB=<NAME>

## Fill Database with virus spread for country:

	python manage.py country_spread <"country">

	Example:
		python manage.py country_spread Bulgaria
	
## Fill Database with tweets from a user:

	python manage.py get_twitter_data <"user_id"> <'tweet_id'>

	Example:
		python manage.py get_twitter_data 3769353255 1242365860980949002
		
	The tweet_id is needed for querying the Twitter API usefully, 
	and will provide all tweets since that tweet_id provided in the command.

## Migrations

	Run:
		python manage.py migrate
	
	Create:
		python manage.py makemigrations --name <"something">

	Reverse:
		python manage.py migrate coronavirus_bg <"number">

	Reverse all migration:
		python manage.py migrate coronavirus_bg zero

## Run Development Server

	python manage.py runserver 8080

	http://localhost:8080/home/

	http://localhost:8000/admin/, 

# Telegram bot for finance tracking

## General info

This is a simple bot for telegram which can store your spendings inside mongoDB. You can customize pretty much everything inside the bot. Also it has a built-in intergration with google-sheets.


## Installation

To get the bot running simply clone this repo and follow these steps:

1. Create .env file with "MONGO_INITDB_ROOT_USERNAME" and "MONGO_INITDB_ROOT_PASSWORD" inside
2. Copy "settings.py.template" as "settings.py" within bot/ directory and populate with the settings of your liking
3. If you want a google sheet integration follow this guide https://medium.com/craftsmenltd/from-csv-to-google-sheet-using-python-ef097cb014f9 and place your "client_secret.json" inside bot/ directory
4. Build the image with 
	```
	docker build -t finbot:latest .
	```
5. Launch the application with 
	```
	docker-compose up -d
	```
	
## Notes

Just a few things you need to know about this storage in general:
* Please expect bugs here, the whole thing was made for my personal usage mostly, but if you'll follow steps described above it should work on your machine too.
* If you want to use "/" command add the following to your bot via botfather
	```
	get_this_month - sometext
	get_last_30 - sometext
	export_to_csv - sometext
	```

# Contacts App

## RESTful API for Managing Contacts


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://linkedin.com/in/fuakye-akyempim-charles)

Contacts App is a set of RESTful APIs that can allow us to utilize an internationally recognized set of contact/records.

DRF-YASG-powered API Documentation.

- Visit `localhost:8001`
- See Documentation in Browser
- ✨Magic ✨

## Features

- Create a new contact/record
- Edit an existing contact/record record
- List contact/records in batches of 20 (and paginate through the rest of the record)
- Retrieve contact/records by ID
- Delete a contact/record by ID
- Upload CSV containing contact record and receive an email after processing is done

## Project Setup

Contact App requires the docker and docker-compose to run

### Unix system or unix like terminal

```sh
git clone https://github.com/KwameSwift/contact-app.git
cd contact-app
touch .env
# Create an env file of the format illustrated in the .env.example, in the root folder
docker-compose up -d --build

# To view logs
docker logs --follow contact-app_web_1
```

Voilà ✨✨ - The app is up and running

### Windows system

```sh
git clone https://github.com/KwameSwift/contact-app.git
cd contact-app
# Create an env file of the format illustrated in the .env.example, in the root folder
docker-compose up -d --build

# To view logs
docker logs --follow contact-app_web_1
```
Voilà ✨✨ - The app is up and running

## Documentation

With the app running visit `localhost:8001` in your browser to view documentation and interact with it.

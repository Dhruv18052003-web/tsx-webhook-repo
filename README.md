# tsx-webhook-repo

# Dev Assessment - Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)


## Setup ngrok


* Step 1: Download ngrok for windows (64 bit)
    https://dashboard.ngrok.com/get-started/setup/windows

* Step 2: Sign up and get the token generated.

```bash
ngrok config add-authtoken 2zIzqFdJBDNAqe0PJUnvzaIWTFD_691tUj7pwoMhSSL6s2x9Q
```

*Step 3: Deploy your app online:

```bash
ngrok http http://127.0.0.1:5000
```
Forwarding url will be displayed.
Example: https://ed65-103-254-245-34.ngrok-free.app -> http://127.0.0.1:5000   

## Prepare MongoDB Container

* Pull the MongoDB Docker image
```bash
docker pull mongo
```

* Run MongoDB container

```bash
docker run -d --name my-mongo -p 27017:27017 -v mongodbdata:/data/db -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=Dhruv@1805 mongo
```

* verify it is running
```bash
docker ps
```

* Stop & remove container (if needed)
```bash
docker stop my-mongo
docker rm my-mongo
```

## Download and configure MongoDB client

* URL to Download MongoDB Compass
https://www.mongodb.com/try/download/compass

* Connecto MongoDB 
mongodb://admin:Dhruv@1805@localhost:27017

## How to test?

* Run app.py

```bash
python app.py
```

* check root: Open web browser & type following url
https://ed65-103-254-245-34.ngrok-free.app

it shows following message
welcome buddy

* check echo: open web browser & trype following url

https://ed65-103-254-245-34.ngrok-free.app/v1/sys/echo?fname=Dhruv&lname=Joshi

it shows:
{"fname":"Dhruv","lname":"Joshi"}






*******************
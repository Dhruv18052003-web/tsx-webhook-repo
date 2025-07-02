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
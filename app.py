from flask import json , request, Flask 
from app.libs.route import register_all_routes

# create Flask application
app = Flask(__name__)

# add all routes 
register_all_routes(app)

if __name__ == '__main__':
    app.run(debug=False)
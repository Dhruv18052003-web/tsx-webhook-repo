from flask import json , request, Flask 
from app.libs.route import register_all_routes
from app.libs.config import Config 
from app.libs.logger import Logging
from loguru import logger

# create Flask application with static folder configuration
app = Flask(__name__, static_folder='app/static', static_url_path='/static')

# add all routes 
register_all_routes(app)

# Load configuration
app.config.from_object(Config)

# Set up logging
Logging.configure_logging()

# this line of code records api call with request payload to sys.log file
@app.before_request
def log_request():
    logger.bind(system=True).info(
        f"[{request.method}] {request.path} from {request.remote_addr} [query string] {request.query_string} [payload] {request.data}\n\n"
)

if __name__ == '__main__':
    app.run(debug=False)
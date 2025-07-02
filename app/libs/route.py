from flask import Blueprint
from app.modules.sys.controllers import sys as sys_controller
from app.modules.git.controllers import actions as git_controller

def register_all_routes(app):

    # Root Controllers
    root_routes = Blueprint('root_routes', __name__, url_prefix='/')

    @root_routes.route('', methods=['GET'])
    def home():
        return sys_controller.home()
    
    app.register_blueprint(root_routes)

    # System controlers
    sys_routes = Blueprint('sys_routes', __name__, url_prefix='/v1/sys')

    @sys_routes.route('/echo', methods=['GET'])
    def echo():
        return sys_controller.echo()
    
    app.register_blueprint(sys_routes)

    # Github Controllers
    git_routes = Blueprint('git_routes', __name__, url_prefix='/v1/git')

    # capture pull action
    @git_routes.route('/pull', methods=['POST'])
    def pull():
        return git_controller.pull()
    
    # capture push action
    @git_routes.route('/push', methods=['POST'])
    def push():
        return git_controller.push()
    
    # capture merge action
    @git_routes.route('/merge', methods=['POST'])
    def merge():
        return git_controller.merge()
    

    # get latest actions on repository
    @git_routes.route('/list', methods=['GET'])
    def list():
        return git_controller.list()
    
    app.register_blueprint(git_routes)

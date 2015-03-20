from app import application
from app.api import hello_world_blueprint

application.register_blueprint(hello_world_blueprint, url_prefix='/hello_world')
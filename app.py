from flask import Flask
from flask_smorest import Api
from resources.items import bp as ItemBlueprint
from resources.store import bp as StoreBlueprint
app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3" 
app.config["OPENAPI_URL_PREFIX"] = "/" # the prefix of our api website.com/
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" # tells flask-smorest to use swagger-ui for displaying information
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # points to swagger-ui code

api = Api(app)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)


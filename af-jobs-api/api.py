
import datetime
from flask.app import Flask
from flask.json import JSONEncoder

from database import db
from af_requests_endpoints import af_requests_bp
import os







# encoder
class CustomJSONEncoder(JSONEncoder):
    "Add support for serializing timedeltas"

    def default(self, o):
        if type(o) == datetime.timedelta:
            return str(o)
        elif type(o) == datetime.datetime:
            return o.isoformat()
        else:
            return super().default(o)


def create_app(settings: dict = None):
    app = Flask(__name__)
    if settings:
        app.config.update(settings)
    app.json_encoder = CustomJSONEncoder

    app.register_blueprint(af_requests_bp)
    return app


app = create_app({
    'SQLALCHEMY_DATABASE_URI': os.getenv('AFDB_URL')
})
db.init_app(app)



# if __name__ == "__main__":
#     app.run(debug=os.getenv("DEBUG", False), host="0.0.0.0")

import os

import config
from app import create_app
from flask_cors import CORS

app = create_app(
    {
        "SQLALCHEMY_DATABASE_URI": os.getenv("AFDB_URL"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
)

allowable_origins = config.get_allowable_origins()
CORS(app, resources={r"/v1/*": {"origins": allowable_origins}})

# if __name__ == "__main__":
#     app.run(debug=os.getenv("DEBUG", False), host="0.0.0.0")

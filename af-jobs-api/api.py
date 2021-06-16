import os

from flask_cors import CORS

from factory import create_app

app = create_app(
    {
        "SQLALCHEMY_DATABASE_URI": os.getenv("AFDB_URL"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
)
CORS(app)

# if __name__ == "__main__":
#     app.run(debug=os.getenv("DEBUG", False), host="0.0.0.0")

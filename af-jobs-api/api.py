import os

from factory import create_app

app = create_app(
    {
        "SQLALCHEMY_DATABASE_URI": os.getenv("AFDB_URL"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
)


# if __name__ == "__main__":
#     app.run(debug=os.getenv("DEBUG", False), host="0.0.0.0")

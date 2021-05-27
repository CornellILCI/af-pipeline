import os


def get_database_url():
    return os.getenv("EBS_AFDB_DB_URL")

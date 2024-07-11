from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()


class Database:
    def __init__(self):
        db_name, db_uri = os.getenv("DB_NAME"), os.getenv("DB_URI")
        self.secret = os.getenv("SECRET")
        self.algorithm = os.getenv("ALGORITHM")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.port = os.getenv("PORT")
        self.secret_key = os.getenv("SECRET_KEY")
        self.client_id = os.getenv("CLIENT_ID")
        self.server_metadata_url = os.getenv("SERVER_META_URL")
        self.client = MongoClient(db_uri, tls=True, tlsCAFile=certifi.where())
        self.db = self.client[db_name]
        self.users = self.db.users
        self.auth = self.db.auth
        self.admins = self.db.admins
        self.tasks = self.db.tasks
        self.assignees = self.db.assignees

    def __del__(self):
        self.client.close()

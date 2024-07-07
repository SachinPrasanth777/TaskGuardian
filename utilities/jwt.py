from jwt import decode, encode
from dotenv import load_dotenv
from utilities.database import Database

load_dotenv()
db = Database()


def create_access_token(payload, secret):
    return encode(payload, secret, algorithm=db.algorithm)


def read_token(token, secret):
    return decode(token, secret, algorithms=[db.algorithm])

import random

otp_storage = {}


def generate_otp(email: str) -> str:
    otp = str(random.randint(10000, 99999))
    otp_storage[email] = otp
    return otp


def check_otp(email: str, otp: str) -> bool:
    if email in otp_storage and otp_storage[email] == otp:
        return True
    return False

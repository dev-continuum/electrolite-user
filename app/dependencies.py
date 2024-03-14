from passlib.context import CryptContext
import random
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_formatted_phone_number(phonenumber):
    country_code = "+91"
    return "{}{}".format(country_code, phonenumber)


def get_random_six_digit_otp():
    return ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])






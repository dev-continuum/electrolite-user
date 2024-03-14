from fastapi import Form
from typing import Optional


class CustomPasswordRequestForm:
    def __init__(
        self,
        phonenumber: str = Form(...),
        otp: str = Form(...)
    ):
        self.phonenumber = phonenumber
        self.otp = otp

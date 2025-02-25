import os
import requests


def validate_captcha_response(captcha_response):
    r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        {"secret": os.environ["RECAPTCHA_V3_SECRET_KEY"], "response": captcha_response},
    )
    return r.json()["success"]

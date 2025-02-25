import os
import requests


def validate_captcha_response(captcha_response):
    secret = os.environ["RECAPTCHA_V3_SECRET_KEY"]
    if secret == "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe":  # Test key
        return True
    r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        {"secret": secret, "response": captcha_response},
    )
    return r.json()["success"]

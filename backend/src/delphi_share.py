import requests
import os
import json
import urllib.parse
from datetime import timedelta
from .datetime import get_now


def create_delphi_share(share_url: str, email: str, should_send_email: bool) -> str:
    share_auth = urllib.parse.unquote(share_url.rsplit("/", 1)[-1])
    backend_url = (
        os.environ["DELPHI_BACKEND_URL"] + "/project_management/file_management/reshare"
    )
    frontend_url = os.environ["DELPHI_FRONTEND_URL"] + "/shared-files"
    payload = {
        "frontend_url": frontend_url,
        "share_auth": share_auth,
        "email": email,
        "expiry_date": (get_now() + timedelta(days=3)).isoformat(),
        "permission_edit": False,
        "permission_download": True,
        "permission_upload": False,
        "should_send_email": should_send_email,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        backend_url, json.dumps(payload), verify=False, headers=headers
    )
    response.raise_for_status()
    return response.json()["share_link"]

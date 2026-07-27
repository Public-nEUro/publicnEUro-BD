import os


def create_frontend_url(rel_path):
    return f"{os.environ['APP_URL']}/manage/{rel_path}"

import os


def get_cli_script(insecure: bool) -> str:
    insecure_str = " --insecure" if insecure else ""
    frontend_url = os.environ["FRONTEND_URL"]
    delphi_backend_url = os.environ["DELPHI_BACKEND_URL"]

    return f"""#!/bin/bash

read -p "Enter your email: " email
read -s -p "Enter your password: " password; echo
read -p "Enter the dataset ID: " dataset
read -p "Enter the folder path to download: " folder_path

get_share_link_url="{frontend_url}/api/get_share_link"
prepare_url="{delphi_backend_url}/project_management/file_management/download/prepare"

share_link=$(curl{insecure_str} -w "\\n" -u "$email":"$password" -L "$get_share_link_url"/"$dataset")

error_message=$(echo $share_link | grep -o '"message":"[^"]*' | cut -d'"' -f4)
if [ -n "$error_message" ]; then
    echo "$error_message"
    exit 1
fi

share_auth=$(basename "$share_link")

prepare_response=$(curl{insecure_str} --location "$prepare_url" --header 'Content-Type: application/json' --data "{{\\"share_auth\\": \\""$share_auth"\\",\\"paths\\": [\\""$folder_path"\\"]}}")

download_name=$(echo $prepare_response | grep -o '"file_name":"[^"]*' | cut -d'"' -f4)
download_link=$(echo $prepare_response | grep -o '"url":"[^"]*' | cut -d'"' -f4)

wget --no-check-certificate -O "$download_name" "$download_link"
"""

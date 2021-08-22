""" Upload input folder images to given deck in the gamecrafter.
"""
import argparse
import json
import logging
import os
import requests  # Found at python-requests.org/
import time

from tgc_utils.utils import list_files_at_path


TGC_CONFIG = {"url": "https://www.thegamecrafter.com/api"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="A folder with input images to upload and nothing else.",
        required=True,
    )
    parser.add_argument(
        "--deck_id",
        help="ID of your TGC deck. See README for instructions on finding it.",
        required=True,
    )
    parser.add_argument(
        "--secrets_json",
        help="A file with secrets: api_key_id, username, password. Get yours from TGC.",
        required=True,
    )
    args = parser.parse_args()
    return args


def create_session(api_key_id, username, password):
    """Create a TGC session

    :return: Python session object
    """
    url = TGC_CONFIG["url"]
    params = {"api_key_id": api_key_id, "username": username, "password": password}
    response = requests.post(url + "/session", params=params)
    if response.status_code != 200:
        assert False, f"error accessing session: {response.json()}"
    session = response.json()["result"]
    return session


def get_root_folder_id(session):
    """Get root folder ID of your account. We'll use that to upload files to.

    :param session: an active TGC session.

    :return: string that is root folder ID
    """
    params = {"session_id": session["id"]}
    url = TGC_CONFIG["url"]
    response = requests.get(url + "/user/" + session["user_id"], params=params)
    user = response.json()["result"]
    root_folder_id = user["root_folder_id"]
    return root_folder_id


def upload_file_to_deck(session, folder_id, deck_id, file_path):
    """Upload a single file to TGC deck.

    :param session: an active TGC session.
    :folder_id: TGC folder ID to upload files to.
    :deck_id: TGC deck ID.
    :file_path: a file to upload to deck_id

    :return: None
    """
    url = TGC_CONFIG["url"]
    basename = os.path.basename(file_path)
    # upload the file first to root folder id
    params = {
        "name": basename,
        "folder_id": folder_id,
        "session_id": session["id"],
        # has_proofed_face has no impact as of 2021-08
        "has_proofed_face": True,
    }
    files = {"file": open(file_path, "rb")}
    response = requests.post(url + "/file", params=params, files=files)
    assert response.status_code == 200
    # after upload is fine, add the file to the deck
    file_id = response.json()["result"]["id"]
    params = {
        "session_id": session["id"],
        "name": basename,
        "deck_id": deck_id,
        "quantity": 1,
        "face_id": file_id,
    }
    response = requests.post(url + "/card", params=params)
    assert response.status_code == 200


def upload_files_to_deck(input_path, deck_id, secrets):
    input_files = list_files_at_path(input_path)
    input_files = [x for x in input_files if x.endswith(".png")]
    session = create_session(
        secrets["api_key_id"], secrets["username"], secrets["password"]
    )
    root_folder_id = get_root_folder_id(session)

    for input_file in input_files:
        logging.info(
            f" * Processing file {input_file} and sleeping 1 second after that."
        )
        upload_file_to_deck(session, root_folder_id, deck_id, input_file)
        time.sleep(1.0)


def main():
    args = parse_args()
    logging.info(f"Reading TGC JSON secrets from {args.secrets_json}.")
    secrets_json_data = open(args.secrets_json).read()
    secrets = json.loads(secrets_json_data)
    logging.info("Starting to upload ...")
    upload_files_to_deck(args.input, args.deck_id, secrets)


if __name__ == "__main__":
    main()

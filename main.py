import os
import subprocess
import concurrent.futures
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from concurrent.futures import ThreadPoolExecutor
page_size = 50

def parse_args():
    parser = argparse.ArgumentParser(description="Download files from Google Drive based on folder ID and voice ID.")
    parser.add_argument("folder_id", type=str, help="Google Drive folder ID from which to download files.")
    parser.add_argument("voice_id", type=str, help="Voice ID associated with the files.")
    return parser.parse_args()

def download_file_subprocess(item, voice_id):
    """Invoke a subprocess to download a file and isolate faults."""
    try:
        command = f"python3 download_script.py --file_id {item['id']} --file_name \"{item['name']}\" --voice_id {voice_id}"
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {item['name']}: {e}")
        return None

def main(folder_id, voice_id):
    output_directory = "outputs"
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    SCOPES = ["https://www.googleapis.com/auth/drive"]

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    get_files_with_token(creds, folder_id, voice_id)

def get_files_with_token(creds, folder_id, voice_id, next_page_token=None):
    try:
        service = build("drive", "v3", credentials=creds)
        query = f"'{folder_id}' in parents"
        results = service.files().list(
            q=query,
            pageSize=page_size,
            fields="nextPageToken, files(id, name)",
            pageToken=next_page_token
        ).execute()

        items = results.get("files", [])
        token = results.get("nextPageToken")
        print(f"Found {len(items)} files in the folder. Next token: {token}")

        if not items:
            print("No more files found. Exiting.")
            return

        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_file = {executor.submit(download_file_subprocess, item, voice_id): item for item in items}
            wav_count = 0
            for future in concurrent.futures.as_completed(future_to_f
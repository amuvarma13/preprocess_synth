import os
import subprocess
import concurrent.futures
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from concurrent.futures import ThreadPoolExecutor

# Define the output directory and make sure it exists
output_directory = "outputs"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

def download_file_subprocess(item, voice_id):
    """Invoke a subprocess to download a file and isolate faults."""
    try:
        command = f"python3 download_script.py --file_id {item['id']} --file_name \"{item['name']}\" --voice_id {voice_id}"
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {item['name']}: {e}")
        return None

def main():

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

    try:
        service = build("drive", "v3", credentials=creds)
        folder_id = '13GYJl3uCGqpTvSN9nCBBhFgvHvxd2Swy'
        voice_id = 'nPczCjzI2devNBz1zQrb'
        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, pageSize=100, fields="nextPageToken, files(id, name)").execute()
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_file = {executor.submit(download_file_subprocess, item, voice_id): item for item in items}
            wav_count = 0
            for future in concurrent.futures.as_completed(future_to_file):
                filename = future.result()
                if filename:
                    wav_count += 1
                    print(f"Downloaded {filename}")

        print(f"Total .wav files downloaded: {wav_count}")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()

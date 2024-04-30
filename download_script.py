import os
import io
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

def download_file(file_id, file_name, voice_id):
    """Download a single file using the Google Drive API."""
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)

    output_directory = "outputs"
    voice_directory = os.path.join(output_directory, voice_id)
    if not os.path.exists(voice_directory):
        os.makedirs(voice_directory)
    
    file_path = os.path.join(voice_directory, file_name)
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    print(f"Downloaded {file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_id', required=True, help="Google Drive file ID")
    parser.add_argument('--file_name', required=True, help="Name of the file to download")
    parser.add_argument('--voice_id', required=True, help="ID used for creating subdirectory")
    args = parser.parse_args()
    download_file(args.file_id, args.file_name, args.voice_id)

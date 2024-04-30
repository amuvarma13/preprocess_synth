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
page_size = 100
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

count_wavs = 0
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
    
    loop_get_files(creds)
 
files = [
    {"folder_id": '1zwBP6-XVRArSd9HROZu9ys0cdU8Qt1mm',"voice_id": '29vD33N1CtxCmqQRPOHJ'}, 
    {"folder_id": '1-5YCtH_Q71QFLb6za9cRBOZNVr0ZY633',"voice_id": '2EiwWnXFnvU5JabPnv8n'}, 
    {"folder_id": '1-2OTj5ENeyT_p-ZqDGoc3eOCC1vSjg5X',"voice_id": '5Q0t7uMcjvnagumLfvZi'}, 

    {"folder_id": '1-Un7hubsPlU2sp2QwDTC0EBDqCdxqR_q',"voice_id": 'CYw3kZ02Hs0563khs1Fj'},
    {"folder_id": '1-CoBSqE2nJq5bCqLCTnRSUqKxtZpPTEv',"voice_id": 'D38z5RcWu1voky8WS1ja'}, 
    {"folder_id": '1-2H2laHvlFOJmSvj5FyzoOQTkBWf2rxt',"voice_id": 'EXAVITQu4vr4xnSDxMaL'}, 
    {"folder_id": '1-EbULlxhI5AHDA--o8tGJQtOm4CnjhZL',"voice_id": 'ErXwobaYiN019PkySvjV'}, 

    {"folder_id": '1-Q6lR96uBdattS3LA-SqcmZMsmDztmvE',"voice_id": 'GBv7mTt0atIp3Br8iCZE'},
    {"folder_id": '1-QCwp5YyomDAAcBz8gi2iy6IkQX1AuPL',"voice_id": 'IKne3meq5aSn9XLyUdCD'}, 
    {"folder_id": '1-ePv2Y7vxkFR72mXaq5EI38PFx1PJx07',"voice_id": 'JBFqnCBsd6RMkjVDRZzb'}, 
    {"folder_id": '1-KLATa5WWDnyaIzlkFA2HusaAiaOIlur',"voice_id": 'LcfcDJNUP1GQjkzn1xUU'}, 

    {"folder_id": '1-bYVEhwq1aL5DS6_os_9aZKBIgEPEtkT',"voice_id": 'MF3mGyEYCl7XYWbV9V6O'},
    {"folder_id": '1-cLx5N0V1PstOJ9O6MGdIMKr0_75jUdY',"voice_id": 'N2lVS1w4EtoT3dr4eOWO'}, 
    {"folder_id": '10FREupuC1uUpPqhXbGnASrfpVQLx7tKR',"voice_id": 'ODq5zmih8GrVes37Dizd'}, 
    {"folder_id": '1-catZnOFofrvWqQVsZc5zzKpq8U_tlWQ',"voice_id": 'oWAxZDx7w5VEj9dCyTzz'}, 


    {"folder_id": '1-ihdzoePuo3Oa_PZfTRji75m_aCyi6Xx',"voice_id": 'onwK4e9ZLuTAKqWW03F9'},
    {"folder_id": '1-yOj19CuUCnjbk-u489155iG1d1Ei7tz',"voice_id": 'pFZP5JQG7iQjIQuC4Bku'}, 
    {"folder_id": '10UczBeUAY6bKYeC5H6AY7CwXbAX5abX3',"voice_id": 'pMsXgVXv3BLzUgSXRplE'}, 
    {"folder_id": '1-v-ldzm2Mc8cCeB4w3RI8mpPXKojF2Za',"voice_id": 'pNInz6obpgDQGcFmaJgB'}, 

    {"folder_id": '1-n0C54rK1_KY-3YSO6fZXLHO5ZNT0LTk',"voice_id": 'piTKgcLEGmPE4e6mEKli'},
    {"folder_id": '10LLZParvYouO3xl6mZ4ssp5OXTYPpjzg',"voice_id": 'pqHfZKP75CvOlQylNhV4'}, 
    {"folder_id": '10fxhS-phWaC_dJIQrc1D0DR6Y54sRRS7',"voice_id": 't0jbNlBVZ17f02VDIeMI'}, 
    {"folder_id": '10690hPcStjQEKq2hwLPX-Mxnv6C53-2N',"voice_id": 'yoZ06aMxZJJ28mfd3POQ'}, 

    {"folder_id": '10AAZ5VzSJ0F13iaidGjjpzIV4EsdII45',"voice_id": 'z9fAnlkpzviPz146aGWa'}, 
    {"folder_id": '1vvA6aiAkewriSlTzAmEBjtUtJvNsBoxg-Mxnv6C53-2N',"voice_id": '21m00Tcm4TlvDq8ikWAM'}, 
    {"folder_id": '1v-14XQO_7mUC99vA8zUBpxQB9TpGXXVR',"voice_id": 'AZnzlk1XvdvUeBnXmlld'}, 


]

def loop_get_files(creds):
    for file in files:

        folder_id = file["folder_id"]
        voice_id = file["voice_id"]

        print(f'starting {voice_id}')

        get_files_with_token(creds, folder_id, 0, voice_id)


def get_files_with_token(creds,folder_id, voice_id,wav_count, next_page_token=None):
    try:
        service = build("drive", "v3", credentials=creds)
        query = f"'{folder_id}' in parents"
        results = None
        if next_page_token:
            results = service.files().list(q=query, pageSize=page_size, fields="nextPageToken, files(id, name)", pageToken=next_page_token).execute()
        else:
            results = service.files().list(q=query, pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
        items = results.get("files", [])
        token = results.get("nextPageToken")
        print(f"Found {len(items)} files in the folder", "token is", token)

        if not items:
            print("No files found.")
            return

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_file = {executor.submit(download_file_subprocess, item, voice_id): item for item in items}
            
            for future in concurrent.futures.as_completed(future_to_file):
                filename = future.result()
                if filename:
                    wav_count += 1
                    print(f"Downloaded {wav_count} number of files")

        if wav_count > 0:
            get_files_with_token(creds,folder_id, voice_id, wav_count, token, )

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()

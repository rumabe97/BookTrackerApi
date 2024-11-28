import re
import json

from packaging import version
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from decouple import config

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
google_credentials_json = config('GOOGLE_CREDENTIALS_JSON')

credentials_dict = json.loads(google_credentials_json)
credentials = Credentials.from_service_account_info(credentials_dict)

drive_service = build('drive', 'v3', credentials=credentials)
folderId = config('FOLDER_ID', default='188n6CCpA_TbuNJ0aztENdCGFr2XHZVfK')


def get_latest_version():
    query = f"'{folderId}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    latest_version = '0.0.0'
    latest_file_id = None

    for file in files:
        name = file.get('name', '')
        match = re.match(r'BookTracker-(\d+\.\d+\.\d+)\.apk$', name)
        if match:
            file_version = match.group(1)
            if version.parse(file_version) > version.parse(latest_version):
                latest_version = file_version
                latest_file_id = file.get('id')

    return latest_version, latest_file_id

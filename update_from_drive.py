import io
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# ID de tes fichiers Google Drive
FILE_IDS = {
    "historique_complet.csv": "1qFUHW811O3DsMv8bRducbc4l0L3VRYY5",
    "classement_youtube.csv": "1F5XghVQghx1KZD7_ZRPSEVOjQbyXxDj2",
    "dashboard.py": "1YW4Eq-FVWbAgJR6Cv6tuqGMsmpoj219H"  # ✅ ID corrigé
}

# Authentification
def get_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

# Téléchargement des fichiers
def update_files_from_drive():
    service = get_drive_service()
    for filename, file_id in FILE_IDS.items():
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        print(f"✅ {filename} mis à jour depuis Drive")

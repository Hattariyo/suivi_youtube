import io
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# ✅ IDs actuels de tes fichiers Google Drive
FILE_IDS = {
    "historique_complet.csv": "1Oi5kWc173-Z4ecnySTkbz6hffuYigXri",
    "classement_youtube.csv": "1c0LeysCYhrKr6JaXD6w-XCHmPMwpXvAu",
    "dashboard.py": "1YW4Eq-FVWbAgJR6Cv6tuqGMsmpoj219H"
}

# 🔐 Authentification avec le compte de service
def get_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

# ⬇️ Téléchargement des fichiers depuis Drive
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

# Lancer la fonction si le script est exécuté directement
if __name__ == "__main__":
    update_files_from_drive()

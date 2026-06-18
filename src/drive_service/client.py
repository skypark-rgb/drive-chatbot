from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload

from google.oauth2 import service_account
from googleapiclient.discovery import build
from urllib3 import request

from models.drive_file import DriveFile


class DriveClient:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path

        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )

        self.service = build(
            "drive",
            "v3",
            credentials=self.credentials,
        )
    
    def list_files(self, folder_id: str):
        query = f"'{folder_id}' in parents and trashed = false"

        results = (
            self.service.files()
            .list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, modifiedTime, createdTime)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )

        files = []

        for file in results.get("files", []):
            files.append(
                DriveFile(
                    id=file["id"],
                    name=file["name"],
                    mime_type=file["mimeType"],
                    modified_time=file["modifiedTime"],
                    created_time=file["createdTime"],
                )
            )
        
        return files
    
    def download_file(self, file_id: str) -> bytes:
        request = self.service.files().get_media(fileId=file_id)

        file_buffer = BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)

        done = False

        while not done:
            _, done = downloader.next_chunk()

        return file_buffer.getvalue()
    
    def export_google_doc_as_text(self, file_id: str) -> str:
        request = self.service.files().export_media(
            fileId=file_id,
            mimeType="text/plain",
        )

        return request.execute().decode("utf-8")

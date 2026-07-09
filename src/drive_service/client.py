from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload

from google.oauth2 import service_account
from googleapiclient.discovery import build

from models.drive_file import DriveFile


import google.auth


import json


class DriveClient:

    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path

        from config import GOOGLE_SERVICE_ACCOUNT_INFO

        scopes = ["https://www.googleapis.com/auth/drive.readonly"]

        if GOOGLE_SERVICE_ACCOUNT_INFO:
            service_account_info = json.loads(GOOGLE_SERVICE_ACCOUNT_INFO)

            self.credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=scopes,
            )

        elif credentials_path:
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=scopes,
            )

        else:
            self.credentials, _ = google.auth.default(
                scopes=scopes,
            )

        self.service = build(
            "drive",
            "v3",
            credentials=self.credentials,
        )


    def list_files(self, folder_id: str):
        all_files = []

        self._list_files_recursive(
            folder_id=folder_id,
            all_files=all_files,
        )

        return all_files


    def _list_files_recursive(self, folder_id: str, all_files: list):
        query = f"'{folder_id}' in parents and trashed = false"

        page_token = None

        while True:
            results = (
                self.service.files()
                .list(
                    q=query,
                    pageSize=100,
                    pageToken=page_token,
                    fields=(
                        "nextPageToken, "
                        "files(id, name, mimeType, modifiedTime, "
                        "md5Checksum, createdTime, size)"
                    ),
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )

            for file in results.get("files", []):
                mime_type = file["mimeType"]

                if mime_type == "application/vnd.google-apps.folder":
                    print(f"📁 Entering folder: {file['name']}")

                    self._list_files_recursive(
                        folder_id=file["id"],
                        all_files=all_files,
                    )

                else:
                    all_files.append(
                        DriveFile(
                            id=file["id"],
                            name=file["name"],
                            mime_type=mime_type,
                            modified_time=file.get("modifiedTime"),
                            created_time=file.get("createdTime"),
                            md5_checksum=file.get("md5Checksum"),
                            size=file.get("size"),
                        )
                    )

            page_token = results.get("nextPageToken")

            if not page_token:
                break    
    
    






    
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


    def export_google_sheet_as_csv(self, file_id: str) -> str:
        request = self.service.files().export_media(
            fileId=file_id,
            mimeType="text/csv",
        )

        return request.execute().decode("utf-8")

import os
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes for read-only access to Google Photos
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

def download_media_item(service, media_id, download_folder):
    media_item = service.mediaItems().get(mediaItemId=media_id).execute()
    base_url = media_item['baseUrl']
    url = f"{base_url}=d"  # '=d' downloads the highest resolution
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(download_folder, media_id + '.jpg')
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {filename}")
    else:
        print(f"Failed to download {media_id}")

def main():
    service = get_service()
    download_folder = 'downloads'
    media_ids_folder = 'non_album_media_ids.txt'
    os.makedirs(download_folder, exist_ok=True)
    with open(media_ids_folder, 'r') as f:
        for line in f:
            media_id = line.strip()
            download_media_item(service, media_id, download_folder)

if __name__ == '__main__':
    main()

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes for read access to Google Photos
SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('photoslibrary', 'v1', credentials=creds,static_discovery=False)

def create_album(service, album_title):
    album = service.albums().create(body={"album": {"title": album_title}}).execute()
    return album['id']

def get_or_create_album(service, album_title):
    albums = service.albums().list().execute()
    for album in albums.get('albums', []):
        if album['title'] == album_title:
            return album['id']
    return create_album(service, album_title)

def add_to_album(service, media_id, album_id):
    try:
        request_body = {
            "mediaItemIds": [
                media_id
            ]
        }
        request = service.albums().batchAddMediaItems(albumId=album_id, body=request_body)
        request.execute()
        print(f"Added media item with ID {media_id} to album with ID {album_id}.")
    except Exception as e:
        print(f"Could not add media item with ID {media_id} to album with ID {album_id}. Reason: {str(e)}")

def main():
    service = get_service()
    album_title = 'DELETE_ME'
    media_ids_folder = 'non_album_media_ids.txt'
    album_id = get_or_create_album(service, album_title)
    if album_id is None:
        print(f"Could not find or create album with title {album_title}")
        return

    with open(media_ids_folder, 'r') as f:
        for line in f:
            media_id = line.strip()
            add_to_album(service, media_id, album_id)

if __name__ == '__main__':
    main()

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes for read-only access to Google Photos
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

def get_all_media_items(service):
    media_items = []
    request_token = None
    while True:
        results = service.mediaItems().list(pageToken=request_token).execute()
        media_items.extend(results.get('mediaItems', []))
        request_token = results.get('nextPageToken')
        if request_token is None:
            print("Requesting another page of all media items...")
            break
    return media_items

def get_all_album_contents(service, album_id):
    album_contents = []
    request_body = {"albumId": album_id, "pageSize": 100}
    while True:
        results = service.mediaItems().search(body=request_body).execute()
        album_contents.extend(results.get('mediaItems', []))
        request_token = results.get('nextPageToken')
        if request_token is None:
            print("Requesting another page of all media items for albums ...")
            break
        request_body['pageToken'] = request_token
    return album_contents

def main():
    service = get_service()
    all_media_items = get_all_media_items(service)
    all_media_ids = set(item['id'] for item in all_media_items)

    album_contents = []
    albums = service.albums().list().execute()
    for album in albums.get('albums', []):
        album_contents += get_all_album_contents(service, album['id'])

    album_media_ids = set(item['id'] for item in album_contents)
    non_album_media_ids = all_media_ids - album_media_ids

    with open('non_album_media_ids.txt', 'w') as f:
        for media_id in non_album_media_ids:
            f.write(media_id + '\n')

    print(f"Found {len(non_album_media_ids)} media items not in any album. IDs written to non_album_media_ids.txt")

if __name__ == '__main__':
    main()

# Google Photo - Photo not in any Album Remover 📸

This python script supports you managing your photos on Google Photos. It detects all photos and videos which are not located in an album and outputs the ids to a file. With the other scripts it is possible to backup those locally before deleting them.

## Disclaimer ❗️

Please note that the **Google Photos API only supports adding media items to albums that were created programmatically via the API**. Manually created albums through the Google Photos web interface or app are not supported. [❗️Issue Tracker here❗️](https://issuetracker.google.com/issues/132274769?pli=1)

## Prerequisites ✅

Before running the script, make sure you have completed the following steps:

1. Set up a Google Cloud Platform (GCP) project.
2. Enable the Google Photos API for your project:
   - Go to the 🌐 [Google Cloud Console](https://console.cloud.google.com/).
   - Select your project (or create a new one).
   - In the left navigation menu, click on "APIs & Services" > "Library".
   - Search for "Google Photos Library API" and click on it.
   - Click the "Enable" button.
3. Create an OAuth 2.0 client ID and download the client secrets JSON file:
   - Go to the 🌐 [Google Cloud Console](https://console.cloud.google.com/).
   - Select your project.
   - In the left navigation menu, click on "APIs & Services" > "Credentials".
   - Click on "Create Credentials" and select "OAuth client ID".
   - Choose "Desktop app" as the application type.
   - Click "Create" and download the JSON file.
   - Rename the JSON file to `credentials.json` and place it in the same directory as the script.
4. Add yourself as a tester in the Google API:
   - Go to the 🌐 [Google Cloud Console](https://console.cloud.google.com/).
   - Select your project.
   - In the left navigation menu, click on "APIs & Services" > "Credentials".
   - Locate the "OAuth 2.0 Client IDs" section and find the client ID associated with your OAuth client ID file.
   - Click on the edit button (✏️) for that client ID.
   - In the "Testing" section, click on "Add Testing Instructions".
   - Provide any necessary instructions and click "Save".
5. Install the required Python dependencies by running
```
pip3 install google-auth google-auth-oauthlib google-auth-httplib2
```

## Setup 🛠️

1. Clone this repository or download the script file.
2. Place the `credentials.json` file (OAuth 2.0 client secrets) in the same directory as the script.

The `credentials.json` should look similar to this:
```json
{
    "installed": {
        "client_id": "xxx.apps.googleusercontent.com",
        "project_id": "xxx",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "xxx",
        "redirect_uris": [
            "http://localhost"
        ]
    }
}

```

## Usage 🚀

### Get all media ids not in an album
1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the script using Python 3: `python3 00_diff.py`.
4. The script will authenticate with Google, create an album (if it doesn't exist), and add the media items from `non_album_media_ids.txt` to the album.
5. Progress and status messages will be printed to the console.

```
...
Requesting another page of all media items for albums ...
Requesting another page of all media items for albums ...
Requesting another page of all media items for albums ...
...
Found 17735 media items not in any album. IDs written to non_album_media_ids.txt
```

### Backup/Download all images not in an album

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the script using Python 3: `python3 01_backup.py`.
4. The script will authenticate with Google, download all images which are not in an album and therefore located in the `non_album_media_ids.txt` file to the folder `download` in the local directory.

### Add all images not in an album to the deletion Album

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the script using Python 3: `python3 02_delete.py`.
4. The script will authenticate with Google, create an album (if it doesn't exist), and add the media items from `non_album_media_ids.txt` to the album.
5. It will delete all photos which are not in an album

## Notes 📝

- The script uses the Google Photos API to perform operations. Make sure you have proper authorization and the required scopes for read and write access to the Google Photos library.
- If an album with the specified title already exists, the script will use that album. If not, it will create a new album.
- The `non_album_media_ids.txt` file should contain valid media item IDs. You can verify the ids in your browser. The ids are also shown when you select the photo of choice and verify the URL.

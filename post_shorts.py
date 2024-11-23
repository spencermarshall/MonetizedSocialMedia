import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set the environment variables in your Python code
os.environ["REFRESH_TOKEN"] = "1//04RaPurJgV86XCgYIARAAGAQSNwF-L9IrLvTfiwEKD1SYQVj6CDxKbAzkUEBDaNHa3ae1LKtQCN0p1BALOS4cuuOWtRCwwIYbAhY"
os.environ["CLIENT_ID"] = "556066699705-0rpktcmob5dkie5hts9hn9bjgvk2ku3r.apps.googleusercontent.com"
os.environ["CLIENT_SECRET"] = "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"

# Define the scope for the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Load credentials from environment variables
def get_credentials():
    credentials = Credentials(
        token=None,  # Access token will be refreshed automatically
        refresh_token=os.environ.get("REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET")
    )
    return credentials

# Upload the YouTube Short
def upload_youtube_short(credentials, video_file_path):
    # Build the YouTube service
    youtube = build("youtube", "v3", credentials=credentials)

    # Prepare the request body
    request_body = {
        "snippet": {
            "title": "Your Short Title #Shorts",
            "description": "Your Short Description",
            "tags": ["shorts", "fun", "example"],
            "categoryId": "22",  # 22 is for People & Blogs, adjust as needed
        },
        "status": {
            "privacyStatus": "public"  # Options: "public", "private", "unlisted"
        },
    }

    # Upload the video
    media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    # Execute the request and get the response
    response = request.execute()
    print(f"Video uploaded successfully: https://www.youtube.com/watch?v={response['id']}")

if __name__ == "__main__":
    # Get credentials using the refresh token
    credentials = get_credentials()

    # Path to your video file (MP4 file)
    video_file_path = "sw_test.mp4"

    # Upload the YouTube Short
    upload_youtube_short(credentials, video_file_path)

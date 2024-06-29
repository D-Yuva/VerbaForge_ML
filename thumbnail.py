import re
import requests
import cv2
import numpy as np
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Extract video ID from YouTube URL
def extract_video_id(url):
    pattern = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Fetch thumbnail URL using YouTube Data API
def fetch_thumbnail_url(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        thumbnail_url = video_response['items'][0]['snippet']['thumbnails']['high']['url']
        return thumbnail_url
    except HttpError as e:
        print(f"Error fetching thumbnail URL: {e}")
        return None

# Download image from URL
def download_image(url):
    response = requests.get(url)
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    return img

# Analyze the thumbnail using Gemini API
def analyze_thumbnail_with_gemini(image, api_key):
    # Hypothetical endpoint, replace with the correct one
    gemini_api_endpoint = "https://api.gemini.com/v1/image_analysis"

    # Convert image to base64 for API request
    _, buffer = cv2.imencode('.jpg', image)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "image": img_base64
    }
    response = requests.post(gemini_api_endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def main():
    url = input("Enter YouTube link: ")
    youtube_api_key = "AIzaSyDKoPwoNghCBxwjEEGuLwG8GjzegNHomPI"
    gemini_api_key = "AIzaSyBPvhyyElfd-l2-tg1xDwVDSQ-7DQgNAvg"

    video_id = extract_video_id(url)
    if not video_id:
        print("Invalid YouTube URL")
        return

    thumbnail_url = fetch_thumbnail_url(video_id, youtube_api_key)
    if not thumbnail_url:
        print("Unable to fetch thumbnail URL")
        return

    print("Thumbnail URL:", thumbnail_url)
    thumbnail_image = download_image(thumbnail_url)

    analysis_result = analyze_thumbnail_with_gemini(thumbnail_image, gemini_api_key)
    if analysis_result:
        print("Detailed Explanation of the Thumbnail:")
        print("Font:", analysis_result.get("font"))
        print("Content Relevancy:", analysis_result.get("content_relevancy"))
        print("Emotion Recognition:", analysis_result.get("emotion_recognition"))
        print("Background Analysis:", analysis_result.get("background_analysis"))

if __name__ == "__main__":
    main()

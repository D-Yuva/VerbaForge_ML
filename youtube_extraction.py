import re
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube

# Extract video ID from YouTube URL
def extract_video_id(url):
    pattern = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

url = input("Enter YouTube link: ")
video_id = extract_video_id(url)

 # Fetch video title using YouTube Data API
api_key = "YOUTUBE_API_KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

try:
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        video_title = video_response['items'][0]['snippet']['title']
        print(f"\nVideo Title: {video_title}")

        def get_video_duration(url):
            yt = YouTube(url)
            duration = yt.length  # Duration in seconds
            minutes, seconds = divmod(duration, 60)
            return f"{minutes} minutes and {seconds} seconds", duration

        video_duration, total_duration = get_video_duration(url)
        print()
        print(f"Video Duration: {video_duration}")
        
except HttpError as e:
        print(f"Error fetching video title: {e}") 
'''
try:
    # Retrieve transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "es", "fr", "de", "it", "pt"])
except Exception as e:
    transcript = None
    print(f"Error: {e}")
    print("Transcript unavailable. Consider using a different method for transcript retrieval.")

#if transcript:
    
    print("\nTranscript:\n")
    transcript_without_duration = []
    for segment in transcript:
        start_time = segment['start']
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        text = segment['text']
        formatted_text = f"[{minutes:02d}:{seconds:02d}] {text}"
        transcript_without_duration.append(formatted_text)
        print(formatted_text)

    # Preprocess text by concatenating all segments
    preprocessed_text = " ".join([segment['text'] for segment in transcript])
    print("\nPreprocessed Transcript Text:\n")
    print(preprocessed_text)

else:
    print("No transcript available.")
'''

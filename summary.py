import google.generativeai as genai
import os
from pytube import YouTube
import time
from youtube_extraction import url
import google

# Set your Google API Key here
GOOGLE_API_KEY = 'AIzaSyBPvhyyElfd-l2-tg1xDwVDSQ-7DQgNAvg'
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

def download_youtube_video(yt_url, download_path='./'):
    yt = YouTube(yt_url)
    stream = yt.streams.get_highest_resolution()
    file_path = stream.download(output_path=download_path)
    return file_path

# Example YouTube URL

# Download the YouTube video
file_path = download_youtube_video(url)

# Upload the video file to Google API
video_file = genai.upload_file(path=file_path)

# Wait for the video to be processed
while video_file.state.name == "PROCESSING":
    print('Waiting for video to be processed.')
    time.sleep(10)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
    raise ValueError(video_file.state.name)
print(f'Video processing complete: {video_file.uri}')

# Create the prompt
prompt = "Describe this video, generate it like a summary."

# Set the model to Gemini 1.5 Flash
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Make the LLM request
print()
print("Making LLM inference request...")
print()
print("Summary")
print()
response = model.generate_content([prompt, video_file], request_options={"timeout": 600})
print(response.text)


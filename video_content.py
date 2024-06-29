import google.generativeai as genai
import os
from pytube import YouTube
import time
from youtube_extraction import url, total_duration
import google
import time

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
prompt_sum = "Describe this video, generate it like a summary."

# Set the model to Gemini 1.5 Flash
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Make the LLM request
print()
print("Making LLM inference request...")
print()
print("Summary")
print()
response = model.generate_content([prompt_sum, video_file], request_options={"timeout": 600})
print(response.text)

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

for i in range(8):
    start_time = i * (total_duration // 8)
    end_time = (i + 1) * (total_duration // 8) if i < 7 else total_duration
    prompt = f"What emotions is shown from {format_time(start_time)} to {format_time(end_time)}"
    
    print(f"{format_time(start_time)} to {format_time(end_time)}")
    try:
        response = model.generate_content([prompt, video_file], request_options={"timeout": 600})
        print(response.text)
    except google.api_core.exceptions.ResourceExhausted:
        print("Quota exceeded. Waiting for 60 seconds before retrying...")
        time.sleep(60)  # Wait for 60 seconds before retrying
        response = model.generate_content([prompt, video_file], request_options={"timeout": 600})
        print(response.text)
    
    print("\n")
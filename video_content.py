import os
import time
import yt_dlp as youtube_dl
import google.generativeai as genai
from youtube_extraction import url, total_duration
import google.api_core.exceptions

# Set your Google API Key here
GOOGLE_API_KEY = 'YOUR_GEMINI_API_KEY'
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

# Function to download YouTube video using yt-dlp
def download_youtube_video(yt_url, download_path='./'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(yt_url, download=True)
        file_path = ydl.prepare_filename(info_dict)
    return file_path

# Example YouTube URL
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
prompt_sum = "Describe this video, generate it like a summary as a single para with bullet points, then generate another set of texts which deals with the most unique and most shown thing in the video"

# Set the model to Gemini 1.5 Flash
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Make the LLM request for summary
print("\nMaking LLM inference request for summary...\n")
response_summary = model.generate_content([prompt_sum, video_file], request_options={"timeout": 600})
print("Summary:")
print(response_summary.text)

# Function to format time in MM:SS format
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

# Analyze emotions in segments of the video
for i in range(4):
    start_time = i * (total_duration // 4)
    end_time = (i + 1) * (total_duration // 4) if i < 3 else total_duration
    prompt = f"What emotions are shown from {format_time(start_time)} to {format_time(end_time)}"
    
    print(f"\n{format_time(start_time)} to {format_time(end_time)}:")
    
    retry_count = 0
    max_retries = 3
    response_emotion = None

    while retry_count < max_retries:
        try:
            response_emotion = model.generate_content([prompt, video_file], request_options={"timeout": 600})
            print(response_emotion.text)
            break  # Exit the loop if the request is successful
        except google.api_core.exceptions.ResourceExhausted:
            retry_count += 1
            print(f"Quota exceeded. Waiting for 60 seconds before retrying... (Attempt {retry_count}/{max_retries})")
            time.sleep(60)  # Wait for 60 seconds before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    if not response_emotion:
        print("Failed to get a response after multiple attempts.")

# Generate script for another creator based on summary and emotion analysis
script_time = input("How long should the script be: ")
cultural_reference = input("What areas cultural references you want to consider: ")
prompt_script = f"Generate a YouTube script for another creator that is similar in content with timestamps, including emotions and background activities. Generate script starting from 0:00 and end at  {script_time}.00, in the script make sure {cultural_reference} movie reference, {cultural_reference} meme reference, few {cultural_reference} words in between, make the script sound very {cultural_reference} and anything related to {cultural_reference} must be added to the script. Finally, suggest similar contents on the internet."

retry_count = 0
response_script = None
max_retries = 3

while retry_count < max_retries:
    try:
        response_script = model.generate_content([prompt_script, response_emotion.text, response_summary.text, video_file], request_options={"timeout": 600})
        break  # Exit the loop if the request is successful
    except google.api_core.exceptions.ResourceExhausted:
        retry_count += 1
        print(f"Quota exceeded. Waiting for 60 seconds before retrying... (Attempt {retry_count}/{max_retries})")
        time.sleep(60)  # Wait for 60 seconds before retrying
    except Exception as e:
        print(f"An error occurred: {e}")
        break

if response_script:
    print("\nGenerated YouTube Script:")
    print(response_script.text)
else:
    print("Failed to get a response after multiple attempts.")

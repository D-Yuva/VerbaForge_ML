# my first change lmao
import google.generativeai as genai
from IPython.display import Markdown,display
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube
import re
import urllib.request
from youtube_extraction import url, video_id, video_title

# API Key
GOOGLE_API_KEY = 'AIzaSyBPvhyyElfd-l2-tg1xDwVDSQ-7DQgNAvg'
genai.configure(api_key=GOOGLE_API_KEY)


# Extract video ID from YouTube URL
def extract_video_id(url):
    pattern = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

#video url for saving file
video_url = input("Enter YouTube link: ")
#video id for getting video title
video_id = extract_video_id(video_url)

def get_video_title(video_idd):
    # Fetch video title using YouTube Data API
    api_key = "AIzaSyDKoPwoNghCBxwjEEGuLwG8GjzegNHomPI"
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        video_response = youtube.videos().list(
            part='snippet',
            id=video_idd
        ).execute()

        video_title = video_response['items'][0]['snippet']['title']
        print(f"\nVideo Title: {video_title}")
    except HttpError as e:
        print(f"Error fetching video title: {e}") 
    #return the video title to use
    return video_title

# Downloading yt thumbnail
def save_thumbnail(link,name_to_save):
  # making the name in proper format
  name_to_save = name_to_save + '.jpg'
  print(f"** Saving File {name_to_save} **\n")
  yt = YouTube(link)
  url = yt.thumbnail_url
  #let's clean the url till .jpg only
  end_index = url.find('.jpg') + 4  # Adding 4 to include '.jpg'
  cleaned_url = url[:end_index]
  urllib.request.urlretrieve(cleaned_url, name_to_save)
  print(f"** {name_to_save} Saved!! **")

def generate_from_thumb(thumbnail_name,script,prompt):
   thumb = genai.upload_file(path=f"{thumbnail_name}.jpg")
   print(f"Uploaded file '{thumb.display_name}' as: {thumb.uri}")
   
   # combine script into the prompt
   combined_prompt = f"{prompt}\n\nHere is the script for the video:\n{script}"
   # Choose a Gemini API model.
   model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    
   # Prompt the model with text and the previously uploaded image.
   response = model.generate_content([thumb, combined_prompt])
   
   # markdown does not work in vscode and works only n jupter format
   # display(Markdown(">" + response.text))
   return response.text



video_title = get_video_title(video_id)
save_thumbnail(video_url,video_title)

script = str(input("Please enter the script  "))
prompt = str(input("Please enter the prompt  "))



answer = generate_from_thumb(video_title,script,prompt)

print(" Answer :\n",answer)
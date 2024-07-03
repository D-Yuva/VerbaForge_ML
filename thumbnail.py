# All imports
import google.generativeai as genai
from IPython.display import Markdown,display
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube
import re
import urllib.request
from diffusers import StableDiffusionPipeline
import torch
import matplotlib.pyplot as plt
from youtube_extraction import url, video_id

# API Key
GOOGLE_API_KEY = 'AIzaSyBPvhyyElfd-l2-tg1xDwVDSQ-7DQgNAvg'
genai.configure(api_key=GOOGLE_API_KEY)


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
    # Choose a Gemini API model.
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
     
    # create two different prompts- one for text gen - another to send to image gen
    text_prompt = f"{prompt}\n\nHere is the script for the video:\n{script}"
    image_prompt = f"""Give me just one prompt for an AI so that I can make an image 
    similar to the image and is suitable for my script 
    \n\nHere is the script for the video:\n{script}"""

    # Prompt the model with text and the previously uploaded image.
    text_response = model.generate_content([thumb, text_prompt])
    image_response = model.generate_content([thumb,image_prompt])

    #send image response as a new prompt to image gen
    image = generate_image(image)
    
    # markdown does not work in vscode and works only n jupter format
    # display(Markdown(">" + response.text))
    return image,text_response.text
    
def generate_image(prompt):
  image_gen_model = "stabilityai/stable-diffusion-xl-base-1.0"
  pipe = StableDiffusionPipeline.from_pretrained(image_gen_model, torch_dtype=torch.float16, use_safetensors=True)
  pipe = pipe.to("cuda")
  image = pipe(prompt).images[0]
  print("[PROMPT]: ",prompt)
  


video_title = get_video_title(video_id)
save_thumbnail(url,video_title)

script = str(input("Please enter the script  "))
prompt = str(input("Please enter the prompt  "))


image,answer = generate_from_thumb(video_title,script,prompt)

print(" Answer :\n",answer)
plt.imshow(image);
plt.axis('off');
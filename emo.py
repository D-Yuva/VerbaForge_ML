from pytube import YouTube
from youtube_extraction import url
import textwrap
import google.generativeai as genai
from IPython.display import Markdown
import PIL.Image
import urllib.request
import os

def download_youtube_video(url, download_path='./'):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    file_path = stream.download(output_path=download_path)
    return file_path


GOOGLE_API_KEY= os.getenv('AIzaSyBPvhyyElfd-l2-tg1xDwVDSQ-7DQgNAvg')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")





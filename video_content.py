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
prompt_sum = "Describe this video, generate it like a summary as a single para with bullet points, then generate another set of texts which deals with the most unique and most shown thing in the video"

# Set the model to Gemini 1.5 Flash
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Make the LLM request
print()
print("Making LLM inference request...")
print()
print("Summary")
print()
response_summary = model.generate_content([prompt_sum, video_file], request_options={"timeout": 600})
print(response_summary.text)

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

for i in range(8):
    start_time = i * (total_duration // 8)
    end_time = (i + 1) * (total_duration // 8) if i < 7 else total_duration
    prompt = f"What emotions is shown from {format_time(start_time)} to {format_time(end_time)}"
    
    print(f"{format_time(start_time)} to {format_time(end_time)}")
    try:
        response_emotion = model.generate_content([prompt, video_file], request_options={"timeout": 600})
        print(response_emotion.text)
    except google.api_core.exceptions.ResourceExhausted:
        print("Quota exceeded. Waiting for 60 seconds before retrying...")
        time.sleep(60)  # Wait for 60 seconds before retrying
        response = model.generate_content([prompt, video_file], request_options={"timeout": 600})
        print(response_emotion.text)
    
    print("\n")

    # Script 
script = """Script: Hidden Gems of [City Name] with a Twist!
Intro

(Upbeat Indie Music with a playful, adventurous vibe)

Scene 1: You're standing on a rooftop overlooking a bustling street market below, with a glimpse of the iconic [Landmark 1] peaking through the city skyline. Confetti gently rains down around you.

(0:00)  You (Energetic, friendly, with a hint of surprise):  Hey everyone, what's up adventure seekers!  (Introduce yourself and your channel)  Today, we're ditching the tourist traps and diving headfirst into the vibrant, hidden heart of [City Name]! But first things first... confetti fight!

(Reach into a hidden bag and pull out confetti poppers, have a playful confetti battle with someone off-camera)

(0:05)  You (Playful, slightly breathless):  Alright, alright, enough with the confetti for now! Look, don't get me wrong, [Landmark 1] is iconic for a reason. But [City Name] has so much more to offer for budget travelers and anyone who wants to experience the city like a local.

(0:10)  You (Enthusiastic):  So, get ready to explore quirky neighborhoods, sip coffee in secret cafes, and maybe even find some hidden street art – all without burning a hole in your wallet! But beware, there might be a few more surprises along the way... Let's go!

Main Content

Scene 2: You're walking down a narrow, colorful street lined with independent shops and overflowing with character. Balloons of various shapes and sizes are bobbing along the street, carried by the gentle breeze.

(0:15)  You (Intrigued):  This is exactly the kind of vibe I'm talking about! Check out this street in the [Neighborhood Name] district.  It's bursting with independent shops and local energy.

(0:20)  You (Pointing to a specific shop with a mischievous grin):  Oh my gosh! Look at [Shop Name]! They specialize in [products they sell] and everything here just screams unique. Plus, you won't find these treasures anywhere else!  (Reach into your backpack and pull out a handful of brightly colored whoopie cushions) But let's see if we can add a little extra "uniqueness" to their storefront...

(Sneak around the corner and strategically place whoopie cushions on a few chairs outside the shop)

(Cut back to you browsing the shop, picking up interesting items)

(0:30)  You (Excited):  Alright, caffeine time!  We're heading to a hidden gem cafe called [Cafe Name]. They roast their own beans and the atmosphere is seriously cozy.

Scene 3:  You're relaxing at the cafe, sipping coffee and enjoying the ambiance. Suddenly, a loud series of whoopie cushion noises erupt from outside.

(0:40)  You (Trying to hold back laughter):  Oh dear, it seems our little prank is a success!  (A sheepish grin spreads across your face)  This is what makes exploring a city so special.  Places like this capture the true soul of [City Name], away from the tourist crowds, and with a touch of unexpected fun!

(0:45)  You (Intrigued):  For the afternoon, we're ditching the guidebooks and heading to a local favorite – [Park Name]. It's a hidden oasis perfect for escaping the hustle and bustle and  just soaking in some peace.  (Reach into your pocket and pull out a giant beach ball)  But who says peace has to be boring?

Scene 4:  You're exploring the park, showing off the beautiful scenery and locals enjoying the space. You're bouncing the giant beach ball around, inviting people to join in a playful game.

(0:55)  You (Mesmerized):  Just look at this view! Breathtaking, right?  And guess what?  There's barely anyone here!

(Show a spot on a map or phone)

(1:00)  You (Informative):  So, if you're looking for a place to relax, have a picnic with friends, or even do some yoga outdoors, this is your spot. Bookmark it!  (The giant beach ball goes flying off-camera in a slow-motion arc) Uh oh, looks like someone's a little too enthusiastic!

Call to Action (CTA)

**"""

prompt_script = "Generate a youtube script"
response = model.generate_content([prompt_script, response_emotion.text, response_summary.text,script, video_file], request_options={"timeout": 600})
print(response.text)
import re
''' Exctract video gives the video id from both yt video link and yt share link '''
def extract_video_id(url):

    pattern = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'

    match = re.search(pattern, url)

    return match.group(1) if match else None
url = str(input("Enter youtube link: "))
video_id = extract_video_id(url)

from youtube_transcript_api import YouTubeTranscriptApi

api_key = "AIzaSyDKoPwoNghCBxwjEEGuLwG8GjzegNHomPI"

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "es", "fr", "de", "it", "pt"])
except:
    transcript = "Transcript unavailable. Consider using a different method for transcript retrieval."

print()
print(transcript)

preprocessed_text = ""
for segment in transcript:
    preprocessed_text += segment['text'] + " "

preprocessed_text = preprocessed_text.replace("[TIMESTAMP]", "")

print()
print(preprocessed_text)
dialogue_text = preprocessed_text
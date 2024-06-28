from youtube_transcript_api import YouTubeTranscriptApi
import cv2
import os
from pytube import YouTube
from deepface import DeepFace
from youtube_extraction import url

def get_frame_gap(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_gap = 1.0 / fps
    cap.release()
    return frame_gap

def download_youtube_video(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').first()
    stream.download(output_path)
    video_path = os.path.join(output_path, stream.default_filename)
    extract_frames(video_path, output_path)

def extract_frames(video_path, output_directory):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    frame_skip_counter = 0
    frame_gap = get_frame_gap(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_skip_counter == 0:
            frame_path = os.path.join(output_directory, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            analyze_emotions(frame_path, frame_count, transcript)
            frame_count += 1

        frame_skip_counter = (frame_skip_counter + 1) % 5
        frame_count += int(frame_gap)

    cap.release()

def analyze_emotions(frame_path, frame_count, transcript):
    frame = cv2.imread(frame_path)
    if frame is not None:
        frame_time_minutes = frame_count // 60
        frame_time_seconds = frame_count % 60

        print(f"Frame {frame_count} - {frame_time_minutes} mins {frame_time_seconds} secs:")

        try:
            result = DeepFace.analyze(frame, actions=['emotion'])
            emotions = result[0]['emotion']
            dominant_emotion = max(emotions, key=emotions.get)

            print("Dominant Emotion:", dominant_emotion)

            if transcript and frame_count < len(transcript):
                print("Transcript:", transcript[frame_count]["text"])
            else:
                print("Transcript unavailable for this frame.")

            print("-" * 50)
        except ValueError as e:
            if "Face could not be detected" in str(e):
                print(f"No Emotions Detected {frame_count}: Face could not be detected.")
            else:
                print(f"No Emotions Detected {frame_count}: {e}")

            print("-" * 50)
    else:
        print("Failed to load frame.")
        print("-" * 50)

def get_video_transcript(video_id, languages=["en"]):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
    except Exception as e:
        transcript = None
        print("Error occurred while retrieving transcript:", e)

    return transcript

if __name__ == "__main__":
    video_url = url
    output_directory = "frames"
    os.makedirs(output_directory, exist_ok=True)
    video_id = video_url.split("=")[-1]
    transcript = get_video_transcript(video_id)
    preprocessed_text = ""
    if transcript:
        for segment in transcript:
            preprocessed_text += segment['text'] + " "
        preprocessed_text = preprocessed_text.replace("[TIMESTAMP]", "")
        print("Preprocessed Transcript Text:", preprocessed_text)

    download_youtube_video(video_url, output_directory)

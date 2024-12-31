import cv2
import numpy as np
from youtube_extraction import preprocessed_text
from deep_translator import GoogleTranslator

supported_languages = {"en": "English", "es": "Spanish", "fr": "French", "pt": "Portuguese", "de": "German", "it": "Italian"}

while True:
    target_language = input("Enter the language you want the summary in (supported languages: {}): ".format(", ".join(supported_languages.values())))
    if target_language.lower() in supported_languages:
        target_language_code = target_language.lower()
        break
    else:
        print("Please enter a valid language code from the list provided.")



translated_text = GoogleTranslator(source='auto', target=target_language_code).translate(preprocessed_text)

print("Translated text:")
print(translated_text)

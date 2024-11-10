"""
import speech_recognition as sr

recognizer = sr.Recognizer()

# Capture audio from the microphone
with sr.Microphone() as source:
    print("Say something:")
    audio = recognizer.listen(source)

# Recognize speech using Google Web Speech API
try:
    text = recognizer.recognize_google(audio)
    print("You said: " + text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError:
    print("Could not request results from Google API")


def custom_transliterate(text):
    transliteration_map = {
        "আমি": "ami",
        "বাংলায়": "banglai",
        "গান": "gan",
        "গাই": "gai",
        # Add more mappings as needed
    }
    
    for bangla, english in transliteration_map.items():
        text = text.replace(bangla, english)
    
    return text

text = "আমি এখন ভালো আছি। পাশ্চাত্যের বিবর্তন"
transliterated_text = custom_transliterate(text)
print(transliterated_text)  # Output: ami banglai gan gai
"""

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

text = "আমি বাংলায় গান গাই। "
transliterated_text = transliterate(text, sanscript.BENGALI, sanscript.ITRANS)
print(transliterated_text.lower())


import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import google.generativeai as genai
import config  # importing the API key

# Initialize recognizer once
recognizer = sr.Recognizer()

def text_to_speech(text):
    # Create a new engine each time to avoid run loop errors
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def aiprocess(command):
    # Use the correct variable name from config.py
    genai.configure(api_key=config.Api)
    model = genai.GenerativeModel("gemini-2.5-flash")
    chat = model.start_chat()
    response = chat.send_message(command)
    return response.text

def comm(text):
    text_lower = text.lower()
    if "open google" in text_lower:
        webbrowser.open("https://google.com")
    elif "open youtube" in text_lower:
        webbrowser.open("https://youtube.com")
    elif text_lower.startswith("play"):
        parts = text_lower.split(" ")
        if len(parts) > 1:
            song = parts[1]
            link = music_library.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                text_to_speech("Song not found in library.")
        else:
            text_to_speech("Please specify a song name.")
    elif "open news" in text_lower:
        webbrowser.open("https://timesofindia.indiatimes.com")
    elif "netflix" in text_lower:
        webbrowser.open("https://www.netflix.com/browse")
    else:
        output = aiprocess(text)
        text_to_speech(output)

if __name__ == "__main__":
    text_to_speech("Initializing Alpha")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                print("Recognizing...")
                word = recognizer.recognize_google(audio)

            if word.lower() == "alpha":
                text_to_speech("Yes, what can I do for you?")
                with sr.Microphone() as source:
                    print("Alpha Activate...")
                    audio = recognizer.listen(source, phrase_time_limit=3, timeout=3)
                    print("Recognizing...")
                    command = recognizer.recognize_google(audio)
                    comm(command)

        except Exception as e:
            print(f"Error: {e}")

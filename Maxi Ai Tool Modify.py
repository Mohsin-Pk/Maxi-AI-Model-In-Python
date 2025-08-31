import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import os
import smtplib
import requests
import pygame
import io

# ElevenLabs API configuration
ELEVENLABS_API_KEY = "*********************" # Cant Show API
RACHEL_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

# Initializing pygame for audio playback
pygame.mixer.init()

def speak(audio):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{RACHEL_VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": audio,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            audio_data = io.BytesIO(response.content)
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
        else:
            print(f"ElevenLabs error: {response.status_code}")
            # Fallback to pyttsx3 if ElevenLabs fails
            fallback_speak(audio)
    except:
        print("ElevenLabs connection failed, using fallback voice")
        fallback_speak(audio)

def fallback_speak(audio):
    """Fallback to pyttsx3 if ElevenLabs fails"""
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print("Good Morning!")
    elif 12 <= hour < 18:
        print("Good Afternoon!")
    else:
        print("Good Evening!")
    speak("Hello Sir Mohsin, How May I Help You ?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=2) as source:  
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No speech detected, try again.")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return "None"
    except sr.RequestError:
        print("Network error. Check your internet connection.")
        return "None"
    return query

def sendEmail(to,content):
    server= smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login('pokerfire611@gmail.com','fkcr ayxa vldz dbvs')
    server.sendmail('pokerfire611@gmail.com',to,content)
    server.close()

if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand().lower()

        # Logic For Executing Task
        if 'wikipedia' in query:
            print('Searching Wikipedia...')
            speak("Analyzing Wikipedia Boss")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia...")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            print("Opening Youtube...")
            speak("Opening Youtube...")
            time.sleep(2)
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            print("Opening Google...")
            speak("Opening Google...")
            time.sleep(2)
            webbrowser.open("https://google.com")

        elif 'open my mailbox' in query:
            print("Opening Gmail...")
            speak ("Opening Gmail")
            time.sleep(2)
            webbrowser.open("http://mail.google.com")

        elif 'time' in query:
            now = datetime.datetime.now()
            str_time = now.strftime("%I:%M %p")   # Example: "03:45 PM"
            speak(f"Sir, the time is {str_time}")
            print(str_time)

        elif'play my playlist' in query:
            speak("Okay,Please Wait Boss")
            print("Please Wait....")
            time.sleep(3)
            webbrowser.open("https://www.youtube.com/watch?v=Q9V2cnJhxDs&list=RDxNVXWHt9JjY&index=3")
        
        elif 'open code' in query:
            print("Opening Vs Code...")
            speak("Opening Vs Code for you Boss")
            time.sleep(2)
            code_path = r"C:\Microsoft VS Code\Code.exe"

            os.startfile(code_path)
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content= takeCommand()
                to=("pokerfire631@gmail.com")
                sendEmail(to,content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry to disappoint you Sir Mohsin,But I cant sent email at the time")
        elif 'are you sure' in query or 'sure' in query:
            speak("yes Sir I am Sure")
         
        elif 'thank you' in query or 'thank' in query:
            speak("Your Most Welcome Sir Mohsin")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye Sir, have a great day!")
            print("Assistant Stopped.")
            break


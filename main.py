import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json
import sys

print("Initializing...")

MASTER = os.environ['USERNAME']

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def greetMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning" + MASTER)
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon" + MASTER)
    else:
        speak("Good Evening" + MASTER)

    # speak("How can I help you")
    listenForCommand()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say 'Hey Jenny' to activate")
        audio = r.listen(source)

    try:
        # print("Analyzing voice")
        query = r.recognize_google(audio, language='en-in').lower()
        # print(f"user said: {query}\n")
        return query

    except Exception as e:
        # speak("Sorry I did not understand. Say that again please")
        query = ""
        return takeCommand()
            
def proccessCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say a Command")
        audio = r.listen(source)

    try:
        print("Analyzing voice")
        query = r.recognize_google(audio, language='en-in').lower()
        # print(f"user said: {query}\n")
        return query

    except Exception as e:
        # speak("Sorry I did not understand. Say that again please")
        query = ""
        return takeCommand()

def main(query):
    # Logic for executing tasks based on the query

    #region Actions
    if 'wikipedia' in query:
        speak("Searching wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak(results)

    elif 'open youtube' in query:
        url = "youtube.com"

        # MacOS
        # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

        # Windows
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

        # Linux
        # chrome_path = '/usr/bin/google-chrome %s'

        webbrowser.get(chrome_path).open(url)

    elif 'open reddit' in query:
        url = "reddit.com"

        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

        webbrowser.get(chrome_path).open(url)

    elif 'open code' in query:
        codePath = f"C:\\Users\\{MASTER}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

    elif 'play music' in query:
        songs_dir = f"C:\\Users\\{MASTER}\\Music"
        songs = os.listdir(songs_dir)
        print(songs)
        os.startfile(os.path.join(songs_dir, songs[1]))
    #endregion
    
    #region Simple actions
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {strTime}")
    
    elif 'day' in query:
        x = datetime.datetime.now()
        speak(f"The day is" + x.strftime("%A"))

    elif 'thank you' in query:
        speak("You are welcome")

    elif "joke" in query:
        response = requests.get("http://api.icndb.com/jokes/random")
        response_dict = json.loads(response.text)

        speak(response_dict["value"]["joke"])

    elif "terminate" in query:
        speak("Terminating.....")
        sys.exit()
    #endregion

    query = ""

def listenForCommand():
    listening = True
    while listening:
        command = takeCommand()
        if "hey jenny" in command:
            listening = False
            query = proccessCommand()
            main(query)
            listening = True

# Main program Start
greetMe()

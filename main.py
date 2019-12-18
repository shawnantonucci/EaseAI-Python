import speech_recognition as sr
import simpleaudio as sa
from sys import platform
import wikipedia
import webbrowser
import requests
import datetime
import geocoder
import pyttsx3
import smtplib
import config
import json
import sys
import os

if platform == "linux" or platform == "linux2":
    # linux
    MASTER = os.environ['USER']
elif platform == "darwin":
    # OS X
    MASTER = os.environ['HG_USER']
elif platform == "win32":
    # Windows...
    MASTER = os.environ['USERNAME']

API_KEY = "3a953c9d38d44253aa115852191812"

trigger = "hey maverick"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def playSound():
    filename = 'myfile.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing  

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
        
    listenForCommand()

def getLocation():
    g = geocoder.ip('me')
    city = g.city
    return city

activated = False

def takeCommand():
    global activated

    r = sr.Recognizer()
    with sr.Microphone() as source:
        if not activated:
            speak("Initiating Maverick...")
            activated = True
        r.adjust_for_ambient_noise(source, 1)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        return query
    except Exception as e:
        query = ""
        query = takeCommand()
        return query
    except sr.RequestError as e: 
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) 

def main(query):
    #region Actions
    if 'wikipedia' in query:
        # speak("Searching wikipedia...")
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
    elif 'time' in query.lower():
        strTime = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {strTime}")
    
    elif 'day' in query:
        x = datetime.datetime.now()
        speak(f"The day is" + x.strftime("%A"))

    elif "date" in query:
        now = datetime.datetime.now()
        
        print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%B %d, %Y")
        speak(f"Today is" + dt_string)	
        # listenForCommand()

    elif "weather" in query:
        city = getLocation()
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={config.api_key}&q={city}")
        response_dict = json.loads(response.text)
        class weather:
            def __init__(self, city):
                self.city = response_dict["location"]["name"]
                self.region = response_dict["location"]["region"]
                self.temp = response_dict["current"]["temp_f"]
                self.condition = response_dict["current"]["condition"]["text"]
                self.wind = response_dict["current"]["wind_mph"]

        CurrentWeather = weather("ann arbor")
        speak(f"{CurrentWeather.city}, {CurrentWeather.region}. The temperature is {CurrentWeather.temp} degrees. It is {CurrentWeather.condition}. The wind is {CurrentWeather.wind} miles per hour.")

    elif "location" in query:
        city = getLocation()
        speak(f"You are currently in {city}")

    elif 'thank you' in query:
        speak("You are welcome")

    elif 'how are you' in query:
        speak("I am doing great thanks for asking!")

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
        if "maverick" in command.lower():
            listening = False
            query = command.replace("maverick", "")
            main(query)
            listening = True

# Main program Start
greetMe()

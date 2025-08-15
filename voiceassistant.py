import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import sys

listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

MIC_INDEX = 0  

def talk(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for a command and return it as lowercase text."""
    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            print("\n Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)  
            audio = listener.listen(source, timeout=5, phrase_time_limit=8)
            print(" Processing...")
            command = listener.recognize_google(audio, language="en-IN")  
            command = command.lower()
            print(f" You said: {command}")
            return command
    except sr.WaitTimeoutError:
        print(" No speech detected.")
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        print("Could not connect to speech recognition service.")
        return ""

def run_assistant():
    """Process the command and perform actions."""
    command = take_command()

    if 'hello' in command:
        talk("Hello! How are you doing?")
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {time}")
    elif 'play' in command:
        song = command.replace('play', '').strip()
        if song:
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)
        else:
            talk("Please tell me the song name.")
    elif 'stop' in command:
        talk("Bye! Have a nice day.")
        sys.exit()
    elif command != "":
        talk("Sorry, I am unable to understand you.")

while True:
    run_assistant()

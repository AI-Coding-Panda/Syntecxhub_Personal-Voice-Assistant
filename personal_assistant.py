import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import pyautogui
import pyjokes
import pywhatkit


engine = pyttsx3.init()
voices = engine.getProperty('voices')

if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(text):
    """Speaks the provided text."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Greets the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your personal voice assistant. How can I help you today?")

def listen_for_command():
    """Listens for a voice command and returns the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        # recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {command}\n")
            return command.lower()
        except sr.WaitTimeoutError:
            return "None"
        except sr.UnknownValueError:
            return "None"
        except sr.RequestError:
            speak("I'm having trouble connecting to the internet.")
            return "None"
        except Exception as e:
            print(e)
            return "None"

tasks = []

def main():
    wish_me()
    
    while True:
        command = listen_for_command()
        
        if command == "None":
            continue

        if 'wikipedia' in command:
            speak('Searching Wikipedia...')
            command = command.replace("wikipedia", "")
            try:
                results = wikipedia.summary(command, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except wikipedia.exceptions.PageError:
                speak("I couldn't find a page for that topic.")
            except wikipedia.exceptions.DisambiguationError:
                speak("There were multiple results, please be more specific.")

        elif 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")

        elif 'open google' in command:
            speak("Opening Google")
            webbrowser.open("google.com")

        elif 'play' in command:
            song = command.replace('play', '')
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'search for' in command:
            topic = command.replace('search for', '')
            speak(f"Searching for {topic}")
            pywhatkit.search(topic)

        elif 'the time' in command:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'the date' in command:
            today = datetime.date.today().strftime("%B %d, %Y")
            speak(f"Today's date is {today}")

        elif 'joke' in command:
            speak(pyjokes.get_joke())

        elif 'add a task' in command or 'add task' in command:
            speak("What is the task?")
            task_name = listen_for_command()
            if task_name != "None":
                tasks.append(task_name)
                speak(f"Added {task_name} to your tasks.")

        elif 'list tasks' in command or 'show tasks' in command:
            if not tasks:
                speak("You have no tasks in your list.")
            else:
                speak("Your tasks are:")
                for i, task in enumerate(tasks):
                    speak(f"{i+1}. {task}")

        elif 'clear tasks' in command:
            tasks.clear()
            speak("All tasks have been cleared.")

        elif 'take a screenshot' in command:
            screenshot_name = f"screenshot_{int(time.time())}.png"
            pyautogui.screenshot(screenshot_name)
            speak("Screenshot taken successfully.")

        elif 'exit' in command or 'quit' in command or 'stop' in command:
            speak("Goodbye! Have a nice day.")
            break
            
        elif 'who are you' in command:
            speak("I am a personal voice assistant created to help you with your daily tasks.")

if __name__ == "__main__":
    main()

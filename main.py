import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random

# 1. Initialize the Text-to-Speech Engine
engine = pyttsx3.init()

# Optional: Set the voice properties (e.g., speed and voice type)
engine.setProperty('rate', 175) # Speed of speech
voices = engine.getProperty('voices')
# Index 0 is typically male, 1 is typically female
engine.setProperty('voice', voices[0].id) 

def speak(text):
    """Converts a given text string into speech."""
    engine.say(text)
    engine.runAndWait()


def get_default_microphone_index():
    """Returns the default microphone index or None if no microphones are found."""
    try:
        microphones = sr.Microphone.list_microphone_names()
    except Exception:
        return None

    if not microphones:
        return None

    print("Available microphones:")
    for index, name in enumerate(microphones):
        print(f"  {index}: {name}")

    return 0


def listen():
    """Listens to the microphone and returns the recognized text."""
    recognizer = sr.Recognizer()
    mic_index = get_default_microphone_index()

    try:
        if mic_index is None:
            raise OSError("No microphone available")

        with sr.Microphone(device_index=mic_index) as source:
            print("\nListening... (Please speak into your microphone)")
            # Adjusting for ambient noise helps make recognition more accurate
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        print("Recognizing...")
        # We use Google's free speech recognition API
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
        
    except sr.UnknownValueError:
        # Triggered if the speech is unintelligible 
        print("Sorry, I didn't catch that. Please speak clearly or try again.")
        return input("Please type your command instead: ").lower()
    except sr.RequestError:
        # Triggered if there is no internet connection
        print("Sorry, the speech recognition service is down.")
        return input("Please type your command instead: ").lower()
    except (OSError, AttributeError):
        # Triggered if no microphone is found, or if PyAudio is missing
        print("No microphone detected (or PyAudio is missing).")
        print("If you want voice input, install PyAudio and ensure your microphone is connected and allowed.")
        return input("Please type your command instead: ").lower()

def main():
    speak("Hello! I am your voice assistant. How can I help you?")
    
    # Infinite loop to keep the assistant running until we tell it to stop
    while True:
        command = listen()
        
        # If nothing was understood, loop back and listen again
        if not command:
            continue
            
        # --- COMMANDS ---
        
        # 1. Responding to greetings
        if "hello" in command or "hi" in command:
            greetings = ["Hello there!", "Hi! How are you?", "Greetings! How can I assist you?"]
            response = random.choice(greetings)
            speak(response)
            
        # 2. Telling the time
        elif "time" in command:
            # Get current time and format it as Hours:Minutes AM/PM
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            print(f"Time: {current_time}")
            speak(f"The current time is {current_time}")
            
        # 3. Telling the date
        elif "date" in command:
            # Get current date and format it as Month Day, Year
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            print(f"Date: {current_date}")
            speak(f"Today's date is {current_date}")
            
        # 4. Searching the web
        elif "search" in command or "google" in command:
            speak("What would you like me to search for?")
            search_query = listen()
            
            if search_query:
                speak(f"Searching Google for {search_query}")
                # Create a Google search URL and open it in the default browser
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
                
        # 5. Exit command
        elif "stop" in command or "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day.")
            break
            
        # Fallback for unknown commands
        else:
            speak("I am not sure how to help with that yet.")

if __name__ == "__main__":
    main()

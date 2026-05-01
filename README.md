# Voice Assistant Project

This is a simple voice assistant built with Python that can perform various tasks through voice commands. It uses speech recognition to listen to your commands and text-to-speech to respond.

## Features

- Greeting responses
- Tell current time
- Tell current date
- Web search functionality
- Voice-based interaction

## Requirements

- Python 3.x
- speech_recognition library
- pyttsx3 library
- PyAudio (for microphone access)

Install dependencies using:
```
pip install speech_recognition pyttsx3
```

Note: PyAudio installation might require additional setup on some systems. Refer to the PyAudio documentation for installation instructions.

## Code Explanation

Below is a detailed explanation of the code in `main.py`, broken down by sections and lines.

### Imports
```python
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random
```
- `speech_recognition as sr`: For recognizing speech from microphone input
- `pyttsx3`: For text-to-speech conversion
- `datetime`: For getting current time and date
- `webbrowser`: For opening web pages
- `random`: For selecting random responses

### Text-to-Speech Initialization
```python
# 1. Initialize the Text-to-Speech Engine
engine = pyttsx3.init()

# Optional: Set the voice properties (e.g., speed and voice type)
engine.setProperty('rate', 175) # Speed of speech
voices = engine.getProperty('voices')
# Index 0 is typically male, 1 is typically female
engine.setProperty('voice', voices[0].id)
```
- Initializes the pyttsx3 engine for speech synthesis
- Sets speech rate to 175 words per minute
- Gets available voices and sets to the first one (usually male voice)

### speak() Function
```python
def speak(text):
    """Converts a given text string into speech."""
    engine.say(text)
    engine.runAndWait()
```
- Takes text as input
- Uses the engine to say the text
- `runAndWait()` ensures the speech completes before continuing

### listen() Function
```python
def listen():
    """Listens to the microphone and returns the recognized text."""
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
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
        print("Sorry, I didn't catch that.")
        return input("Please type your command instead: ").lower()
    except sr.RequestError:
        # Triggered if there is no internet connection
        print("Sorry, the speech recognition service is down.")
        return input("Please type your command instead: ").lower()
    except (OSError, AttributeError):
        # Triggered if no microphone is found, or if PyAudio is missing
        print("No microphone detected (or PyAudio is missing).")
        return input("Please type your command instead: ").lower()
```
- Creates a Recognizer instance
- Uses microphone as audio source
- Adjusts for ambient noise for 1 second
- Listens for audio input
- Sends audio to Google's speech recognition API
- Returns the recognized text in lowercase
- Handles various exceptions with fallback to text input

### main() Function
```python
def main():
    speak("Hello! I am your voice assistant. How can I help you?")
    
    # Infinite loop to keep the assistant running until we tell it to stop
    while True:
        command = listen()
        
        # If nothing was understood, loop back and listen again
        if not command:
            continue
```
- Greets the user when started
- Enters an infinite loop to continuously listen for commands
- If no command is recognized, continues listening

### Command Processing
```python
        # --- COMMANDS ---
        
        # 1. Responding to greetings
        if "hello" in command or "hi" in command:
            greetings = ["Hello there!", "Hi! How are you?", "Greetings! How can I assist you?"]
            response = random.choice(greetings)
            speak(response)
```
- Checks if command contains "hello" or "hi"
- Selects a random greeting from the list
- Speaks the selected greeting

```python
        # 2. Telling the time
        elif "time" in command:
            # Get current time and format it as Hours:Minutes AM/PM
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            print(f"Time: {current_time}")
            speak(f"The current time is {current_time}")
```
- Checks if command contains "time"
- Gets current time and formats as 12-hour format with AM/PM
- Prints and speaks the time

```python
        # 3. Telling the date
        elif "date" in command:
            # Get current date and format it as Month Day, Year
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            print(f"Date: {current_date}")
            speak(f"Today's date is {current_date}")
```
- Checks if command contains "date"
- Gets current date and formats as full month name, day, year
- Prints and speaks the date

```python
        # 4. Searching the web
        elif "search" in command or "google" in command:
            speak("What would you like me to search for?")
            search_query = listen()
            
            if search_query:
                speak(f"Searching Google for {search_query}")
                # Create a Google search URL and open it in the default browser
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
```
- Checks if command contains "search" or "google"
- Asks for search query and listens
- If query received, constructs Google search URL and opens in browser

```python
        # 5. Exit command
        elif "stop" in command or "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day.")
            break
```
- Checks for exit commands
- Says goodbye and breaks the loop

```python
        # Fallback for unknown commands
        else:
            speak("I'm sorry, I didn't understand that command. Please try again.")
```
- For unrecognized commands, apologizes and continues

### Running the Program
```python
if __name__ == "__main__":
    main()
```
- Ensures the script runs only when executed directly (not imported)
- Calls the main function to start the assistant

## How to Run

1. Ensure all dependencies are installed
2. Make sure your microphone is working and accessible
3. Run the script: `python main.py`
4. Speak commands like "hello", "what time is it", "what's the date", "search for Python", or "stop"

## Notes

- Requires internet connection for speech recognition
- Microphone access is needed for voice input
- The assistant will continue running until you say "stop", "exit", or "quit"
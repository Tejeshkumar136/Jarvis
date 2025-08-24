import json
import os
import speech_recognition as sr

# Define the path for the status data file
STATUS_FILE = os.path.join(os.path.dirname(__file__), "Data", "Status.data")    # Define the path for the status data file    

def ensure_status_file():
    """Ensure the status file exists with default values"""
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    if not os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'w') as f:
            json.dump({"voice_recognition": False}, f)

def get_voice_status():
    """Get the current voice recognition status"""
    ensure_status_file()
    try:
        with open(STATUS_FILE, 'r') as f:
            data = json.load(f)
            return data.get("voice_recognition", False)
    except:
        return False

def set_voice_status(status):
    """Set the voice recognition status"""
    ensure_status_file()
    try:
        with open(STATUS_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = {}
    
    data["voice_recognition"] = status
    
    with open(STATUS_FILE, 'w') as f:
        json.dump(data, f)

def toggle_voice_status():
    """Toggle the voice recognition status"""
    current_status = get_voice_status()
    set_voice_status(not current_status)
    return not current_status 

def recognize_speech():
    """Recognize speech and return the recognized text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
    print("Recognizing...")
    try:
        text = recognizer.recognize_google(audio)
        response = f"You said: {text}"
        return response
    except sr.UnknownValueError:
        return "Sorry, I could not understand."
    except sr.RequestError:
        return "Sorry, I could not understand." 
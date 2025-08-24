import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# load environmental variables from a .env files.
env_vars = dotenv_values(".env")
AssistantVoice = "en-CA-LiamNeural"

# asynchronomus function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"C:\Users\tejes\Desktop\jarvis\Data\speech.mp3" # define the path where speech file will be saved

    if os.path.exists(file_path):     # check if file already exists
        os.remove(file_path)          # if it exists remove it to avoid overwriting errors

        # create the comunicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(r"C:\Users\tejes\Desktop\jarvis\Data\speech.mp3") # save the generated speech as mp3 file

# function to manage text to speech (tts) functionality
def TTS(Text, func=lambda r=None: True):
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # convert text to an audio file
            asyncio.run(TextToAudioFile(Text))

            # initialize pygame mixer for audio playback
            pygame.mixer.init()

            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r"C:\Users\tejes\Desktop\jarvis\Data\speech.mp3")
            pygame.mixer.music.play()

            # loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)
            return True
        except Exception as e:
            print(f"Error in TTS (attempt {retry_count + 1}): {e}")
            retry_count += 1
            if retry_count >= max_retries:
                print("Max retries reached, skipping TTS")
                return False
        finally:
            try:
                # call the provided function with false to signal the end of TTS
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"error in finally block:{e}")
    
    return False

# function to manage text to speech with additional responses for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")

    # list of predefined responses for cases where text is too long
    responses = [
       "The rest of the result has been printed to the chat screen, kindly check it out sir.",
       "The rest of the text is now on the chat screen, sir, please check it.",
       "You can see the rest of the text on the chat screen, sir.",
       "The remaining part of the text is now on the chat screen, sir.",
       "Sir, you'll find more text on the chat screen for you to see.",
       "The rest of the answer is now on the chat screen, sir.",
       "Sir, please look at the chat screen, the rest of the answer is there.",
       "You'll find the complete answer on the chat screen, sir.",
       "The next part of the text is on the chat screen, sir.",
       "Sir, please check the chat screen for more information.",
       "There's more text on the chat screen for you, sir.",
       "Sir, take a look at the chat screen for additional text.",
       "You'll find more to read on the chat screen, sir.",
       "Sir, check the chat screen for the rest of the text.",
       "The chat screen has the rest of the text, sir.",
       "There's more to see on the chat screen, sir, please look.",
       "Sir, the chat screen holds the continuation of the text.",
       "You'll find the complete answer on the chat screen, kindly check it out sir.",
       "Please review the chat screen for the rest of the text, sir.",
       "Sir, look at the chat screen for the complete answer."
    ]

    if len(Data) > 4 and len(Text)>=250:
        TTS(" ".join(Text.split(".")[:2]) + "." + random.choice(responses), func)

    else:
        TTS(Text,func)

if __name__ == "__main__":
    while True:
        TTS(input("Enter the text:"))

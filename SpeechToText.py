from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import pathlib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# load environmental variables form env files
env_vars = dotenv_values(".env")
# get input language settings from environmental variables
InputLanguage = "en"

# define HTML code for speach recognition
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# replace the language settings in the HTML code with input language from environmental variables
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")


# write the modified html code to the file
with open(r"C:\Users\tejes\Desktop\jarvis\Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# get the current working directory
current_dir = os.getcwd()
# generate file path for the html file
Link = f"{current_dir}/Data/Voice.html"

# set chrom options for webDriver
chrome_options = Options()
user_agent = "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")
# Initialize the chrome WebDriver using the chromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# define the path for temporary files.
TempDirPath = rf"{current_dir}/Frontend/Files"


# function to set the assistant status by writing it to a file
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)


# Function to modify the query to ensure proper punctuation and formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's",
                      "where's", "how's", "can you"]

    # check if query is a question then add a question mark if necessary
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        # add a period if a query is a not a question
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()


# function to translate text into english using the mtranslate library
def UniversalTranslator(Text):
    english_Translation = mt.translate(Text, "en", "auto")
    return english_Translation.capitalize()


# function to perform speech recognition using the WenDriver
def SpeechRecognition():
    # Open the Html file in the browser
    driver.get("file:///" + Link)
    #start speech recognition by clicking the start button
    driver.find_element(by=By.ID, value="start").click()

    while True:
        try:
            #Get the recognition text form the html output element
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                #stop recognition by clicking the stop button
                driver.find_element(by=By.ID, value="end").click()

                #if input language is english, return the modified query.
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    #if input language is not english, translate the text into english
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception as e:
            pass

# main execution block.
if __name__ == "__main__":
    try:
        while True:
            Text = SpeechRecognition()
            print(Text)
            if Text.lower() == "exit":
                print("Stopping Speech Recognition.")
                break
    except KeyboardInterrupt:
        print("\nUser interrupted. Exiting...")
    finally:
        driver.quit()  # Ensure the browser is closed properly



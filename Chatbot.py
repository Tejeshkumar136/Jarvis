from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# Load environment veriables from the .env file.
env_vars = dotenv_values(".env")

# retrieve specific environment variables for username , assistent name , and API key.
Username = "Tejesh Kumar"
Assistantname = "Jarvis"
GroqAPIKey = "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"

# Initialize the groq client using provided API Key
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat message
messages =[]

# define system message that provides context to the AI chatbot about it's role and behaviour
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# a list of system interations for the chatbot
SystemChatBot = [
    {"role": "system", "content": System}
]

# attempt to load the chat log from a JSON file
try:
    with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","r") as f:
        messages = load(f)
except FileNotFoundError:
    # if file doesn't exist , create an empty json file to store chat log
    with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","w") as f:
        dump([],f)
# function to get real time date and time
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    # formate the information into a string
    data = f"please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

# function to modify the chatbot's response for better formatting
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()] # remove empty lines
    modified_answer = '\n'.join(non_empty_lines) # join the cleaned lines back together
    return modified_answer

# main Chatbot function to handle user queries.
def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response. """

    try:
        # load the existing chat log from the JSOzn file.
        with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","r") as f:
            messages = load(f)

            # append the User's query to the message list.
        messages.append({"role": "user", "content": f"{Query}"})

        # makea request to the groq API for a response.
        comletion = client.chat.completions.create(
            model = "llama3-70b-8192", #specifi the AI model to be used
            messages = SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens = 1024,
            temperature = 0.7,
            top_p = 1,
            stream = True,
            stop = None
        )

        Answer ="" # Initialize an empty string to store the AI's response

        #prosess the streamed response chunks.
        for chunk in comletion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content  # append the content to the answer
        Answer = Answer.replace("</s>","") # clean up any unwanted tokens from the response

        # append the Chatbot's response to the message list.
        messages.append({"role": "assistant", "content": Answer})

        # save the updated chat log to the JSON file
        with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","w") as f: 
            dump(messages,f, indent = 4)
        return AnswerModifier(Answer= Answer)

    except Exception as e:

        print(f"Error:{e}")
        with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","w") as f:
            dump([], f, indent = 4)
        return ChatBot(Query)

# Main program entry point
if __name__ =="__main__":
    try:
        while True:
            user_input = input("Enter your Question: ").strip()  # Removes accidental spaces
            if not user_input:
                print("Please enter a valid question.")
                continue
            print(ChatBot(user_input))
    except KeyboardInterrupt:
        print("\n[INFO] Program exited by user.")
        exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")



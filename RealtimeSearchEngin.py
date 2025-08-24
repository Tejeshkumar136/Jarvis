from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables from .env file.
env_vars = dotenv_values(".env")

# retrive environment variables from chatbot configuration
Username = "Tejesh Kumar"
Assistantname = "Jarvis"
GroqAPIkey = "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"

# Initialize the Groq with the API key
client = Groq(api_key = GroqAPIkey)

# define System instructions for the chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file, or create an empty one if it dosent exist
try:
    with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","r") as f:
        messages = load(f)
except:
    with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","w") as f:
        dump([],f)

# function to perform google search and format the result
def GoolgeSearch(query):
    results = list(search(query, advanced = True,num_results=5))
    Answer = f"The search results for'{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer
# Function to clean up the empty spaces from answer
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return  modified_answer

# predefined Chatbot conversation system messages and initial user message
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "hello how can I help You"}
]

# function to get realtime information like current date and time
def Information():
    data=""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use this Real-Time information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours,{minute} minutes, {second} seconds.\n"
    return data

# function to handle real-time search and response generation
def RealtimeSearchEngin(prompt):
    global SystemChatBot, messages

    # Load the chat log from the JSON file.
    with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","r") as f:
        messages = load(f)
    messages.append({"role": "user","content": f"{prompt}"})

    #ADD google search results to the system chatbot message.
    SystemChatBot.append({"role": "system","content": GoolgeSearch(prompt)})

    # generate a response using Groq clint
    completion = client.chat.completions.create(
        model ="llama3-70b-8192",
        messages = SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature = 0.7,
        max_tokens = 2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""

    # concatenate response chunk from the streaming output
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>","")
    messages.append({"role": "assistant", "content": Answer})

    # save the updates chat log back to JSON file.
    with open(r"C:\Users\tejes\Desktop\jarvis\Data\ChatLog.json","w") as f:
        dump(messages, f, indent=4)

    # remove the most recent system message form the chatbot conversation
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    if __name__ == "__main__":
        while True:
            try:
                prompt = input("Enter your query: ")
                if prompt.lower() == "exit":
                    print("Goodbye!")
                    break  # Exit loop if user types "exit"
                print(RealtimeSearchEngin(prompt))
            except KeyboardInterrupt:
                print("\nKeyboard Interrupt detected. Exiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

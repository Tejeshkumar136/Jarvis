import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep


# function to open and display images based on a given import
def open_image(prompt):
    folder_path = r"C:\Users\tejes\Desktop\jarvis\Data"
    prompt = prompt.replace(" ", "_")

    # generate the filename for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            # try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image

        except IOError:
            print(f"Unable to open{image_path}")


# API details for the Hugging Face stable Diffusion model
API_URl = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer{get_key('.env','HuggingFaceAPIKey')}"}


# Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URl, headers=headers, json=payload)
    return response.content


# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []

    # create 4 images generations tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality =4k, sharpness= maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)


def GenerateImage(prompt: str):
    asyncio.run(generate_images(prompt))
    open_image(prompt)


while True:

    try:
        with open(r"C:\Users\tejes\Desktop\jarvis\Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
        Prompt, Status = Data.split(",")

        if Status == "True":
            print("Generation Images...")
            ImageStatus = GenerateImage(prompt=Prompt)

            # reset the status in the file after generation images
            with open(r"C:\Users\tejes\Desktop\jarvis\Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
                break
        else:
            sleep(1) 
    except:
        pass

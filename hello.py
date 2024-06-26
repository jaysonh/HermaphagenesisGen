from flask import Flask, request
import requests
from flask import send_file
from openai import OpenAI
from dotenv import load_dotenv
import os


def download_file(url, local_filename):
    # Send a GET request to the URL
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Check if the request was successful
        # Open a local file with the same name as the URL's basename
        with open(local_filename, 'wb') as local_file:
            # Write the content of the response to the local file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    local_file.write(chunk)
    return local_filename



app = Flask(__name__)

@app.route("/hello")
def hello():
    return "hello world"


@app.route("/")
def dalle3():
    prompt_txt = request.args.get('prompt')
    #prompt_txt = "a unique creature with an upside-down large intestine at the top, a single lung beneath it, another intestine under the lung, a liver at the bottom, four distinct sets of small intestines each with two attached stomachs. Visualize this organism in a dense forest and burrow environment, showing an elongated, segmented body, webbed limbs for climbing and burrowing, and keen sensory organs. The scene includes vibrant forest foliage and intricate underground tunnels, with realistic textures and dynamic lighting. High detail, intricate features, lifelike depiction"
    print(f"prompt: {prompt_txt}")


    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt_txt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    download_file(image_url, "dalle_img.png")
#    return image_url 
#    with open("./dalle_img.png", 'wb') as file:
#        file.write(response.content)
    return send_file('dalle_img.png')
#    return f"Running Dall E 3, url: {image_url}"

#@app.route("/test")
#def testing():

@app.route("/stable")
def stable():

    prompt = request.args.get('prompt')
    #prompt = ""
    #with open('prompt.txt', 'r') as file:
    # Read the entire content of the file
    #    prompt = file.read()

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer sk-x977IttPcveA6BZGo1Y4m1ZwOVyfzprxxKJZjB9cBqOmTphX",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "jpeg",
        },
    )

    with open("./corgi.jpg", 'wb') as file:
        file.write(response.content)
    return send_file('corgi.jpg')

if __name__ == "__main__":
    load_dotenv()
    app.run()



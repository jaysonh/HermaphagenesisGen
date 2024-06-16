from flask import Flask, request
import requests
from flask import send_file

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "hello world"


@app.route("/dalle")
def dalle3():
    prompt = request.args.get('prompt')
    print(f"prompt: {prompt}")
    return "Running Dall E 3"

@app.route("/")
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
#    return prompt_arg
    return send_file('corgi.jpg')

if __name__ == "__main__":
    app.run()



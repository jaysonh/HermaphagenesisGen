from flask import Flask, request
from flask_cors import CORS
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
CORS(app)

@app.route("/hello")
def hello():
    return "hello world"

api_access = { "jayson" : "1234",
	      "marcin"  : "abcd1234",
	 	"test"  : "sj324hjn3j24jj23" }

def checkApiAccess(api_key):
    element_found = False
    for value in api_access.values():
        print(f"checking value {value} against {api_key}")
        if value == api_key:
            print(f"found api_key {api_key}")
            element_found = True
            break
    return element_found;

@app.route("/")
def dalle3():


    prompt_txt = request.args.get('prompt')
    api_key = request.args.get('key')

    print(f"prompt: {prompt_txt}")
    print(f"key: {api_key}")

    if checkApiAccess(api_key) == True:
        client = OpenAI()

#        organism_desc = "a unique amphibious creature with"
#        prompt_txt = organism_desc + prompt_txt

        assistant = client.beta.assistants.create(
     	   name="Animal Descriptor",
           instructions="You describe the phsyical look of an animal",
    	   tools=[{"type": "code_interpreter"}],
    	   model="gpt-4-1106-preview",
        )

        thread = client.beta.threads.create()
        animal_desc = client.beta.threads.messages.create(
 		   thread_id=thread.id,
    		   role="user",
    		   content="please describe in one sentence a unique description of an animal",
		)
        run = client.beta.threads.runs.create_and_poll(
               thread_id=thread.id,
               assistant_id=assistant.id,
               instructions="Please address the user as Jane Doe. The user has a premium account.",
          )
        
        organism_desc ="NULL"

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
#        if messages.length > 0:
#            organism_desc = message.content[0].text.value
        first_msg = True       
        for message in messages:
            if first_msg == True:
                organism_desc = message.content[0].text.value
                first_msg=False
                assert message.content[0].type == "text"
                print({"role": message.role, "message": message.content[0].text.value})
       
        client.beta.assistants.delete(assistant.id)
#       organism_desc = message.content[0].text.value
        prompt_txt = organism_desc + " with a " + prompt_txt

        print(f"prompt: {prompt_txt}")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_txt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        download_file(image_url, "dalle_img.png")
        return send_file('dalle_img.png')
    return "invalid api key"
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



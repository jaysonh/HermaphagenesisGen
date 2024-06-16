from openai import OpenAI
import requests

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


client = OpenAI()

#response = client.images.generate(
#  model="dall-e-3",
#  prompt="A pink pineapple on the beach witha neon sunset in the background photorealistic",
#  size="1024x1024",
#  quality="standard",
#  n=1,
#)

#image_url = response.data[0].url
image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-4esazWoErU7knvolLrfkHv23/user-JfItjIBBx6POIFdpA0yxEBau/img-XkovPywbhX3SbZFZsfV6L1eA.png?st=2024-06-16T11%3A05%3A02Z&se=2024-06-16T13%3A05%3A02Z&sp=r&sv=2023-11-03&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-06-15T15%3A00%3A24Z&ske=2024-06-16T15%3A00%3A24Z&sks=b&skv=2023-11-03&sig=O%2BH6D0Uv5IDI35ISziNy4kbf8BvYKC8vmlcEdFplml4%3D"
download_file(image_url, "test.png")

print(f"image url: {image_url}")


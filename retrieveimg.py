import os
from pymongo import MongoClient
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv


load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["vision_ai"]
collection = db["screenshots"]
num_images = 3  # no of images to retrieve
screenshot_data_list = collection.find().sort("timestamp", -1).limit(num_images)
for index, screenshot_data in enumerate(screenshot_data_list):
    screenshot_binary = screenshot_data["screenshot"]
    
    # convert binary data back to image
    image = Image.open(BytesIO(screenshot_binary))
    
    # save the image to a file
    image_path = f"retrieved_image_{index + 1}.jpg"
    image.save(image_path)

    print(f"Image {index + 1} saved as {image_path}")

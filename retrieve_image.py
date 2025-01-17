import os
from pymongo import MongoClient
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["vision_ai"]
collection = db["screenshots"]

# Number of recent images to retrieve
num_images = 5  # You can change this to retrieve more or fewer images

# Retrieve the most recent N screenshots from MongoDB
screenshot_data_list = collection.find().sort("timestamp", -1).limit(num_images)

# Save each image as a separate file
for index, screenshot_data in enumerate(screenshot_data_list):
    screenshot_binary = screenshot_data["screenshot"]
    
    # Convert binary data back to image
    image = Image.open(BytesIO(screenshot_binary))
    
    # Save the image to a file
    image_path = f"retrieved_image_{index + 1}.jpg"
    image.save(image_path)

    print(f"Image {index + 1} saved as {image_path}")

from google import genai
import time
from google.genai import types
from PIL import Image
import pyautogui
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from io import BytesIO

class ScreenAnalyzer:
    def __init__(self):
        """Initialize the ScreenAnalyzer with the GenAI client and MongoDB connection."""
        load_dotenv()
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY"),
            http_options={"api_version": "v1alpha"},
        )
        # Connect to MongoDB Atlas
        self.mongo_client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.mongo_client["vision_ai"]
        self.collection = self.db["screenshots"]

    @staticmethod
    def capture_screen():
        """Captures a screenshot and returns it as a BytesIO object."""
        screenshot = pyautogui.screenshot()
        screenshot = screenshot.convert("RGB")
        buffer = BytesIO()
        screenshot.save(buffer, format="JPEG")
        buffer.seek(0)  # Reset the buffer pointer to the beginning
        return buffer

    @staticmethod
    def load_and_resize_image(image_buffer):
        """Loads and resizes the image from a BytesIO object to maintain aspect ratio."""
        with Image.open(image_buffer) as img:
            aspect_ratio = img.height / img.width
            new_height = int(img.width * aspect_ratio)
            return img.resize((img.width, new_height), Image.Resampling.LANCZOS)

    def save_to_mongodb(self, image_buffer, metadata=None):
        """Saves the screenshot to MongoDB as binary data."""
        metadata = metadata or {}
        # Save the image and metadata
        self.collection.insert_one({
            "screenshot": image_buffer.getvalue(),
            "metadata": metadata,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def analyze_screen(self, prompt):
        """Analyzes the screen based on a screenshot and prompt."""
        screen_buffer = self.capture_screen()
        self.save_to_mongodb(screen_buffer, metadata={"prompt": prompt})  # Save screenshot to MongoDB
        screen = self.load_and_resize_image(screen_buffer)
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[prompt, screen],
            config=types.GenerateContentConfig(
                system_instruction="Only give the output of White Board. Ignore the other part of screen.",
            ),
        )
        return response.text

import base64
import os
import uuid
from PIL import Image
from io import BytesIO

IMAGE_DIR = 'images/'

def save_image(image_data):
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image_id = str(uuid.uuid4())
    image_path = os.path.join(IMAGE_DIR, f'{image_id}.png')
    image.save(image_path)
    return image_id

def get_image(image_id):
    image_path = os.path.join(IMAGE_DIR, f'{image_id}.png')
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    else:
        return None

def resize_image(image_id, width, height):
    image_path = os.path.join(IMAGE_DIR, f'{image_id}.png')
    if os.path.exists(image_path):
        image = Image.open(image_path)
        resized_image = image.resize((width, height))
        buffered = BytesIO()
        resized_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    else:
        return None

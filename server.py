import zmq
import base64
import json
import os
from PIL import Image
from io import BytesIO
from image_utils import save_image, get_image, resize_image

# Create a directory to store images if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        message = socket.recv_json()
        operation = message['operation']
        
        if operation == 'upload':
            image_data = message['image_data']
            image_id = save_image(image_data)
            response = {'status': 'success', 'image_id': image_id}
        elif operation == 'retrieve':
            image_id = message['image_id']
            image_data = get_image(image_id)
            response = {'status': 'success', 'image_data': image_data}
        elif operation == 'resize':
            image_id = message['image_id']
            width = message['width']
            height = message['height']
            resized_image_data = resize_image(image_id, width, height)
            response = {'status': 'success', 'image_data': resized_image_data}
        else:
            response = {'status': 'error', 'message': 'Invalid operation'}

        socket.send_json(response)

if __name__ == '__main__':
    main()

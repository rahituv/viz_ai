from azure_api_utils import AzureApiReturnedError

import requests
import os


class FaceDetector:

    def __init__(self, image_folder, azure_key):
        self._image_folder = image_folder
        self._azure_key = azure_key

    def detect_faces_in_images(self, image_name_list):
        return [self.detect_face(image_name) for image_name in image_name_list]

    def detect_face(self, image_name):
        headers = {'Content-Type': 'application/octet-stream',
                   'Ocp-Apim-Subscription-Key': self._azure_key}
        image_path = os.path.join(self._image_folder, image_name)
        if not os.path.exists(image_path):
            raise NoSuchImageError(image_name)
        face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
        data = open(image_path, 'rb')
        response = requests.post(face_api_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        raise AzureApiReturnedError


class NoSuchImageError(Exception):
    pass

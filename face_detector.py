from azure_api_utils import face_id_key

import requests
import os


class FaceDetector:

    file_name_key = "file_name"
    face_meta_data_key = "face_meta_data"

    def __init__(self, image_folder, azure_key):
        self._image_folder = image_folder
        self._azure_key = azure_key

    def create_faces_data(self, image_name_list):
        faces_data = dict()
        for image_name in image_name_list:
            for current_face in self._detect_face(image_name):
                faces_data[FaceDetector._parse_face_response(current_face)] = {
                    FaceDetector.file_name_key: image_name,
                    FaceDetector.face_meta_data_key: current_face
                }
        return faces_data

    @staticmethod
    def _parse_face_response(face):
        try:
            return face[face_id_key]
        except KeyError:
            raise MalformedFaceResponse

    def _detect_face(self, image_name):
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
        response.raise_for_status()


class NoSuchImageError(Exception):
    pass


class MalformedFaceResponse(Exception):
    pass


if __name__ == "__main__":
    from azure_api_utils import my_keys
    fd = FaceDetector(image_folder="images", azure_key=my_keys[0])
    print fd.create_faces_data(["a.jpg"])

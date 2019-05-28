import requests


class FaceGrouper:

    face_ids_key = "faceIds"

    def __init__(self, azure_key):
        self._azure_key = azure_key

    def group_faces(self, face_ids):
        headers = {'Content-Type': 'application/json',
                   'Ocp-Apim-Subscription-Key': self._azure_key}
        data = {
            self.face_ids_key: face_ids
        }
        face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/group'
        response = requests.post(face_api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()


class NoSuchImageError(Exception):
    pass

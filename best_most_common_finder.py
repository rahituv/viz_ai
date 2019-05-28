from face_detector import FaceDetector
from face_grouper import FaceGrouper

import os
from PIL import Image


class BestImageOfMostCommonFaceFinder:

    grouped_faces_groups_key = "groups"
    meta_data_face_rectangle_key = "faceRectangle"
    face_rectangle_width_key = "width"
    face_rectangle_height_key = "height"

    def __init__(self, image_folder, azure_key):
        self._image_folder = image_folder
        self._face_detector = FaceDetector(image_folder=image_folder, azure_key=azure_key)
        self._face_grouper = FaceGrouper(azure_key=azure_key)

    def get_best_image_of_most_common_face(self, image_name_list):
        if self._file_names_are_invalid(image_name_list=image_name_list):
            raise AnImageIsMissingError
        face_detection_data = self._face_detector.create_faces_data(image_name_list=image_name_list)
        grouped_faces = self._face_grouper.group_faces(face_detection_data.keys())
        most_common_face_ids = self._get_ids_of_most_common_face(grouped_faces_response=grouped_faces)
        if most_common_face_ids is None:
            return None
        best_image_id = self._get_best_image_id(face_detection_data=face_detection_data, relevant_image_ids=most_common_face_ids)
        return face_detection_data[best_image_id][FaceDetector.face_meta_data_key]

    def _file_names_are_invalid(self, image_name_list):
        image_paths = [os.path.join(self._image_folder, image_name) for image_name in image_name_list]
        return False in map(lambda x: os.path.exists(x), image_paths)

    def _get_ids_of_most_common_face(self, grouped_faces_response):
        if len(grouped_faces_response[self.grouped_faces_groups_key]) == 0:
            return None
        return sorted([[len(group), group] for group in grouped_faces_response[self.grouped_faces_groups_key]],
                      key=lambda x: x[0])[-1][1]

    def _get_best_image_id(self, face_detection_data, relevant_image_ids):
        image_ratio_pairs = list()
        for image_id in relevant_image_ids:
            image_meta_data = face_detection_data[image_id][FaceDetector.face_meta_data_key]
            face_rectangle = image_meta_data[self.meta_data_face_rectangle_key]
            face_size = face_rectangle[self.face_rectangle_height_key] * face_rectangle[self.face_rectangle_width_key]
            im = Image.open(os.path.join(self._image_folder, face_detection_data[image_id][FaceDetector.file_name_key]))
            image_width, image_height = im.size
            image_size = image_height * image_width
            if image_size == 0:
                raise InvalidImageError
            image_ratio_pairs.append([image_id, float(face_size) / image_size])
        return sorted(image_ratio_pairs, key=lambda x: x[1])[-1][0]


class AnImageIsMissingError(Exception):
    pass


class InvalidImageError(Exception):
    pass


if __name__ == "__main__":
    from azure_api_utils import my_keys
    bf = BestImageOfMostCommonFaceFinder(image_folder="images", azure_key=my_keys[0])
    print bf.get_best_image_of_most_common_face(image_name_list=["l1.jpg", "l2.jpg", "l3.jpg", "l4.jpg",
                                                                 "l5.jpg", "l6.jpg", "l7.jpg"])


from face_detector import FaceDetector
from face_grouper import FaceGrouper

from utils import NoSuchImageError

import os
from PIL import Image


class BestImageOfMostCommonFaceFinder:

    grouped_faces_groups_key = "groups"
    messy_group_faces_key = "messyGroup"
    meta_data_face_rectangle_key = "faceRectangle"
    face_rectangle_width_key = "width"
    face_rectangle_height_key = "height"

    response_meta_data_key = "meta_data"
    response_file_name_key = "file_name"

    def __init__(self, image_folder, azure_key):
        self._image_folder = image_folder
        self._face_detector = FaceDetector(image_folder=image_folder, azure_key=azure_key)
        self._face_grouper = FaceGrouper(azure_key=azure_key)

    def get_best_image_of_most_common_face(self, image_name_list):
        self._confirm_files_exist(image_name_list=image_name_list)
        face_detection_data = self._face_detector.create_faces_data(image_name_list=image_name_list)
        grouped_faces = self._face_grouper.group_faces(face_detection_data.keys())
        most_common_face_ids = self._get_ids_of_most_common_face(grouped_faces_response=grouped_faces)
        if most_common_face_ids is None:
            dict()
        best_image_id = self._get_best_image_id(face_detection_data=face_detection_data, relevant_image_ids=most_common_face_ids)
        return {self.response_meta_data_key: face_detection_data[best_image_id][FaceDetector.face_meta_data_key],
                self.response_file_name_key: face_detection_data[best_image_id][FaceDetector.file_name_key]}

    def _confirm_files_exist(self, image_name_list):
        for image_name in image_name_list:
            if not os.path.exists(os.path.join(self._image_folder, image_name)):
                raise NoSuchImageError(image_name)

    def _get_ids_of_most_common_face(self, grouped_faces_response):
        if len(grouped_faces_response[self.grouped_faces_groups_key]) == 0:
            if len(grouped_faces_response[self.messy_group_faces_key]) == 0:
                return None
            return [grouped_faces_response[self.messy_group_faces_key][0]]
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
                raise InvalidImageError(face_detection_data[image_id][FaceDetector.file_name_key])
            image_ratio_pairs.append([image_id, float(face_size) / image_size])
        return sorted(image_ratio_pairs, key=lambda x: x[1])[-1][0]


class InvalidImageError(Exception):

    def __init__(self, file_name):
        self.file_name = file_name


if __name__ == "__main__":
    from azure_api_utils import my_keys
    bf = BestImageOfMostCommonFaceFinder(image_folder="images", azure_key=my_keys[0])
    print bf.get_best_image_of_most_common_face(image_name_list=["l1.jpg", "l2.jpg", "l3.jpg", "l4.jpg",
                                                                 "l5.jpg", "l6.jpg", "l7.jpg"])


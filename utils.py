class NoSuchImageError(Exception):

    def __init__(self, file_name):
        self.file_name = file_name


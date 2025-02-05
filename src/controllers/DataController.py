import os.path
import re

from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseMessage
from .ProjectController import ProjectController


class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseMessage.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseMessage.FILE_SIZE_EXCEEDED.value

        return True, ResponseMessage.FILE_UPLOAD_SUCCEEDED.value

    def generate_unique_file_path(self, original_filename: str, project_id: str):

        random_key = self.generate_random_name()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_filename = self.generate_clean_filename(original_filename=original_filename)

        new_file_path = os.path.join(
            project_path,
            random_key + '_' + cleaned_filename
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_name()
            new_file_path = os.path.join(
                project_path,
                random_key + '_' + cleaned_filename
            )

        return new_file_path, random_key + '_' + cleaned_filename

    def generate_clean_filename(self, original_filename: str):

        # remove special characters, except underscore the dot
        cleaned_filename = re.sub(r'[^\w.]', '', original_filename.strip())

        # replace white spaces with an underscore
        cleaned_filename = cleaned_filename.replace(" ", "_")

        return cleaned_filename

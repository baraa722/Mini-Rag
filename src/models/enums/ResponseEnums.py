from enum import Enum


class ResponseMessage(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file type is not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded the allowed limit"
    FILE_UPLOAD_SUCCEEDED = "file was uploaded successfully"
    FILE_UPLOAD_FAILED = "failed to upload the file"
    FILE_VALIDATION_SUCCEEDED = "file validation was successful"

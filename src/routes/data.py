import json
import os
import aiofiles
import logging

from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseMessage

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1, data"],
)


@data_router.post("/upload_file/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):

    data_controller = DataController()
    project_controller = ProjectController()

    # validating the file properties
    is_valid, message = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST,
            content={
                "op_status": "success" if is_valid else "failed",
                "message": message
            })

    project_path_dir = project_controller.get_project_path(project_id=project_id)
    file_path = data_controller.generate_unique_filename(original_filename=file.filename, project_id=project_id)


    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as ex:

        logger.error(f"error while uploading the file: {ex}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "operation_status": "failed",
                "message": ResponseMessage.FILE_UPLOAD_FAILED.value
            }
        )


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "operation_status": "success",
            "message": ResponseMessage.FILE_UPLOAD_SUCCEEDED.value
        }
    )
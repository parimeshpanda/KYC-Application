from urllib.parse import unquote_plus
from fastapi import  File, \
Form, HTTPException, Query,\
Response, UploadFile
from typing import Optional

from azure.storage.blob import  generate_blob_sas, \
    BlobSasPermissions, ContentSettings

from azure.storage.blob.aio import BlobServiceClient
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.constants import Constant


ACCOUNT_NAME = Constant.ACCOUNT_NAME
CONTAINER_NAME = Constant.CONTAINER_NAME
CONNECTION_STRING = Constant.CONNECTION_STRING


class FileUpload(BaseModel):
    filename: str

async def upload_to_azure_blob(file: bytes, filename: str, content_type: str, container_name: str, connection_string: str):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    async with blob_service_client:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        await blob_client.upload_blob(file,blob_type="BlockBlob", content_settings=ContentSettings(content_type), overwrite=True)
        return blob_client
    

async def generate_sas_token(blob_client: BlobServiceClient, container_name: str, blob_name: str):
    blob_sas_permissions = BlobSasPermissions(read=True, list = True)
    start_time = datetime.now(timezone.utc)
    expiry = start_time + timedelta(days=500)  # Expiry time for the SAS token
    sas_token = generate_blob_sas(
        account_name=blob_client.account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=blob_client.credential.account_key,
        permission=blob_sas_permissions,
        expiry=expiry
    )
    return sas_token



async def upload_file( file: UploadFile = File(...), filename:Optional[str]=None) -> str:
    # if not file.content_type.startswith('image/'):
    #     raise HTTPException(status_code=400, detail="Only image files are allowed.")
    connection_string = CONNECTION_STRING
    container_name = CONTAINER_NAME
    account_name = ACCOUNT_NAME

    blob_name = filename if filename else file.filename
    content_type = file.content_type
    file_content = await file.read()
    blob_client = await upload_to_azure_blob(
        file_content, 
        blob_name,
        content_type,
        container_name, 
        connection_string
    )
    sas_token = await generate_sas_token(
        blob_client,
        container_name, 
        blob_name
    )
    blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    blob_sas_url = blob_url + "?" + sas_token
    # blob_sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{filename}?{sas_token}"

    return blob_sas_url
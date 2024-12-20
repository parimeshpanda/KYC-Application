# import os 
# from datetime import datetime, timedelta

# from azure.core.credentials import AzureKeyCredential
# from azure.ai.formrecognizer import DocumentAnalysisClient
# from azure.storage.blob import BlobServiceClient, generate_container_sas, BlobSasPermissions


# # class AzureDI



# container_name = os.environ.get("AZURE_BLOB_CONTAINER_NAME")
# account_name= os.environ.get("AZURE_BLOB_ACCOUNT_NAME")

# # Initialize clients
# document_analysis_client = DocumentAnalysisClient(
#     endpoint=os.environ.get("AZURE_DI_ENDPOINT"), 
#     credential=AzureKeyCredential(os.environ.get("AZURE_DI_KEY"))
#     )


# blob_service_client = BlobServiceClient.from_connection_string(os.environ.get("AZURE_BLOB_CONN_STRING"))
# account_key = blob_service_client.credential.account_key

# def generate_blob_sas_token(blob_file_name):
#     account_key = blob_service_client.credential.account_key
#     sas_token = generate_container_sas(
#         account_name=account_name,
#         container_name=os.environ.get("AZURE_BLOB_CONTAINER_NAME"),
#         blob_name=blob_file_name,
#         account_key=account_key,
#         permission=BlobSasPermissions(read=True),
#         expiry=datetime.utcnow() + timedelta(hours=1)  # Token valid for specified hours
#     )
#     return f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_file_name}?{sas_token}"

# def extract_passport_info(blob_file_name):
#     extracted_information = {}
#     confidence = 0
#     sas_token = generate_blob_sas_token(blob_file_name)
#     sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_file_name}?{sas_token}"
#     print(f"SAS URL: {sas_url}")

#     try:
#         res = document_analysis_client.begin_analyze_document_from_url("prebuilt-idDocument", document_url = sas_token)
#         id_document_info = res.result().documents[0]

#         extracted_information["DocumentType"] = id_document_info.doc_type  
#         extracted_information["FirstName"] = id_document_info.fields.get('FirstName').value
#         extracted_information["LastName"] = id_document_info.fields.get('LastName').value
#         extracted_information["Sex"] = id_document_info.fields.get('Sex').value
#         extracted_information["DocumentNumber"] = id_document_info.fields.get('DocumentNumber').value
#         extracted_information["DateOfBirth"] = str(id_document_info.fields.get('DateOfBirth').value)
#         extracted_information["DateOfIssue"] = str(id_document_info.fields.get('DateOfIssue').value)
#         extracted_information["DateOfExpiration"] = str(id_document_info.fields.get('DateOfExpiration').value)
#         extracted_information["PlaceOfBirth"] = id_document_info.fields.get('PlaceOfBirth').value
    
#     except Exception as e:
#         print("The Following Exception Occoured while extracting information from the Uploaded Passport Document: ",e)
#         return "The Passport was not found in the Azure Blob. Please upload the document again."
    
#     return extracted_information


# def extract_ssn_info(blob_file_name):
#     extracted_information = {}
#     confidence = 0
#     sas_token = generate_blob_sas_token(blob_file_name)
#     sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_file_name}?{sas_token}"
#     print(f"SAS URL: {sas_url}")
#     try:
#         res = document_analysis_client.begin_analyze_document_from_url("prebuilt-idDocument", document_url = sas_token)
#     except Exception as e:
#         print(e)
#         return "The SSN card was not found in the Azure Blob. Please upload the document again."
#     id_document_info = res.result().documents[0]

#     try:
#         extracted_information["DocumentType"] = id_document_info.doc_type  
#         extracted_information["FirstName"] = id_document_info.fields.get('FirstName').value
#         extracted_information["LastName"] = id_document_info.fields.get('LastName').value
#         extracted_information["DocumentNumber"] = id_document_info.fields.get('DocumentNumber').value

#     except Exception as e:
#         print("The Following Exception Occoured while extracting information from the Uploaded  SSN Document: ",e)
#         return "Information could not be extracted from the document. Please try to upload the document again."
    
#     return extracted_information
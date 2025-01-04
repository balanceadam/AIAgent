from datetime import datetime, timedelta

from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from storages.backends.azure_storage import AzureStorage


def generate_sas_for_blob(blob_name):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    container_name = settings.AZURE_CONTAINER
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

    # Define permissions
    sas_permissions = BlobSasPermissions(read=True)  # This will allow only read operations on the blob

    # Define the period for which the SAS will be valid
    sas_expiry = datetime.utcnow() + timedelta(hours=1)  # SAS will be valid for 1 hour

    sas_token = generate_blob_sas(account_name=account_name,
                                  container_name=container_name,
                                  blob_name=blob_name,
                                  account_key=account_key,
                                  permission=sas_permissions,
                                  expiry=sas_expiry)

    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    return sas_url


class AzureSASStorage(AzureStorage):

    def url(self, name, parameters=None, expire=None):
        # Use the default behavior if expire is set
        if expire:
            return super().url(name, parameters=parameters, expire=expire)

        sas_url = generate_sas_for_blob(name)

        return sas_url


class AzureCDNStorage(AzureStorage):
    # 给azure blob storage替换为cdn的链接
    def url(self, name, parameters=None, expire=None):
        return settings.MEDIA_HOST + name


class LocalFileStorage(FileSystemStorage):
    def url(self, name):
        uri = super().url(name)
        if not uri:
            return uri
        return settings.MEDIA_HOST + uri

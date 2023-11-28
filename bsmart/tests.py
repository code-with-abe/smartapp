from azure.storage.blob import ContainerClient

container_url = "https://sdasstorageeast02.blob.core.windows.net/raw?sp=racwdl&st=2023-11-17T04:46:51Z&se=2023-11-18T12:46:51Z&spr=https&sv=2022-11-02&sr=c&sig=SzSpr9s9lJ2SP8uAJR4Iyv6ZMwKVxto1T6mMv7AZ3QY%3D"
container_client = ContainerClient.from_container_url(container_url)

# List the blobs in the container
# blob_list = container_client.list_blobs()
# for blob in blob_list:
#     print(blob.name)

local_file_path = "../media/pickup.csv"
blob_name = "diabetes/uploadpickup.csv"  # The name you want the blob to have in the container

# Get a BlobClient to represent the blob we are creating
blob_client = container_client.get_blob_client(blob=blob_name)

# Upload the local file to Azure Storage
with open(local_file_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)
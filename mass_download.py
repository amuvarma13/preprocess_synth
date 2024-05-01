import os
from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_blob(bucket_name, blob_name, destination_folder):
    """Download a single blob from GCP bucket."""
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Construct the local file path
    local_file_path = os.path.join(destination_folder, blob_name)

    # Create necessary subdirectories if they don't exist
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    # Download the blob to the local file
    blob.download_to_filename(local_file_path)
    return f"Downloaded {blob_name} to {local_file_path}"

def download_files(bucket_name, destination_folder):
    """Download all files from GCP bucket to a local folder using multiple threads."""
    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Initialize the Google Cloud Storage client and list all blobs
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    # Use ThreadPoolExecutor to download blobs concurrently
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(download_blob, bucket_name, blob.name, destination_folder): blob.name for blob in blobs}

        # Process results as they are completed
        for future in as_completed(futures):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"An error occurred while downloading {futures[future]}: {e}")

if __name__ == "__main__":
    bucket_name = 'wavs-1-05-24-1'  # Replace with your actual bucket name
    destination_folder = 'wavs'  # Replace with your desired local path
    download_files(bucket_name, destination_folder)

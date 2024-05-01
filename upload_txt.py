import sys
from google.cloud import storage

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the specified Google Cloud Storage bucket."""
    # Create a storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file to Google Cloud Storage
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_file.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    bucket_name = 'txt_files_27_04'  # Specify your bucket name here

    # Call the upload function
    upload_to_bucket(bucket_name, filename, filename)

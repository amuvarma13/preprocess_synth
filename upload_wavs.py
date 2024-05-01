import os
from google.cloud import storage
from concurrent.futures import ProcessPoolExecutor, as_completed

def upload_file(bucket_name, source_folder, filename):
    """Helper function to upload a single file in a separate process."""
    # Each process needs to create its own client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    local_path = os.path.join(source_folder, filename)
    blob = bucket.blob(filename)
    blob.upload_from_filename(local_path)
    return f"Uploaded {filename} to {bucket_name}"

def upload_files(bucket_name, source_folder):
    """Upload files to GCP bucket using multiple processes."""
    # Get all .wav files ready for upload
    files_to_upload = []
    for subdir, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.endswith(".wav"):
                files_to_upload.append((subdir, filename))

    # Create a ProcessPoolExecutor for managing concurrent uploads
    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(upload_file, bucket_name, subdir, filename): filename
                   for subdir, filename in files_to_upload}

        # Process results as they are completed
        for future in as_completed(futures):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"An error occurred while uploading {futures[future]}: {e}")

if __name__ == "__main__":
    bucket_name = 'wavs-1-05-24-1'  # Replace with your bucket name
    source_folder = 'outputs'  # Replace with the path to your outputs directory
    upload_files(bucket_name, source_folder)

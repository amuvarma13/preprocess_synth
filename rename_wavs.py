import os

def rename_wavs_and_txts(voice_id):
    # Construct the path to the directory
    directory = f'outputs/{voice_id}/'
    
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"No directory found for {voice_id}")
        return

    # Walk through all files in the directory
    for file in os.listdir(directory):
        # Check if the file is a wav or txt file
        if file.endswith('.wav') or file.endswith('.txt'):
            # Construct the full current file path
            old_path = os.path.join(directory, file)
            # Generate the new file name and path
            new_name = f"{voice_id}_{file}"
            new_path = os.path.join(directory, new_name)
            
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed '{file}' to '{new_name}'")

# Example usage:
voice_id = '29vD33N1CtxCmqQRPOHJ'
rename_wavs_and_txts(voice_id)

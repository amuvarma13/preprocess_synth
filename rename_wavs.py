import os
import argparse

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

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Rename WAV and TXT files to include their voice ID as a prefix.")
    
    # Add arguments
    parser.add_argument('voice_id', type=str, help="The voice ID for the files to be renamed.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the command line arguments
    rename_wavs_and_txts(args.voice_id)

if __name__ == "__main__":
    main()

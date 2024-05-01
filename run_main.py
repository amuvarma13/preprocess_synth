import csv
import subprocess
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script_from_csv(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 2:
                logging.error(f"Skipping invalid row: {row}")
                continue
            folder_id, voice_id = row
            print(f"Processing folder {folder_id} with voice {voice_id}")
            command = f"python3 main.py {folder_id} {voice_id}"
            try:
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                logging.info(f"Successfully processed folder {folder_id} with voice {voice_id}")
                logging.info(result.stdout)
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to process folder {folder_id} with voice {voice_id}")
                logging.error(e.stderr)

if __name__ == "__main__":
    csv_file = 'ids.csv'  # Path to the CSV file containing the IDs
    run_script_from_csv(csv_file)

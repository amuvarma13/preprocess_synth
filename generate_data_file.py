import os
from phonemizer import phonemize
from phonemizer.backend import EspeakBackend

directory = 'outputs/29vD33N1CtxCmqQRPOHJ'


def find_wavs_with_non_empty_txt(directory):
    # This will hold the names of wav files (without extension) with non-empty corresponding txt files
    matched_files = []

    # Walk through all files and folders in the provided directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a wav file
            if file.endswith('.wav'):
                # Construct the full path to the wav file
                wav_path = os.path.join(root, file)
                # Change the extension from .wav to .txt
                txt_path = os.path.splitext(wav_path)[0] + '.txt'
                
                # Check if the txt file exists and is not empty
                if os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
                    # Add the filename without extension and without path
                    matched_files.append(os.path.splitext(file)[0])

    return matched_files

#get all file root names
all_files = find_wavs_with_non_empty_txt(directory)

#get texts
def read_txt_files(file_roots, directory_base="outputs"):
    texts = []
    
    # Iterate over each file root provided
    for file_root in file_roots:
        # Extract voice_id and construct the directory path
        voice_id = file_root.split('_')[0]  # Assuming the voice_id is the prefix before the first underscore
        directory = os.path.join(directory_base, voice_id)
        
        # Construct the full path to the txt file
        txt_file_path = os.path.join(directory, f"{file_root}.txt")
        
        # Check if the txt file exists
        if os.path.exists(txt_file_path):
            # Read the contents of the txt file
            with open(txt_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                texts.append(content)
        else:
            print(f"File not found: {txt_file_path}")
            
    return texts

texts = read_txt_files(all_files)



def phonemize_texts(texts, language='en-us'):
    phonemized_texts = []

    # Phonemize each text in the list
    for text in texts:
        phonemized_text = phonemize(
            text,
            backend="espeak",
            language=language,
            strip=False,
            preserve_punctuation=True,
            with_stress=True
        )
        phonemized_texts.append(phonemized_text)
    
    return phonemized_texts


p_txts = phonemize_texts(texts)
print(p_txts)
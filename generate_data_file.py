import os
import random
import sys
import argparse
from phonemizer import phonemize
# from phonemizer.backend.espeak.wrapper import EspeakWrapper

# Set library path for eSpeak phonemization
# _ESPEAK_LIBRARY = '/opt/homebrew/Cellar/espeak/1.48.04_1/lib/libespeak.1.1.48.dylib'
# EspeakWrapper.set_library(_ESPEAK_LIBRARY)

speaker_num = random.randint(1000, 9999)

def find_wavs_with_non_empty_txt(directory):
    matched_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                wav_path = os.path.join(root, file)
                txt_path = os.path.splitext(wav_path)[0] + '.txt'
                if os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
                    matched_files.append(os.path.splitext(file)[0])
    return matched_files

def read_txt_files(file_roots, directory_base="outputs"):
    texts = []
    for file_root in file_roots:
        voice_id = file_root.split('_')[0]
        directory = os.path.join(directory_base, voice_id)
        txt_file_path = os.path.join(directory, f"{file_root}.txt")
        if os.path.exists(txt_file_path):
            with open(txt_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                texts.append(content)
        else:
            print(f"File not found: {txt_file_path}")
    return texts

def phonemize_texts(texts, language='en-us'):
    return phonemize(texts, backend="espeak", language=language, strip=False, preserve_punctuation=True, with_stress=True)

def main(speaker_id):
    directory = f'outputs/{speaker_id}'
    all_files = find_wavs_with_non_empty_txt(directory)
    print(f'Found {len(all_files)} files with non-empty txt files')
    texts = read_txt_files(all_files)
    print(f'Generated texts for {len(texts)} files')
    p_txts = phonemize_texts(texts)
    print(f'Phonemized {len(p_txts)} texts')
    if not os.path.exists('txts'):
        os.makedirs('txts')
    with open(f'txts/{speaker_id}.txt', 'w', encoding='utf-8') as file:
        for file_root, p_txt in zip(all_files, p_txts):
            line = f"{file_root}.wav|{p_txt}|{speaker_num}\n"
            file.write(line)
    print(f"Output file created: txts/{speaker_id}.txt")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('speaker_id', type=str, help='An integer for the speaker ID')
    args = parser.parse_args()
    main(args.speaker_id)

import os

def combine_text_files(source_dir, output_file):
    """
    Combine all text files in the specified directory into a single file without any gaps between them.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(source_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(source_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    contents = infile.read()
                    outfile.write(contents)  # Directly write the contents, no newlines added

def split_data(combined_file, train_file, val_file, train_ratio=0.8):
    """
    Split the combined file into training and validation files based on the train_ratio.
    """
    with open(combined_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        train_size = int(len(lines) * train_ratio)
        train_lines = lines[:train_size]
        val_lines = lines[train_size:]

    with open(train_file, 'w', encoding='utf-8') as file:
        file.writelines(train_lines)

    with open(val_file, 'w', encoding='utf-8') as file:
        file.writelines(val_lines)

def main():
    source_dir = 'txts'
    combined_file = 'combined.txt'
    train_file = 'train_list.txt'
    val_file = 'val_list.txt'
    
    # Combine all text files into one without gaps
    combine_text_files(source_dir, combined_file)
    
    # Split the combined text into training and validation files
    split_data(combined_file, train_file, val_file)

if __name__ == '__main__':
    main()

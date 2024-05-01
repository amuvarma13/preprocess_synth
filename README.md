# preprocess_synth

Step 1 download all the wav files




Step 2 Generate the data files

Now we need to check which wav files are good and can be phonemized and generate data files for these

```
for dir in outputs/*; do
    if [ -d "$dir" ]; then
        subdir_name=$(basename "$dir")
        python3 generate_data_file.py "$subdir_name"
    fi
done
```

Here is a simple bash script for this. 
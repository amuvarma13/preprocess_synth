# preprocess_synth

Step 1 Download all the wav files

The main.py script calls the download on a specific folder. You can update the ids.csv  to reflect this. The script that calls main.py on 
all folders is run_main.py; call:

```
python run_main.py
```

Step 2 Rename all files

You can run rename_wavs.py on a specific directory by

``` 
python rename_wavs.py dirname
```





Step 3 Generate the data files

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
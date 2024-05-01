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

Step 4 Generate train and val txts

Now we can run the bash script to run `train_list.txt` and `val_list.txt`

```
python generate_train_and_val.py
```

Step 5 Upload all wav files to storage

Run the script to upload all files flatly to cloud storage:

First we have to add the service account to path. 

```
export GOOGLE_APPLICATION_CREDENTIALS="service.json"
```


```
python upload_wavs.py
```



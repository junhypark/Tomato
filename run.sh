#!/bin/bash

read -p "Enter the input video file name : " video_file
read -p "Enter the input docx file name : " docx_file
read -p "Enter the name of output wav file name : " wav_file

if [ -z "$video_file" ]; then
    echo "Error: Video file name is required."
    exit 1
fi

if [ -z "$docx_file" ]; then
    echo "Error: DOCX file name is required."
    exit 1
fi

if [ -z "$wav_file" ]; then
    echo "Error: Output WAV file name is required."
    exit 1
fi

python3 init.py "$video_file" "$docx_file" "$wav_file"
python3 generate_tts.py "$video_file" "$wav_file"


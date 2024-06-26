read -p "Enter the root path name : " root_path
read -p "Enter the input video file name : " video_file
read -p "Enter the input docx file name : " docx_file
read -p "Enter the name of output wav file name : " wav_file

if [ -z "$root_path" ]; then
    echo "Error: Root path name is required."
    exit 1
fi

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

python init.py "$root_path" "$video_file" "$docx_file" "$wav_file"
python generate_tts.py "$video_file" "$wav_file" "$root_path"


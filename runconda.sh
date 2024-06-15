read -p "Enter the base path: " root_path
read -p "Enter the conda env name: " conda_env
read -p "Enter the input video file name : " video_file
read -p "Enter the input docx file name : " docx_file
read -p "Enter the name of output wav file name : " wav_file

if [ -z "$root_path" ]; then
    echo "Error: root path is required."
    exit 1
fi

if [ -z "$conda_env" ]; then
    echo "Error: conda env name is required."
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

source ~/anaconda3/etc/profile.d/conda.sh
conda activate "$conda_env"
python init.py "$root_path" "$video_file" "$docx_file" "$wav_file"
python generate_tts.py "$video_file" "$wav_file" "$root_path"


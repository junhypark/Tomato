if [ "$#" -ne 5 ]; then
    echo "Usage: bash webrun.sh <CONDA_ENV_NAME> <VIDEO_FILE_NAME> <DOCX_FILE_NAME> <WAV_FILE_NAME> <ROOT_PATH>"
    exit 1
fi

input1=$1
input2=$2
input3=$3
input4=$4
input5=$5
input6=$6

echo "Input1: $input1"
echo "Input2: $input2"
echo "Input3: $input3"
echo "Input4: $input4"
echo "Input5: $input5"

source ~/anaconda3/etc/profile.d/conda.sh

conda activate "$input1"

python  "$input5"/init.py "$input5" "$input2" "$input3" "$input4"
python  "$input5"/generate_tts.py "$input2" "$input4" "$input5"
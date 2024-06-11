from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE

app = Flask(__name__)

UPLOAD_FOLDER = '\\\\wsl.localhost\\Ubuntu-20.04\\<YOUR_WSL_INPUT_FOLDER_PATH>'
OUTPUT_FOLDER = '\\\\wsl.localhost\\Ubuntu-20.04\\<YOUR_WSL_OUTPUT_FOLDER_PATH>'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files or 'file' not in request.files:
        return jsonify(error='No file part'), 400
    
    video = request.files['video']
    docx = request.files['file']

    if video.filename == '' or docx.filename == '':
        return jsonify(error='No selected file'), 400

    video_filename = secure_filename(video.filename)
    docx_filename = secure_filename(docx.filename)

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    docx_path = os.path.join(app.config['UPLOAD_FOLDER'], docx_filename)

    video.save(video_path)
    docx.save(docx_path)

    try:
        # Replace these filenames with the correct ones as needed
        audio_filename = 'marriage.wav'
        wsl_conda_env = "tomato"
        wsl_video_path = video_filename
        wsl_docx_path = docx_filename
        wsl_audio_path = audio_filename

        # Make sure the paths are correct and the files exist
        wsl_input_path = '<YOUR_WSL_INPUT_FOLDER_PATH>'
        command = f'wsl bash -c "cd {wsl_input_path} && bash ../webrun.sh {wsl_conda_env} {wsl_video_path} {wsl_docx_path} {wsl_audio_path}"'
        
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Python script error: {stderr.decode('utf-8')}")
            return jsonify(error='Python script error', details=stderr.decode('utf-8')), 500

        result_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'result.mp4')
        
        # Ensure the file exists before returning it
        if not os.path.exists(result_file_path):
            print(f"Result file not found: {result_file_path}")
            return jsonify(error='Result file not found'), 404

        return jsonify(message='Files processed successfully', output=result_file_path)

    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify(error='Server error', details=str(e)), 500

@app.route('/download', methods=['GET'])
def download_file():
    file_path = request.args.get('path')
    if not file_path:
        return jsonify(error='File path is required'), 400
    
    # Use the output folder path directly
    wsl_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'result.mp4')
    print(f"File path: {wsl_file_path}")

    if not os.path.exists(wsl_file_path):
        return jsonify(error='File not found', path=wsl_file_path), 404

    return send_file(wsl_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=3001, debug=True)

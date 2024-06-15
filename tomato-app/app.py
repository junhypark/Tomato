from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE
from urllib.parse import unquote
import json

app = Flask(__name__)

WSL_FOLDER = '\\\\wsl.localhost\\Ubuntu-20.04\\'

def concat(root):
    global WSL_FOLDER
    
    re = ''

    for i in root.split('/')[1:]:
        re += i + '\\'

    return WSL_FOLDER +re+'input', WSL_FOLDER +re+'output'

@app.route('/upload', methods=['POST'])
def upload_file():
    global WSL_FOLDER

    if 'video' not in request.files or 'file' not in request.files:
        return jsonify(error='No file part'), 400
    
    video = request.files['video']
    docx = request.files['file']
    wsl_path = request.form.get('wslPath')
    conda_env = request.form.get('condaEnv')

    root = os.path.join(WSL_FOLDER, wsl_path)
    app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'] = concat(wsl_path)

    if video.filename == '' or docx.filename == '':
        return jsonify(error='No selected file'), 400

    if not wsl_path or not conda_env:
        return jsonify(error='Missing input values'), 400

    video_filename = secure_filename(video.filename)
    docx_filename = secure_filename(docx.filename)

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    docx_path = os.path.join(app.config['UPLOAD_FOLDER'], docx_filename)

    video.save(video_path)
    docx.save(docx_path)

    try:
        audio_filename = 'marriage.wav'

        # Make sure the paths are correct and the files exist
        wsl_input_path = wsl_path + '/input'
        command = f'wsl bash -c "cd {wsl_input_path} && bash ../webrun.sh {conda_env} {video_filename} {docx_filename} {audio_filename} {wsl_path}"'
        
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Python script error: {stderr.decode('utf-8')}")
            return jsonify(error='Python script error', details=stderr.decode('utf-8')), 500

        result_file_path = app.config['OUTPUT_FOLDER'] + '\\result.mp4'
        
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
    file_path = unquote(request.args.get('path'))
    if not file_path:
        return jsonify(error='File path is required'), 400

    print(f"File path: {file_path}")

    if not os.path.exists(file_path):
        return jsonify(error='File not found', path=file_path), 404

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=3001, debug=True)

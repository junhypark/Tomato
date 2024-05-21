from moviepy.editor import VideoFileClip
from docx import Document


def extract_audio_from_video(video_file_path, audio_file_path):
    video = VideoFileClip("./input/"+video_file_path)

    video.audio.write_audiofile("./output/"+audio_file_path, codec='pcm_s16le')

def open_docx(docx_file_path):
    return Document(docx_file_path)

def main(video_file, audio_file, docx_file):
    # video_file = 'INPUT NAME OF VIDEO.mp4'
    # audio_file = 'OUTPUT NAME OF AUDIO.wav'
    # docx_file = './input/INPUT NAME OF DOCX.docx'
    
    extract_audio_from_video(video_file, audio_file)
    return audio_file, open_docx(docx_file)
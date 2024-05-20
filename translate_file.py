from moviepy.editor import VideoFileClip
from docx import Document


def extract_audio_from_video(video_file_path, audio_file_path):
    video = VideoFileClip(video_file_path)

    video.audio.write_audiofile(audio_file_path, codec='pcm_s16le')

def open_docx_per_paragraph(docx_file_path):
    docx = Document(docx_file_path)
    result = list()
    
    for x, paragraph in enumerate(docx.paragraphs):
        result.append({str(x): paragraph.text})

    return result

def main(video_file, audio_file, docx_file):
    # video_file = './input/INPUT NAME OF VIDEO.mp4'
    # audio_file = './output/OUTPUT NAME OF AUDIO.wav'
    # docx_file = './input/INPUT NAME OF DOCX.docx'
    
    extract_audio_from_video(video_file, audio_file)
    return open_docx_per_paragraph(docx_file)
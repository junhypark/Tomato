from moviepy.editor import VideoFileClip
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

num_count = 0

def extract_audio_from_video(video_file_path, audio_file_path):
    video = VideoFileClip("./input/"+video_file_path)

    video.audio.write_audiofile("./output/"+audio_file_path, codec='pcm_s16le')

def is_list(paragraph):
    p = paragraph._element
    for e in p.xpath(".//w:numPr"):
        return True
    return False

def get_list_level(paragraph):
    p = paragraph._element
    num_elements = p.xpath(".//w:numId")
    if num_elements:
        return int(num_elements[0].get(qn("w:val")))
    return None

def get_list_number(paragraph):
    global num_count

    num_id = get_list_level(paragraph)
    if num_id is not None:
        num_count += 1
        return f"{num_id+num_count-1}."
    return ""

def open_docx(docx_file_path):
    doc = Document(docx_file_path)
    result = ''

    for paragraph in doc.paragraphs:
        if is_list(paragraph):
            id= get_list_number(paragraph)
            result += (f"{id} {paragraph.text}\n")
        else:
            result += paragraph.text + "\n"
    return result

def main(video_file, audio_file, docx_file):
    # video_file = 'INPUT NAME OF VIDEO.mp4'
    # audio_file = 'OUTPUT NAME OF AUDIO.wav'
    # docx_file = './input/INPUT NAME OF DOCX.docx'
    
    extract_audio_from_video(video_file, audio_file)
    return audio_file, open_docx(docx_file)
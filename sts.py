import re
from sentence_transformers import SentenceTransformer, util

# 문장 구분을 위한 함수
def parse_dialogues(text):
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())
    return sentences

# 스크립트 파싱 함수
def parse_script(script_text):
    scenes = {}
    current_scene = None
    current_content = []
    scene_pattern = re.compile(r'^(\d+)\.\s*(.*?)\s*$')

    for line in script_text.split('\n'):
        line = line.strip()
        scene_match = scene_pattern.match(line)
        if scene_match:
            if current_scene is not None:
                scenes[current_scene] = extract_dialogues(current_content)
            current_scene = f"{scene_match.group(1)}. {scene_match.group(2)}"
            current_content = []
        else:
            current_content.append(line)
    
    if current_scene:
        scenes[current_scene] = extract_dialogues(current_content)

    return scenes

# 대화 추출 함수
def extract_dialogues(content):
    dialogues = []
    dialogue_pattern = re.compile(r'^(\w+)(?:\s*\(.*?\))?\s*(.*)$')
    for line in content:
        line = line.strip()
        match = dialogue_pattern.match(line)
        if match:
            dialogue = re.sub(r'\[.*?\]', '', match.group(2)).strip()
            dialogues.append(dialogue)
    return dialogues

# 대화 비교 함수
def compare_dialogues(scenes, movie_dialogues):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    movie_dialogues_encoded = model.encode(movie_dialogues)
    results = []

    for scene, dialogues in scenes.items():
        if dialogues:
            scene_dialogues_encoded = model.encode(dialogues)
            similarities = util.pytorch_cos_sim(movie_dialogues_encoded, scene_dialogues_encoded)

            for movie_index, movie_dialogue in enumerate(movie_dialogues):
                max_similarity = similarities[movie_index].max().item()
                best_match_index = similarities[movie_index].argmax().item()
                best_match_dialogue = dialogues[best_match_index]
                results.append((movie_dialogue, best_match_dialogue, scene, max_similarity))
    
    return results

# 스크립트와 대화 샘플

def main(text, script):
    # 대화를 파싱하고 비교
    movie_dialogues_text = text
    script_text = script
    movie_dialogues = parse_dialogues(movie_dialogues_text)
    scenes = parse_script(script_text)
    comparison_results = compare_dialogues(scenes, movie_dialogues)

    # 결과 출력
    for movie_dialogue, best_match_dialogue, scene, similarity in comparison_results:
        print(f"Movie Dialogue: '{movie_dialogue}'")
        print(f"Most Similar Scene Dialogue: '{best_match_dialogue}'")
        print(f"Scene: {scene}")
        print(f"Similarity: {similarity:.2f}")
        print("\n---\n")
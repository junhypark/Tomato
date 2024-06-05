import re
from sentence_transformers import SentenceTransformer, util

def parse_scenario(scenario_text):
    scenes = []
    scene_num = None
    s_line = ''
    s_text_list = []

    for i in scenario_text.split('\n'):
        new_scene_num = re.findall(r'^(\d+\.\s)', i)
        if new_scene_num:
            if scene_num:
                s_text_list.append((scene_num, s_line.strip()))
            s_line = ''
            scene_num = new_scene_num[0].strip()
        else:
            s_line += '\n' + i

    if scene_num:
        s_text_list.append((scene_num, s_line.strip()))

    for i in s_text_list:
        liness = i[1].split('\n\n')
        for lines in liness:
            lines = re.findall(r'(^[가-힣0-9\s]{2,6})(\(Na\))?\n([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)', lines)

            if lines:
                for line in lines:
                    clean_li = re.sub(r'\([^)]*\)', '', line[2])
                    clean_line = re.sub(r'\n', '', clean_li)
                    if len(clean_line) >= 2:
                        scenes.append((i[0], clean_line))

    return scenes

def parse_movie_dialogues(movie_dialogue_text):
    result = list()

    for i in movie_dialogue_text:
        sentences = re.split(r'(?<=[.?!])\s+|\n', i["text"].strip())
        [result.append({"text": sentence, "start": i["start"],"end": i["end"]}) for sentence in sentences if len(sentence) > 5]

    return result

def compare_dialogues(scenes, movie_dialogues, model, threshold=0.5):
    if not scenes or not movie_dialogues:
        raise ValueError("Scenes and movie dialogues must not be empty.")

    detailed_results = []
    scene_sentences = [(scenes[i]["text"], i) for i in range(len(scenes)) if scenes[i]["person"] != "none"]
    scene_embeddings = model.encode([ss[0] for ss in scene_sentences])

    if len(scene_sentences) == 0 or len(movie_dialogues) == 0:
        return []

    used_scene_indices = set()

    for dialogue in movie_dialogues:
        dialogue_sentences = re.split(r'(?<=[.!?])\s+', dialogue["text"].strip())
        for dialogue_sentence in dialogue_sentences:
            dialogue_embedding = model.encode([dialogue_sentence])[0]
            similarities = util.cos_sim(dialogue_embedding, scene_embeddings)[0]

            best_match_idx = -1
            best_similarity = -1

            for idx, similarity in enumerate(similarities):
                if similarity > best_similarity and idx not in used_scene_indices:
                    best_similarity = similarity
                    best_match_idx = idx

            if best_similarity > threshold and best_match_idx != -1:
                scene, sentence = scenes[best_match_idx]
                detailed_results.append((dialogue_sentence, sentence, scene, best_similarity))
                used_scene_indices.add(best_match_idx)

    return detailed_results

def get_best_scene_order(detailed_results):
    scene_list = [result[2] for result in detailed_results]
    consecutive_scenes = []
    current_scene = None
    count = 0

    for i in range(len(scene_list) - 1):
        if scene_list[i] == scene_list[i + 1]:
            if scene_list[i] != current_scene:
                current_scene = scene_list[i]
                count = 2
            else:
                count += 1
        else:
            if count >= 2:
                consecutive_scenes.append(current_scene)
            current_scene = None
            count = 0

    if count >= 2:
        consecutive_scenes.append(current_scene)

    return consecutive_scenes

def refine_comparisons(best_scene_order, scenes, movie_dialogues, model, threshold=0.5):
    refined_results = []

    used_scene_indices = set()

    for dialogue in movie_dialogues:
        dialogue_sentences = re.split(r'(?<=[.!?])\s+', dialogue.strip())
        for dialogue_sentence in dialogue_sentences:
            dialogue_embedding = model.encode([dialogue_sentence])[0]
            similarities = []
            for idx, (scene, sentence) in enumerate(scenes):
                if scene in best_scene_order and idx not in used_scene_indices:
                    sentence_embedding = model.encode([sentence])[0]
                    similarity = util.cos_sim(dialogue_embedding, sentence_embedding).item()
                    similarities.append((idx, scene, sentence, similarity))

            if similarities:
                best_match = max(similarities, key=lambda x: x[3])
                if best_match[3] > threshold:
                    refined_results.append((dialogue_sentence, best_match[2], best_match[1], best_match[3]))
                    used_scene_indices.add(best_match[0])

    return refined_results

def filter_non_consecutive_scenes(results):
    filtered_results = []
    current_scene = None
    count = 0

    for i in range(len(results) - 1):
        if results[i][2] == results[i + 1][2]:
            if results[i][2] != current_scene:
                current_scene = results[i][2]
                count = 2
            else:
                count += 1
        else:
            if count >= 2:
                filtered_results.extend(results[i-count+1:i+1])
            current_scene = None
            count = 0

    if count >= 2:
        filtered_results.extend(results[-count:])

    return filtered_results

# 모델 로드
model = SentenceTransformer('jhgan/ko-sbert-sts')



# 시나리오 및 영화 대사 파싱
scenes = parse_scenario(scenario_text)
movie_dialogues = parse_movie_dialogues(movie_dialogue_text)

# 대사 비교
detailed_results = compare_dialogues(scenes, movie_dialogues, model, threshold=0.6)

# 최적의 씬 순서 찾기
best_scene_order = get_best_scene_order(detailed_results)

# 최적의 씬 순서로 텍스트 비교
refined_results = refine_comparisons(best_scene_order, scenes, movie_dialogues, model, threshold=0.6)

# 두 번 이상 연속되지 않은 씬 필터링
filtered_results = filter_non_consecutive_scenes(refined_results)

# 씬별 문장 출력
print("시나리오 씬별 문장:")
for scene, sentence in scenes:
    print(f"{scene}: {sentence}")

# 영화 대사 출력
print("\n영화 대사:")
for dialogue in movie_dialogues:
    print(dialogue)

# 최적의 씬 순서 결과 출력
print("\n최적의 씬 순서:")
print(best_scene_order)

# 각 영화 대사에 대해 가장 유사한 씬 문장과 그 씬을 출력
print("\n영화 대사와 유사한 씬 문장 비교 결과:")
for result in filtered_results:
    movie_dialogue, best_match_sentence, scene, similarity = result
    print(f"영화 대사: {movie_dialogue}\n가장 유사한 씬 문장: {best_match_sentence}\n씬: {scene}\n유사도: {similarity}\n")

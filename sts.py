import re
from sentence_transformers import SentenceTransformer, util

def parse_movie_dialogues(movie_dialogue_text):
    result = list()

    for i in movie_dialogue_text:
        sentences = re.split(r'(?<=[.?!])\s+|\n', i["text"].strip())
        [result.append({"text": sentence, "start": i["start"],"end": i["end"]}) for sentence in sentences if len(sentence) > 5]

    return result

def compare_dialogues(scenes, movie_dialogues, model, threshold=0.7):
    if not scenes or not movie_dialogues:
        raise ValueError("Scenes and movie dialogues must not be empty.")

    detailed_results = []
    scene_sentences = [(scenes[i]["text"], i) for i in range(len(scenes)) if scenes[i]["person"] != "none"]
    scene_embeddings = model.encode([ss[0] for ss in scene_sentences])

    if len(scene_sentences) == 0 or len(movie_dialogues) == 0:
        return []

    for dialogue in movie_dialogues:
        dialogue_embedding = model.encode([dialogue["text"]])[0]
        similarities = util.cos_sim(dialogue_embedding, scene_embeddings)[0]

        # Get the best match for each dialogue
        best_match_idx = similarities.argmax().item()
        best_similarity = similarities[best_match_idx].item()

        if best_similarity > threshold:
            detailed_results.append((dialogue, scene_sentences[best_match_idx][0], scenes[scene_sentences[best_match_idx][1]]["sn"], best_similarity, scene_sentences[best_match_idx][1]))

    return detailed_results

def get_best_scene_order(detailed_results):
    # Extract scenes in order of their appearance in detailed_results
    scene_list = [result[2] for result in detailed_results]

    # Identify scenes that appear consecutively more than once
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

def refine_comparisons(best_scene_order, scenes, movie_dialogues, model, threshold=0.7):
    refined_results = []

    for dialogue in movie_dialogues:
        dialogue_embedding = model.encode([dialogue["text"]])[0]
        similarities = []
        for i in range(len(scenes)):
            if scenes[i]["sn"] in best_scene_order and scenes[i]["person"] != 'none':
                sentence_embedding = model.encode([scenes[i]["text"]])[0]
                similarity = util.cos_sim(dialogue_embedding, sentence_embedding).item()
                similarities.append((scenes[i]["sn"], scenes[i]["text"], similarity, i))

        if similarities:
            best_match = max(similarities, key=lambda x: x[2])
            if best_match[2] > threshold:
                refined_results.append((dialogue["text"], dialogue["start"], dialogue["end"], best_match[1], best_match[0], best_match[2], best_match[3]))

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

def main(movie_dialogue_text, scenario_text):
    # 모델 로드
    model = SentenceTransformer('jhgan/ko-sbert-sts')

    movie_dialogues = parse_movie_dialogues(movie_dialogue_text)

    # 대사 비교
    detailed_results = compare_dialogues(scenario_text, movie_dialogues, model, threshold=0.6)

    # 최적의 씬 순서 찾기
    best_scene_order = get_best_scene_order(detailed_results)

    # 최적의 씬 순서로 텍스트 비교
    refined_results = refine_comparisons(best_scene_order, scenario_text, movie_dialogues, model, threshold=0.6)

    # 두 번 이상 연속되지 않은 씬 필터링
    filtered_results = filter_non_consecutive_scenes(refined_results)

    # 씬별 문장 출력
    print("시나리오 씬별 문장:")
    for scene in scenario_text:
        print(scene["sn"], ":" , scene["text"])

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
        movie_dialogue, start, end, best_match_sentence, scene, similarity, index = result
        print(f"영화 대사: {movie_dialogue}\n가장 유사한 씬 문장: {best_match_sentence}\n씬: {scene}\n유사도: {similarity}\n인덱스: {index}\n시간: {start}~{end}\n")
    return filtered_results, best_scene_order
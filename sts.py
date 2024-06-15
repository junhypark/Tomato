import re
from sentence_transformers import SentenceTransformer, util

def parse_scenario(scenario_text):
    tt = []
    nn = []
    cc = []
    for line in scenario_text.split('\n\n'):
        t = re.findall(r'[가-힣]{1,}(\(V\.O\.\))?\s?(\(NA\))?(\s*)?\t{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line)
        if len(t) !=0 :
            tt.append(line)
        n = re.findall(r'^(\(?[가-힣]{1,}\)?(\(V\.O\.\))?\s?(\(Na\))?\n{1,})([가-힣\.\,\!\?\s\t]*)',line)
        if len(n) !=0:
            nn.append(line)
        c = re.findall(r'[가-힣]{1,}(\(V\.O\.\))?\s?(\(NA\))?(\s)*\:([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line)
        if len(c) !=0:
            cc.append(line)

    listtype=[('tt', tt), ('nn', nn), ('cc', cc)]
    stype = max(listtype, key=lambda k: len(k[1]))[0]

    print('Type is ', stype)

    if stype=='tt':
        return tapp(scenario_text)
    elif stype=='nn':
        return neww(scenario_text)
    elif stype=='cc':
        return coll(scenario_text)

def neww(scenario_text):
    scenes = []
    scene_num = None
    s_line = ''
    s_text_list = []
    for i in scenario_text.split('\n'):
            new_scene_num = re.findall(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)(\.)(.+)', i)
            if new_scene_num:
                if scene_num:
                    s_text_list.append((scene_num, s_line.strip()))
                s_line = ''
                scene_num = new_scene_num[0]  #.strip()
            else:
                s_line += '\n' + i
    
    if scene_num:
        s_text_list.append((scene_num, s_line.strip()))
    
    for i in s_text_list:
        liness = i[1].split('\n\n')
        for lines in liness:                                        
            lines = re.findall(r'^([가-힣]{1,5}[0-9]?[A-z]?[a-z]?\s?)(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?\n{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',lines)
            for line in lines:
                textd = line[11].replace('\n', '').strip()
                textd = textd.replace('\t', '').strip()
                textd = textd.replace('\s', '').strip()
                texxt=re.sub(r'\(.*?\)', '', textd).strip()
                for linee in re.split('[.!?]', texxt):    
                    if len(re.sub(' ', '', linee)) >= 2:
                        scenes.append((i[0], linee))               
    return scenes

def tapp(scenario_text):
    scenes = []
    scene_num = None
    s_line = ''
    s_text_list = []
    for i in scenario_text.split('\n'):
            new_scene_num = re.findall(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)(\.)(.+)', i)
            if new_scene_num:
                if scene_num:
                    s_text_list.append((scene_num, s_line.strip()))
                s_line = ''
                scene_num = new_scene_num[0]  #.strip()
            else:
                s_line += '\n' + i
    
    if scene_num:
        s_text_list.append((scene_num, s_line.strip()))
    
    for i in s_text_list:
        liness = i[1].split('\n\n')
        for lines in liness:                                         
            lines = re.findall(r'^([가-힣]{1,5}[0-9]?[a-z]?\s?)(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?\t{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',lines)
            for line in lines:
                textd = line[11].replace('\n', '').strip()
                textd = textd.replace('\t', '').strip()
                textd = textd.replace('\s', '').strip()
                texxt=re.sub(r'\(.*?\)', '', textd).strip()
                for linee in re.split('[.!?]', texxt):    
                    if len(re.sub(' ', '', linee)) >= 2:
                        scenes.append((i[0], linee))                    
    return scenes

def coll(scenario_text):
    scenes = []
    scene_num = None
    s_line = ''
    s_text_list = []
    for i in scenario_text.split('\n'):
            new_scene_num = re.findall(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)(\.)(.+)', i)
            if new_scene_num:
                if scene_num:
                    s_text_list.append((scene_num, s_line.strip()))
                s_line = ''
                scene_num = new_scene_num[0]
            else:
                s_line += '\n' + i
    
    if scene_num:
        s_text_list.append((scene_num, s_line.strip()))
    
    for i in s_text_list:
        liness = i[1].split('\n\n')
        for lines in liness:                                         
            lines = re.findall(r'^([가-힣]{1,5}[0-9]?[a-z]?\s?)(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?\t{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',lines)
            for line in lines:
                textd = line[11].replace('\n', '').strip()
                textd = textd.replace('\t', '').strip()
                textd = textd.replace('\s', '').strip()
                texxt=re.sub(r'\(.*?\)', '', textd).strip()
                for linee in re.split('[.!?]', texxt):    
                    if len(re.sub(' ', '', linee)) >= 2:
                        scenes.append((i[0], linee))
                    
    return scenes

def parse_movie_dialogues(movie_dialogue_text):
    sentences = re.split(r'(?<=[.?!])\s+|\n', movie_dialogue_text.strip())
    return [sentence for sentence in sentences if len(sentence) > 5]

def compare_dialogues(scenes, movie_dialogues, model, threshold=0.5):
    if not scenes or not movie_dialogues:
        raise ValueError("Scenes and movie dialogues must not be empty.")

    detailed_results = []
    scene_sentences = [sentence for scene, sentence in scenes]
    scene_embeddings = model.encode(scene_sentences)    # From Web

    if len(scene_sentences) == 0 or len(movie_dialogues) == 0:
        return []

    used_scene_indices = set()

    for dialogue in movie_dialogues:
        dialogue_sentences = re.split(r'(?<=[.!?])\s+', dialogue.strip())
        for dialogue_sentence in dialogue_sentences:
            dialogue_embedding = model.encode([dialogue_sentence])[0]   # From Web
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
            dialogue_embedding = model.encode([dialogue_sentence])[0]   # From Web
            similarities = []
            for idx, (scene, sentence) in enumerate(scenes):
                if scene in best_scene_order and idx not in used_scene_indices:
                    sentence_embedding = model.encode([sentence])[0]    # From Web
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

def main(scenario_text, movie_dialogue_text):
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')  # From Web

    scenes = parse_scenario(scenario_text)
    movie_dialogues = parse_movie_dialogues(movie_dialogue_text)

    detailed_results = compare_dialogues(scenes, movie_dialogues, model, threshold=0.6)

    best_scene_order = get_best_scene_order(detailed_results)

    refined_results = refine_comparisons(best_scene_order, scenes, movie_dialogues, model, threshold=0.6)

    filtered_results = filter_non_consecutive_scenes(refined_results)

    print("\n최적의 씬 순서:")
    print(best_scene_order)

    print("\n영화 대사와 유사한 씬 문장 비교 결과:")
    for result in filtered_results:
        movie_dialogue, best_match_sentence, scene, similarity = result
        print(f"영화 대사: {movie_dialogue}\n가장 유사한 씬 문장: {best_match_sentence}\n씬: {scene}\n유사도: {similarity}\n")
    
    del model

    return filtered_results

# Rest of code lines are made
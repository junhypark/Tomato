import re

# flag: 씬헤드라인:0, 대사: 1, 지문: 2

# lineInfo = {'text':line  , 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum   }

def check_blank(scene, dia, best_scenes, blank=None):
    # scene => [{text, person, start, end, flag, sn}]
    # blank => [{speak1, speak2}]
    # dia => movie_dialogue, start, end, best_match_sentence, scene, similarity, index = result
    result = list()
    
    for d in dia:
        for sc in scene:
            if d[3] == sc["text"] and d[4] == sc["sn"]:
                sc["start"] = d[1]
                sc["end"] = d[2]

    for b in blank:
        time_check = dict()
        can_index = list()
        for bs in best_scenes:
            for s in range(len(scene)):
                if b["speak1"] == scene[s]["end"]:
                    time_check["blank_start"] = s
                elif b["speak2"] == scene[s]["start"]:
                    time_check["blank_end"] = s
                elif scene[s]["sn"] != bs:
                    time_check["blank_end"] = s-1
                    time_check["blank_start"] = s-1

            can_index = scene[time_check["blank_start"]+1:time_check["blank_end"]]
            result.append({"comment": can_index, "sn":bs})
    
    final = list()

    for r in result:
        temp = dict()
        temp["sn"] = r["sn"]
        temp["fi_com"] = [scene[i]["text"] for i in r["comment"] if scene[i]["flag"] == 2]
        final.append(temp)

    return final    


def main(text):
    textt=text.split('\n\n')
    textt

    totalSS = list()

    snum = 0
    flag_num = 0

    for line in textt:

        if len(line) == 0:
            continue
        # 씬헤드라인 구분
        if re.match(r'^(?:\n)?(\d+)(\.)(.+)', line):
            match = re.match(r'^(?:\n)?(\d+)(\.)(.+)', line)
            snum = match.group(1)
            flag_num = 0

            totalSS.append({'text': snum+'.'+match.group(3)  , 'person': 'none', 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum})

        elif re.match(r'^([가-힣]{1,4})(\(Na\))?\n{1,}(.+)',line):  # 배역과 대사
            text = re.match(r'^([가-힣]{1,4})(\(Na\))?\n{1,}(.+)',line) # Na 등은 반영되지 않음
            flag_num = 1

            totalSS.append({'text': text.group(3)  , 'person': text.group(1), 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum})

        else:
            delete=['CUT TO', 'cut to', 'Cut to', 'Cut To', '\n', '\t']
            pattern = '|'.join(re.escape(word) for word in delete)
            flag_num = 2

            lineInfo = {'text': re.sub(pattern, '', line)  , 'person': 'none', 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum   }
            
            totalSS.append(lineInfo)


    return totalSS
import re

def check_blank(sc, dia, comment, blank):
    # scene => [{text, person, start, end, flag, sn}]
    # blank => [{speak1, speak2}]
    # comment => filtered
    # dia => movie_dialogue, start, end, best_match_sentence, scene, similarity, index = result
    result = list()
    pn_sn = 0

    for b in blank:
        for di in dia:
            
            if b["speak2"] == di["start"]:
                temp = -1
                temp2 = -1
                for fi in range(len(comment)):
                    if comment[fi][0] in di["text"]:
                        temp = fi
                        break
                for i in range(len(sc)):
                    if comment[temp][1] in sc[i]["text"]:
                        temp2 = i
                        pn_sn = sc[i]["sn"]
                        break
                
                if temp != -1 and temp2 != -1:
                    if sc[temp2-1]["sn"] != pn_sn and sc[temp2-1]["person"] == "none":
                        result.append({"start": b["speak1"], "end": b["speak2"], "text": sc[temp2-1]["text"], "sn": pn_sn, "sc": sc[temp2-1]})
                        
            
            elif b["speak1"] == di["end"]:
                temp = -1
                temp2 = -1
                for fi in range(len(comment)):
                    if comment[fi][0] in di["text"]:
                        temp = fi
                        break
                for i in range(len(sc)):
                    if comment[temp][1] in sc[i]["text"]:
                        temp2 = i
                        pn_sn = sc[i]["sn"]
                        break
                
                if temp != -1 and temp2 != -1:
                    if sc[temp2+1]["sn"] != pn_sn:
                        break
                    if sc[temp2+1]["person"] == "none":
                        result.append({"start": b["speak1"], "end": b["speak2"], "text": sc[temp2+1]["text"], "sn": pn_sn})
                        break
            
    
    # 시간이 긴 순서대로 (중복일 경우)
    unique_results = {}
    
    for r in result:
        text = r['text']
        duration = r['end'] - r['start']
        
        if text not in unique_results:
            unique_results[text] = r
        else:
            existing_duration = unique_results[text]['end'] - unique_results[text]['start']
            if duration > existing_duration:
                unique_results[text] = r
    
    return result

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

        elif re.match(r'^([가-힣]{1,4}[0-9]?)(\(Na\))?(\n{1,}(.+))+',line):  # 배역과 대사
            text = re.match(r'^([가-힣]{1,4}[0-9]?)(\(Na\))?\n{1,}(.+(\n)?)+',line, re.DOTALL) # Na 등은 반영되지 않음
            textd = text.group(3).replace('\n', '').strip()
            texxt=re.sub(r'\(.*?\)', '', textd).strip()
            flag_num = 1

            totalSS.append({'text': texxt  , 'person': text.group(1), 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum})
        else:
            delete=['CUT TO', 'cut to', 'Cut to', 'Cut To', '\n', '\t']
            pattern = '|'.join(re.escape(word) for word in delete)
            flag_num = 2

            lineInfo = {'text': re.sub(pattern, '', line)  , 'person': 'none', 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum   }
            
            totalSS.append(lineInfo)


    return totalSS
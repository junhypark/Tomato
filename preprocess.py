import re

# Made
def check_blank(sc, dia, comment, blank):
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
                    if sc[temp2-1]["text"] == "" or sc[temp2-1]["text"] == None or sc[temp2-1]["text"] == '\n':
                        pass
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
                    if sc[temp2+1]["text"] == "" or sc[temp2+1]["text"] == None or sc[temp2+1]["text"] == None:
                        pass
                    if sc[temp2+1]["person"] == "none":
                        result.append({"start": b["speak1"], "end": b["speak2"], "text": sc[temp2+1]["text"], "sn": pn_sn})
                        break
            
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

def taptap(textt):
    totalSS = list()
    delete=['CUT TO', 'cut to', 'Cut to', 'Cut To', '\n', '\t', '\s']
    nt=['\n',]
    pattern = '|'.join(re.escape(word) for word in delete)
    aa = []
    snum=0
    flag_num = 0

    for line in textt:
        if len(line) == 0:
            continue
        
        if re.match(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)', line):
            match = re.match(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)(\.)?(.+)', line)
            snum = match.group(1)
            flag_num = 0
    
            totalSS.append({'text': snum+'.'+match.group(3)  , 'person': 'none', 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum})
    
    
        elif re.match(r'([가-힣]{1,5}[0-9]?[a-z]?\s?)(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?\t{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line): # 배역과 대사
            text = re.match(r'([가-힣]{1,5}[0-9]?[a-z]?\s?)(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?\t{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line, re.DOTALL) # Na 등은 반영되지 않음
            textd = text.group(12).replace('\n', '').strip()
            textd = textd.replace('\t', '').strip()
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

def newnew(textt):
    totalSS = list()
    delete=['CUT TO', 'cut to', 'Cut to', 'Cut To', '\n', '\t']
    pattern = '|'.join(re.escape(word) for word in delete)

    snum = 0
    flag_num = 0
    
    for line in textt:
    
        if len(line) == 0:
            continue
        if re.match(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)(\.)?(.+)', line):
            match = re.match(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)(\.)?(.+)', line)
            snum = match.group(1)
            flag_num = 0
    
            totalSS.append({'text': snum+'.'+match.group(3)  , 'person': 'none', 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum})
    
    
        elif re.match(r'^([가-힣]{1,5}[0-9]?[A-z]?[a-z]?\s?)(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?\n{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line):  # 배역과 대사
            text = re.match(r'^([가-힣]{1,5}[0-9]?[A-z]?[a-z]?\s?)(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?\n{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line, re.DOTALL) # Na 등은 반영되지 않음
            #text = re.match(r'^([가-힣]{1,5}[0-9]?[a-z]?\s?)(\(V\.O\.\)?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?\n{1,}(\s*)?([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line, re.DOTALL)
            textd = text.group(12).replace('\n', '').strip()
            textd = textd.replace('\t', '').strip()
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

def colcol(textt):
    totalSS = list()
    delete=['CUT TO', 'cut to', 'Cut to', 'Cut To', '\n', '\t']
    pattern = '|'.join(re.escape(word) for word in delete)    
    aa = []

    snum = 0
    flag_num = 0
    
    for line in textt:
    
        if len(line) == 0:
            continue
        if re.match(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)(\.)?(.+)', line):
            match = re.match(r'^(?:\n)?(?:S#)?(?:#)?(?:#S)?(\d+)(\.)?(.+)', line)
            snum = match.group(1)
            flag_num = 0
    
            totalSS.append({'text': snum+'.'+match.group(3)  , 'person': 'none', 'start': 0 , 'end': 0, 'flag' : flag_num, 'sn':snum})
    
    
        elif re.match(r'[가-힣]{1,}(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?(\s)*\:([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line):  # 배역과 대사
            text = re.match(r'([가-힣]{1,5}[0-9]?[a-z]?\s?)(\(V\.O\.\))?(\(V\.O\))?(\(v\.o\.\))?(\(v\.o\))?\s?(\(NA\))?(\(Na\))?(\(na\))?(\(N\))?(\s*)?(\s)*\:([가-힣A-Za-z0-9\s\(\)\,\?\!\.\…]*)',line, re.DOTALL) # Na 등은 반영되지 않음
            textd = text.group(12).replace('\n', '').strip()
            textd = textd.replace('\t', '').strip()
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

def main(text):
    textt=text.split('\n\n')
    tt = []
    nn = []
    cc = []

    for line in textt:
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

    if stype=='tt':
        return taptap(textt)
        
    elif stype=='nn':
        return newnew(textt)
        
    elif stype=='cc':
        return colcol(textt)
# Made
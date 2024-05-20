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
script_text = """
29.	 한남분실. 아침 
한강변에 세워진 낮은 건물. 
커다란 여행가방을 든 하윤주. 긴장한 표정. [HN홀딩스]라 적힌 간판을 본다. 

로비
하윤주. 인터폰을 누르려는데 

황반장(OFF)
왔어?

황반장. 위이잉~ 전기면도기로 수염을 밀며 문을 열고 들어간다. 

감시반
책상에 앉아 있는 십여 명의 감시반들.   
커다란 지도를 보며 대화를 하는 사람. 수배자 몽타주를 넘겨보는 사람.

하윤주
???

복도를 지나다 낯익은 얼굴들에 당황하는 하윤주. 

감시반들 사이로 보이는 지하철 쇼핑녀. 신문을 보던 등산객.

실장실
벌컥! 문을 여는 황반장.
립스틱을 바르다 화들짝 놀라는 이실장. 시크한 느낌. 하이톤의 목소리. 

이실장
노크!!!

쾅! 재빨리 문을 닫는 황반장. 똑똑! 노크를 하고 다시 벌컥 열며

황반장
신입입니다. 

척! 경례를 붙이는 하윤주. 절도 있는 모습. 

하윤주
경찰대 29기 하윤주입니다. 
금일 특수범죄과 한남분실 근무를 명. 받았습니다. 

리포트와 하윤주를 번갈아 보는 이실장. 까칠한 표정.

[감시]. [단서획득]. [기억력] 등 모든 항목에 A+ 체크가 된 보고서.    

이실장
아슬 아슬 했네. 

마지막 메모 칸에 써있는 장난스런 손 글씨. [단점 : 손버릇이 고약함] 

웃음을 참는 이실장. 황반장을 째리다 하윤주를 본다. 

이실장
정했어?
하윤주
네?
이실장
코드네임. 안정했어?
하윤주
아닙니다. 꽃사슴으로 정했습니다. 
이실장
꽃?

회의실
스크린에 떠 있는 뚱의 사진. 

이실장
닉네임 물먹는 하마. 
어제 은행 건 외 3건의 현장에서 확인됐다. 
교통카드로 물건을 샀는데 덕분에 동선이 파악됐어.

삼삼오오 앉아있는 감시반. 정보팀들과 멀찍이 떨어진 하윤주의 모습.  
하윤주. 브리핑에 집중한 듯 툭. 툭툭. 손가락을 움직이고 있다. 

스크린화면 - 동선이 표시된 서울시 지도가 뜨고

이실장
서울 곳곳을 유랑하시는 와중에 oo동이 생활권으로 분석됐다. 
oo역을 중심으로 도보 20분 반경이 작전구역이다.  

황반장. 원경으로 찍힌 특공일행의 모습을 하나씩 가리키며 

황반장
운전 하나. 작업 넷. 안테나 하나. 총 여섯 분. 
건국 이래 가장 나이스한 도적떼다. 
 지금까지 피해액이 2백억이 넘어.
놈들이 열심히 버는 만큼 부끄럽지 않게 전력을 다하자고.
질문?

일제히 하윤주를 돌아보는 감시반. 정보팀. ‘뭐지?’ 하윤주가 고개를 들면 딴청을 피운다. 
 
황반장
아. 오늘 온 신입. 29기 하윤주.
이 쪽은 정보팀. 쩌~ 쪽은 같이 일 할 감시반. 

황반장. 손을 휘휘~ 저어가며 대충 소개를 하다 

황반장
아! 코드네임은... 꽃. 돼지다.

벌떡 일어서는 하윤주. 

하윤주
반장님!!!

‘어쭈?’ 돌아보는 황반장. 

황반장
왜?

하윤주를 보는 동료들. 썰렁해진 분위기. 

하윤주
쟈크... 열리셨습니다. 
황반장
...

굳은 표정으로 지익~! 쟈크를 올리는 황반장. 고개를 끄덕이며 사라진다. 

황반장
아거스!

장비실
이어몰드. 리시버. 소형카메라 등 각종 장비를 체크하는 전문적인 모습. 

하윤주. 목이 긴 기린과 이어몰드. 각종 장비를 테스트 중.  
황반장은 치질 방석. 목 베개 등을 챙기며 신문 속 [오늘의 운세]를 보고 있다.   

황반장
“매사에 노력하지만 쉽지 않은 하루가 될 것이다. 
동남쪽이 길하고 남서쪽이 흉하다...”

캐비닛을 여는 하윤주. 여행가방에서 잘 다려진 경찰제복을 꺼내면 
옆 캐비닛의 기린. 길게 고개를 내민다. 

기린
우린 그거 필요 없는데.
계급장 달 때. 국립묘지 갈 때. 입을 일 있겠어?

하윤주. 작게 끄덕이면 스윽~ 멋진 선배 포스로 캐비닛에 기대는 기린. 

기린
첫 출근 긴장되지?

순간. 쾅! 캐비닛을 닫고 있는 힘껏 누르는 황반장.

황반장
지랄한다. 동아리냐?  

문틈에 손이 낀 기린. 고통을 참으며 이를 악문다. 

기린
아.파.요. 

경찰뱃지. 신분증을 캐비닛에 넣고 문을 닫는 하윤주. 화면 암전.  

검은색 지휘 밴을 따라 주차장을 빠져나오는 차들. 
택시. 오토바이. 트럭 등 각양각색의 차들이 강변북로로 진입한다. 


30.	 도심거리. 낮
[oo역] 표지를 지나는 지휘 밴과 감시반 차량들. 사거리를 기점으로 흩어지는 모습.  

지휘 밴
운전석. 과묵한 인상의 나무늘보와 뒷좌석의 황반장. 하윤주.  

서울시 구역별 지도. 망원경. 광대역 무전송수신기 등이 설치된 지휘 밴의 뒷좌석.  

무전기를 드는 황반장. 한눈에 편해 보이는 의자에 반쯤 누운 자세.  

황반장
불편한 거 없지?
하윤주
...

하윤주. 구석 보조의자에 각을 잡고 앉아있다. 

황반장
여기는 송골매. 동물원 들리나? 


31.	 통제실. 낮
지도와 멀티모니터가 설치된 지하 공간. 헤드셋을 낀 다섯 남짓 남녀. 
후덕한 인상과 몸매. 목소리는 꾀꼬리인 통제녀. 

통제녀
동물원. 아주 잘 들립니다.
황반장(E)
애인 생겼어? 오늘 따라 톤이 좋아~!

통제녀. 수줍게 고개를 숙이면 마이크를 들고 벽시계를 보는 이실장. 날카로운 모습.    

이실장
잡담금지. 
지금부터 범죄정보관리법에 따라 모든 교신은 녹음 된다. 

신호를 받고 녹음기 버튼을 누르는 통제남. 

이실장
13시 00분 정각. 동물원 개장!   

지휘 밴
접이식 보드를 펼치는 황반장. 
작전구역이 프린트된 지도에 장기를 두듯 척!척! 동물자석을 붙인다. 

황반장
구관조 3번 출구. xx사거리 닭.

[oo역] 출입구 - 가판을 펼치는 구관조. 
횡단보도 - 가이드북을 든 관광객 닭. 
거리 - 비즈니스맨 기린. 
도로 - 퀵서비스 오토바이를 모는 두더지와 옆을 스치는 원숭이의 택시.  
인도 변 - 떡볶이트럭에 앉아 오뎅국물을 끊이는 독사. 

긴장과 설렘이 교차하는 하윤주. 거리의 감시반을 보다 고개를 돌리며  

하윤주
저는 언제 투입되는 겁니까?
황반장
때 되면.  

나침반을 꺼내는 황반장. 골똘한 표정. 

황반장
오늘은 남서쪽이 흉하다. 닭. 독사 특히 주의 할 것.  
"""
def __main__(text):
    # 대화를 파싱하고 비교
    movie_dialogues_text = text
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
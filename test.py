# -*- coding: utf-8 -*-
import streamlit as st
import random, base64
from pathlib import Path

# -----------------------------
# 페이지 & 기본 스타일
# -----------------------------
st.set_page_config(page_title="고전 시가 어휘 게임", page_icon="📘", layout="centered")

# 전통 분위기 배경/버튼
st.markdown("""
<style>
.stApp {
    background: url("https://i.ibb.co/Zm5rfyk/flower-bg.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
h1 {
    color: #3b2f2f;
    text-align: center;
    background-color: rgba(255, 248, 220, 0.7);
    padding: 10px;
    border-radius: 10px;
}
.block-container {
    background: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #c9a66b;
}
div.stButton > button {
    background-color: #f8f1e7;
    color: #3b2f2f;
    border: 2px solid #c9a66b;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 18px;
    font-weight: bold;
}
div.stButton > button:hover { background-color: #e6d3c3; color: #000; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 옛한글 폰트 임베드 (@font-face)
# -----------------------------
def inject_old_hangul_font():
    # 우선순위: 함초롬바탕 옛한글 → 함초롬돋움 옛한글 → 나눔바른고딕 옛한글
    candidates = [
        "fonts/HCRBatangLVT.ttf",
        "fonts/HCRDotumLVT.ttf",
        "fonts/NanumBarunGothicYetHangul.ttf",
    ]
    chosen = None
    for p in candidates:
        if Path(p).exists():
            chosen = p
            break

    if chosen:
        with open(chosen, "rb") as f:
            font_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        @font-face {{
            font-family: 'OldHangul';
            src: url(data:font/ttf;base64,{font_b64}) format('truetype');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }}
        /* 앱 전역에 강제 적용 */
        html, body, .stApp, .stApp * {{
            font-family: 'OldHangul', serif !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        return True, chosen
    else:
        st.warning("⚠️ 옛한글 폰트 파일을 찾지 못했습니다. 프로젝트의 fonts/ 폴더에 HCRBatangLVT.ttf(권장) 또는 HCRDotumLVT.ttf를 넣어주세요.")
        return False, None

_ = inject_old_hangul_font()

# -----------------------------
# 데이터셋: 고전시가 필수 어휘 100
# -----------------------------
words = {
    "": "가을",
    "나리(물)": "시내(물)",
    "소반": "밥상",
    "바": "바다",
    "졍지": "부엌",
    "님": "앞",
    "곰": "뒤",
    "즈": "모습",
    "즈믄": "천(1000)",
    "온": "백(100)",
    "별헤": "벼랑에",
    "곶": "꽃",
    "백구": "흰 갈매기",
    "이화": "배꽃 (흰색, 봄)",
    "도화": "복숭아꽃 (붉은색)",
    "행화": "살구꽃(분홍빛)",
    "해오라비": "해오라기, 하얀 백로",
    "뫼": "산 / 수라(궁중용어)",
    "하얌(향암)": "시골에 살아 세상 이치를 모르는 어리석은 사람",
    "소": "연못",
    "청약립": "갓",
    "녹사의": "우비(소박한 옷차림)",
    "믈": "물",
    "블": "불",
    "플": "풀",
    "시비": "사립문",
    "실솔": "귀뚜라미",
    "즌": "진 곳 (위험한 곳)",
    "사창": "여인의 방",
    "해동": "우리나라",
    "계림": "우리나라",
    "동이": "우리나라",
    "동방": "우리나라",
    "여름": "열매",
    "벽계수": "푸른 시냇물",
    "녀름": "여름",
    "": "강",
    "": "땅",
    "관산": "국경, 관문, 요새",
    "": "끝",
    "촉": "촛불",
    "녹양": "버드나무",
    "양류": "버드나무",
    "연하": "안개와 노을",
    "금수": "수놓은 비단",
    "혜음": "근심, 걱정, 시름",
    "남여": "가마",
    "황운": "누렇게 익은 곡식",
    "건곤": "하늘과 땅(온 세상)",
    "모쳠": "초가의 처마",
    "애": "날개",
    "이": "아양",
    "삼춘": "봄",
    "삼하": "여름",
    "삼추": "가을",
    "삼동": "겨울",
    "시앗": "첩",
    "침선": "바느질",
    "수품": "솜씨, 능력",
    "잣": "성(城)",
    "": "마을",
    "파람": "휘파람",
    "우음": "웃음",
    "홍진": "세속적 세계, 인간세계",
    "선다": "서운하다",
    "녀다": "가다, 지내다, 살아가다",
    "얼다": "(육체적) 사랑하다",
    "괴다": "(정신적) 사랑하다",
    "벼기다": "우기다, 모함하다",
    "방송하다": "내보내다, 석방하다",
    "늣기다": "흐느끼다",
    "이슷하다": "비슷하다",
    "혀다": "(악기, 불)을 켜다",
    "어엿브다": "불쌍하다",
    "싀어디여": "사라져서, 죽어 없어져",
    "삼기다": "생기다, 태어나다, 만들어지다",
    "우다": "꺼리다",
    "다": "마름질하다, 마련하다",
    "여희다": "이별하다, 헤어지다",
    "둏다": "좋다",
    "좋다": "깨끗하다",
    "헌사다": "야단스럽다",
    "어리다": "어리석다",
    "슬허하다": "슬퍼하다",
    "외다": "그르다, 잘못되다",
    "하다": "많다, 크다",
    "쟐다": "짧다",
    "수이": "쉽게",
    "긋다": "끊어지다",
    "닛다": "이어지다",
    "오뎐된": "방정맞은",
    "고두": "머리를 조아리다",
    "오마 다": "온다고 하다",
    "가시다": "변하다, 바뀌다",
    "로": "자주",
    "모쳐라": "마침",
    "고텨": "다시",
    "져근덧": "잠깐 사이에, 어느 덧, 문득",
    "슬장": "실컷",
    "마": "이미, 벌써",
    "빗기": "비스듬히",
    "유세차": "이해의 차례는",
    "~ㄹ셰라": "~할까 두렵다",
    "~손": "~에게",
    "~도곤": "~보다",
    "~우희": "~전에 / ~위에",
    "~다히": "~의, ~답게",
    "~": "~곳(장소)",
    "~제": "~때",
    "~니와": "물론이거니와",
    "~하": "~야",
    "~곰": "~좀",
    "~고져": "~하고자",
    "~다호라": "~같구나",
}

# -----------------------------
# 세션 상태
# -----------------------------
if "score" not in st.session_state: st.session_state.score = 0
if "q_num" not in st.session_state: st.session_state.q_num = 1
if "quiz_data" not in st.session_state: st.session_state.quiz_data = None
if "rank" not in st.session_state: st.session_state.rank = "노비"

# -----------------------------
# 계급 로직
# -----------------------------
def get_rank(score:int)->str:
    if score < 10:  return "노비"
    elif score < 20: return "상인"
    elif score < 40: return "중인"     # 양반 승급은 20문제 필요 → 20~39는 중인
    else:            return "양반"

def get_rank_message(prev:str, new:str):
    if prev == new: return None
    if new == "상인": return "🎉 축하합니다! 이제 상인이 되셨습니다."
    if new == "중인": return "🎉 축하합니다! 이제 중인 계급으로 오르셨습니다."
    if new == "양반": return "🎉 과거 시험에 급제하였씁니다! 이제 양반이 되셨습니다!"
    return None

# -----------------------------
# 문제 생성 (정답 제외하고 오답 추출 → 중복 방지)
# -----------------------------
def generate_question():
    answer, meaning = random.choice(list(words.items()))
    wrongs = random.sample([w for w in words.keys() if w != answer], 3)
    options = wrongs + [answer]
    random.shuffle(options)
    return answer, meaning, options

if st.session_state.quiz_data is None:
    st.session_state.quiz_data = generate_question()

answer, meaning, options = st.session_state.quiz_data

# -----------------------------
# 화면
# -----------------------------
st.title("📘 고전 시가 필수 어휘 학습 게임")
st.caption("옛한글 글자가 네모(□)로 보이면 상단의 폰트 경고를 확인하세요.")
st.subheader(f"Q{st.session_state.q_num}. 다음 뜻에 해당하는 단어는?")
st.info(meaning)

choice = st.radio("정답을 고르세요:", options, index=None)

if st.button("제출"):
    prev_rank = get_rank(st.session_state.score)
    if choice == answer:
        st.success("✅ 정답입니다!")
        st.session_state.score += 1
    else:
        st.error(f"❌ 오답입니다! 정답은 '{answer}' 였습니다.")
    st.session_state.q_num += 1
    st.session_state.quiz_data = generate_question()

    new_rank = get_rank(st.session_state.score)
    msg = get_rank_message(prev_rank, new_rank)
    if msg:
        st.balloons()
        st.success(msg)
    st.session_state.rank = new_rank

# -----------------------------
# 점수 & 계급 & 리셋
# -----------------------------
st.write(f"현재 점수: **{st.session_state.score}점**")
st.write(f"현재 계급: 🏅 **{st.session_state.rank}**")

if st.button("게임 다시 시작하기"):
    st.session_state.score = 0
    st.session_state.q_num = 1
    st.session_state.quiz_data = generate_question()
    st.session_state.rank = "노비"
    st.experimental_rerun()

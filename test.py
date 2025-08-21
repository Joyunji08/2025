# -*- coding: utf-8 -*-
import streamlit as st
import random

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="고전 어휘 외워보자!", page_icon="📖", layout="centered")

# -----------------------------
# CSS
# -----------------------------
page_bg = """
<style>
.stApp { background-color: #f0f6ff; font-family: 'Arial', sans-serif; }
h1 { color: #0052cc; text-align: center; font-size: 2.2em; font-weight: bold;
     padding: 12px; border-bottom: 3px solid #0052cc; margin-bottom: 20px; }
h2,h3 { color: #003366; }
.block-container { background: #ffffff; padding: 25px; border-radius: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
.score-card { background: #ffffff; padding: 15px; border-radius: 15px; box-shadow: 0px 3px 8px rgba(0,0,0,0.1); margin-bottom: 10px; }
div.stButton > button { background-color: #0052cc; color: white; border: none; border-radius: 6px;
                         padding: 10px 20px; font-size: 16px; font-weight: bold; }
div.stButton > button:hover { background-color: #003d99; color: #e6f0ff; }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------
# 문제 데이터
# -----------------------------
sentences = [
    {"sentence":"님은 가시고 나는 임을 뫼와야 하리라","word":"뫼다","hanja":"-","meaning":"모시다","options":["모시다","받들다","지키다","바라보다","버리다"]},
    {"sentence":"강호에 봄이 드니 꽃들이 만발하였도다","word":"강호","hanja":"江湖","meaning":"강과 호수","options":["강과 호수","은거지","산과 들","궁궐","마을"]},
    {"sentence":"일편단심 가실 줄이 이시랴","word":"단심","hanja":"丹心","meaning":"변치 않는 한마음","options":["변치 않는 한마음","나태한 마음","변덕스런 마음","분노한 마음"]},
    {"sentence":"절의를 굽히지 않고 나라를 지켰도다","word":"절의","hanja":"節義","meaning":"절개와 의리","options":["절개와 의리","욕심과 탐욕","게으름","겁 많음"]},
    {"sentence":"호연지기 기개 드높아","word":"기개","hanja":"氣槪","meaning":"씩씩하고 꿋꿋한 기상","options":["씩씩하고 꿋꿋한 기상","나약함","무기력함","겁 많음"]},
    {"sentence":"산천이 아름다우니 마음이 설렌다","word":"산천","hanja":"山川","meaning":"산과 내, 자연 경치","options":["산과 내, 자연 경치","바다와 강","도시","집"]},
    {"sentence":"단옷날이라 온 집안이 흥성이다","word":"단옷","hanja":"端午","meaning":"음력 5월 5일","options":["음력 5월 5일","음력 1월 1일","추석","설날"]},
    {"sentence":"고려의 충신은 충절을 지켰다","word":"충절","hanja":"忠節","meaning":"충성과 절개","options":["충성과 절개","배신","무관심","탐욕"]},
    {"sentence":"옥루에서 달빛을 바라보며 시를 읊었다","word":"옥루","hanja":"玉樓","meaning":"높은 누각","options":["높은 누각","궁궐","낮은 집","장터","연못"]},
    {"sentence":"봄바람에 꽃향기 가득하다","word":"풍류","hanja":"風流","meaning":"멋스러운 삶, 예술적 정취","options":["멋스러운 삶, 예술적 정취","혼잡한 삶","가난한 생활","싸움"]},
    # ... 나머지 데이터 동일한 형식으로 추가
]

# -----------------------------
# 세션 상태
# -----------------------------
if "score" not in st.session_state: st.session_state.score = 0
if "q_num" not in st.session_state: st.session_state.q_num = 1
if "quiz_data" not in st.session_state: st.session_state.quiz_data = None
if "rank" not in st.session_state: st.session_state.rank = "노비"
if "submitted" not in st.session_state: st.session_state.submitted = False

# -----------------------------
# 계급 로직
# -----------------------------
def get_rank(score:int)->str:
    if score < 10: return "노비"
    elif score < 20: return "상인"
    elif score < 40: return "중인"
    else: return "양반"

def get_rank_message(prev:str,new:str):
    if prev==new: return None
    if new=="상인": return "🎉 축하합니다! 이제 상인이 되셨습니다."
    if new=="중인": return "🎉 축하합니다! 이제 중인 계급으로 오르셨습니다."
    if new=="양반": return "🎉 과거 시험에 급제하였습니다! 이제 양반이 되셨습니다!"
    return None

# -----------------------------
# 문제 생성
# -----------------------------
def generate_question():
    q = random.choice(sentences)
    sentence = q["sentence"].replace(q["word"], f"**__{q['word']}__**")
    options = q["options"].copy()
    random.shuffle(options)
    return sentence, q["word"], q["meaning"], options

if st.session_state.quiz_data is None:
    st.session_state.quiz_data = generate_question()

sentence, target_word, correct_meaning, options = st.session_state.quiz_data

# -----------------------------
# 화면
# -----------------------------
st.title("📖 문해력 증진 학습 게임")
st.subheader(f"Q{st.session_state.q_num}. 밑줄 친 단어의 의미는 무엇일까요?")
st.markdown(f"<div class='block-container'>{sentence}</div>", unsafe_allow_html=True)

choice = st.radio("뜻을 고르세요:", options, index=0 if not st.session_state.submitted else None)

# 제출 버튼
if st.button("제출") and not st.session_state.submitted:
    st.session_state.submitted = True
    prev_rank = get_rank(st.session_state.score)
    if choice == correct_meaning:
        st.success("✅ 정답입니다!")
        st.session_state.score += 1
    else:
        st.error(f"❌ 오답입니다! '{target_word}'의 뜻은 '{correct_meaning}' 입니다.")
    st.session_state.q_num += 1
    new_rank = get_rank(st.session_state.score)
    msg = get_rank_message(prev_rank,new_rank)
    if msg:
        st.balloons()
        st.success(msg)
    st.session_state.rank = new_rank

# 다음 문제 버튼
if st.button("다음 문제") and st.session_state.submitted:
    st.session_state.quiz_data = generate_question()
    st.session_state.submitted = False
    st.experimental_rerun()

# 점수 & 계급 표시
st.markdown(f"<div class='score-card'>현재 점수: <b>{st.session_state.score}점</b></div>", unsafe_allow_html=True)
st.markdown(f"<div class='score-card'>현재 계급: 🏅 <b>{st.session_state.rank}</b></div>", unsafe_allow_html=True)

# 게임 초기화
if st.button("게임 다시 시작하기"):
    st.session_state.score = 0
    st.session_state.q_num = 1
    st.session_state.quiz_data = generate_question()
    st.session_state.rank = "노비"
    st.session_state.submitted = False
    st.experimental_rerun()

# -*- coding: utf-8 -*-
import streamlit as st
import random

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="고전 어휘 외워보자!", page_icon="📖", layout="centered")

# -----------------------------
# CSS (화이트·우드 톤 + 버튼 나란히)
# -----------------------------
page_bg = """
<style>
.stApp { 
    background-color: #fdfaf6; 
    font-family: 'Arial', sans-serif; 
}
h1 {
    color: #5c4033; 
    text-align: center; 
    font-size: 2.5em; 
    font-weight: bold;
    padding: 12px; 
    margin-bottom: 20px;
}
h2 {
    color: #7b5e57;
    text-align: center;
    font-size: 1.8em;
    margin-bottom: 40px;
}
.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 70vh;
    max-width: 600px;
    margin: 0 auto;
}
.block-container {
    background: #ffffff; 
    padding: 25px; 
    border-radius: 15px; 
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1); 
    margin-bottom: 20px; 
}
.score-card {
    background: #ffffff; 
    padding: 15px; 
    border-radius: 15px; 
    box-shadow: 0px 3px 8px rgba(0,0,0,0.1); 
    margin-bottom: 10px; 
}
div.stButton > button {
    background-color: #a67c52; 
    color: white; 
    border: none; 
    border-radius: 6px;
    padding: 12px 25px; 
    font-size: 18px; 
    font-weight: bold; 
    margin: 5px;
}
div.stButton > button:hover {
    background-color: #855e42; 
    color: #fdfaf6; 
}
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
]

MAX_QUESTIONS = 10

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "score" not in st.session_state: st.session_state.score = 0
if "q_num" not in st.session_state: st.session_state.q_num = 1
if "quiz_data" not in st.session_state: st.session_state.quiz_data = None
if "rank" not in st.session_state: st.session_state.rank = "노비"
if "submitted" not in st.session_state: st.session_state.submitted = False
if "game_started" not in st.session_state: st.session_state.game_started = False
if "used_questions" not in st.session_state: st.session_state.used_questions = []
if "choice" not in st.session_state: st.session_state.choice = None

# -----------------------------
# 계급 로직
# -----------------------------
def get_rank(score:int) -> str:
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
# 문제 생성 (중복 방지, 밑줄 표시)
# -----------------------------
def generate_question():
    remaining = [q for q in sentences if q not in st.session_state.used_questions]
    if not remaining:
        st.session_state.used_questions = []
        remaining = sentences.copy()
    q = random.choice(remaining)
    st.session_state.used_questions.append(q)
    sentence = q["sentence"].replace(q["word"], f"<u>{q['word']}</u>")
    options = q["options"].copy()
    random.shuffle(options)
    return sentence, q["word"], q["meaning"], options

if st.session_state.quiz_data is None:
    st.session_state.quiz_data = generate_question()

# -----------------------------
# 메인 화면
# -----------------------------
if not st.session_state.game_started:
    st.markdown("""
    <div class="main-container">
        <h1>🌿 고전 어휘 학습 게임 🌿</h1>
        <h2>고전 어휘를 외워보세요!</h2>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Leaf_icon.svg/1024px-Leaf_icon.svg.png" width="200">
    </div>
    """, unsafe_allow_html=True)

    if st.button("시작하겠습니까?", key="start_game"):
        st.session_state.game_started = True

# -----------------------------
# 게임 화면
# -----------------------------
if st.session_state.game_started:
    if st.session_state.q_num > MAX_QUESTIONS:
        st.success(f"🎉 게임 종료! 최종 점수: {st.session_state.score}, 계급: {st.session_state.rank}")
        if st.button("게임 다시 시작하기"):
            st.session_state.score = 0
            st.session_state.q_num = 1
            st.session_state.quiz_data = generate_question()
            st.session_state.rank = "노비"
            st.session_state.submitted = False
            st.session_state.game_started = False
            st.session_state.used_questions = []
            st.session_state.choice = None
        st.stop()

    sentence, target_word, correct_meaning, options = st.session_state.quiz_data
    st.subheader(f"Q{st.session_state.q_num}. 밑줄 친 단어의 의미는 무엇일까요?")
    st.markdown(f"<div class='block-container'>{sentence}</div>", unsafe_allow_html=True)
    st.session_state.choice = st.radio("뜻을 고르세요:", options, index=0 if not st.session_state.submitted else None)

    # -----------------------------
    # 버튼 form 안에 넣기 (한 번 클릭으로 제출 + 다음 문제 처리)
    # -----------------------------
    with st.form(key="quiz_form"):
        col1, col2 = st.columns(2)
        submit_clicked = col1.form_submit_button("제출")
        next_clicked = col2.form_submit_button("다음 문제")

        if submit_clicked and not st.session_state.submitted:
            st.session_state.submitted = True
            prev_rank = get_rank(st.session_state.score)
            if st.session_state.choice == correct_meaning:
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

        if next_clicked and st.session_state.submitted:
            st.session_state.quiz_data = generate_question()
            st.session_state.submitted = False
            st.session_state.choice = None

    # 점수 & 계급 표시
    st.markdown(f"<div class='score-card'>현재 점수: <b>{st.session_state.score}점</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-card'>현재 계급: 🏅 <b>{st.session_state.rank}</b></div>", unsafe_allow_html=True)

    # 게임 초기화 버튼
    if st.button("게임 다시 시작하기"):
        st.session_state.score = 0
        st.session_state.q_num = 1
        st.session_state.quiz_data = generate_question()
        st.session_state.rank = "노비"
        st.session_state.submitted = False
        st.session_state.game_started = False
        st.session_state.used_questions = []
        st.session_state.choice = None

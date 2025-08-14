import streamlit as st

st.set_page_config(page_title="MBTI 판타지 직업 추천기", page_icon="🪄")

st.title("✨ MBTI 판타지 직업 추천기 ✨")
st.write("당신의 MBTI를 선택하면, 어울리는 판타지 직업을 알려드립니다!")

# MBTI 목록
mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# MBTI → 직업 매핑
fantasy_jobs = {
    "INTJ": ("대마법학자", "고대의 지식을 연구하며 마법의 본질을 탐구합니다."),
    "INTP": ("연금술사", "신비한 조합과 실험으로 새로운 세계를 창조합니다."),
    "ENTJ": ("제국 장군", "전략과 리더십으로 왕국을 이끌어 나갑니다."),
    "ENTP": ("모험가", "새로운 땅을 개척하고 미지의 세계를 탐험합니다."),
    "INFJ": ("예언가", "미래를 내다보고 운명을 설계합니다."),
    "INFP": ("숲의 드루이드", "자연과 교감하며 치유와 보호의 힘을 씁니다."),
    "ENFJ": ("빛의 사제", "사람들을 하나로 묶고 희망을 전파합니다."),
    "ENFP": ("전설의 음유시인", "노래와 이야기로 세상을 변화시킵니다."),
    "ISTJ": ("왕국의 기사", "명예와 의무를 중시하며 왕국을 수호합니다."),
    "ISFJ": ("성역의 수호자", "평화를 지키기 위해 헌신합니다."),
    "ESTJ": ("왕실 집행관", "질서와 법을 수호하며 정의를 실현합니다."),
    "ESFJ": ("왕국의 대사", "외교와 협상을 통해 국가를 번영으로 이끕니다."),
    "ISTP": ("그림자 암살자", "은밀하게 목표를 제거하는 달인입니다."),
    "ISFP": ("방랑 화가", "세상의 아름다움을 그림으로 남깁니다."),
    "ESTP": ("검투사", "아레나에서 명성과 부를 쌓는 전사입니다."),
    "ESFP": ("무대 위의 마법사", "관중의 마음을 사로잡는 엔터테이너입니다."),
}

# 선택
user_mbti = st.selectbox("당신의 MBTI는?", mbti_list)

if st.button("추천 받기"):
    job_name, job_desc = fantasy_jobs[user_mbti]
    st.subheader(f"🏰 추천 직업: {job_name}")
    st.write(job_desc)


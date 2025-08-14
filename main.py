import streamlit as st
from datetime import datetime
import hashlib
import random

st.set_page_config(page_title="🌌 오늘의 운세: MBTI × 별자리 🌠", page_icon="🔮", layout="centered")

# ========= CSS: 네온 밤하늘 + 유성우 =========
st.markdown("""
<style>
/* 배경: 그라데이션 밤하늘 */
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(1200px 600px at 20% 10%, rgba(255,255,255,0.05), transparent 40%),
              linear-gradient(180deg, #0b0b1a 0%, #111133 50%, #1a1a3d 100%);
  color: #f7f7ff;
  font-family: "Pretendard", "Noto Sans KR", system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}

/* 네온 제목 */
h1, .title-neon {
  text-align: center;
  font-size: 2.4rem;
  color: #e6e6ff;
  text-shadow: 0 0 12px #7df9ff, 0 0 24px #c400ff, 0 0 40px #7df9ff;
  letter-spacing: 1px;
  margin-top: .2rem;
}

/* 설명 텍스트 네온 */
.subtitle-neon {
  text-align: center;
  color: #bfe9ff;
  text-shadow: 0 0 10px #00eaff70;
  margin-bottom: .6rem;
}

/* 카드 느낌 컨테이너 */
.block {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 0 20px rgba(0,238,255,0.12), inset 0 0 20px rgba(196,0,255,0.08);
  border-radius: 18px;
  padding: 18px 16px;
  backdrop-filter: blur(6px);
}

/* 버튼: 네온 */
.stButton>button {
  background: #0f0f22;
  border: 2px solid #7df9ff;
  color: #e9faff;
  font-weight: 700;
  border-radius: 12px;
  padding: .6rem 1rem;
  box-shadow: 0 0 18px #7df9ff70, 0 0 30px #c400ff40;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.stButton>button:hover {
  transform: translateY(-1px) scale(1.03);
  box-shadow: 0 0 26px #7df9ff, 0 0 40px #c400ff90;
  border-color: #c400ff;
}

/* 유성우: 키프레임 + 레이어 */
.shooting-stars {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; overflow: hidden; z-index: 0;
}
.star {
  position: absolute;
  width: 2px; height: 2px;
  background: white;
  box-shadow: 0 0 8px #fff, 0 0 20px #7df9ff, 0 0 28px #c400ff;
  border-radius: 50%;
  animation: fall linear infinite;
  opacity: .85;
}
@keyframes fall {
  0% { transform: translate3d(0,0,0) rotate(45deg); opacity: 0; }
  5% { opacity: .95; }
  100% { transform: translate3d(120vw, 120vh, 0) rotate(45deg); opacity: 0; }
}
/* 폼 요소 네온 테두리 */
[data-baseweb="select"] div, .stSelectbox div[data-baseweb="select"] {
  text-shadow: 0 0 10px #00eaff70;
}
</style>
<div class="shooting-stars">
  <!-- 다양한 지점에서 떨어지는 유성들 -->
  <div class="star" style="top:-5vh; left:10vw; animation-duration:3.2s; animation-delay:.2s;"></div>
  <div class="star" style="top:-10vh; left:35vw; animation-duration:3.6s; animation-delay:1.0s;"></div>
  <div class="star" style="top:-8vh; left:55vw; animation-duration:4.0s; animation-delay:.6s;"></div>
  <div class="star" style="top:-6vh; left:75vw; animation-duration:2.8s; animation-delay:1.4s;"></div>
  <div class="star" style="top:-12vh; left:85vw; animation-duration:3.4s; animation-delay:.9s;"></div>
  <div class="star" style="top:-7vh; left:20vw; animation-duration:3.8s; animation-delay:1.8s;"></div>
  <div class="star" style="top:-9vh; left:5vw; animation-duration:3.1s; animation-delay:2.2s;"></div>
</div>
""", unsafe_allow_html=True)

# ========= 헤더 =========
st.markdown('<div class="title-neon">🌙🌠 MBTI × 별자리 오늘의 운세 🔮✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-neon">밤하늘 아래 반짝이는 당신의 오늘 — 성격의 별과 별자리의 기운이 만나는 순간 🌌🪄</div>', unsafe_allow_html=True)
st.markdown("")

# ========= 입력 =========
mbtis = [
    "INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"
]
zodiacs = [
    "양자리(Aries) ♈","황소자리(Taurus) ♉","쌍둥이자리(Gemini) ♊","게자리(Cancer) ♋",
    "사자자리(Leo) ♌","처녀자리(Virgo) ♍","천칭자리(Libra) ♎","전갈자리(Scorpio) ♏",
    "사수자리(Sagittarius) ♐","염소자리(Capricorn) ♑","물병자리(Aquarius) ♒","물고기자리(Pisces) ♓"
]

col1, col2 = st.columns(2)
with col1:
    user_mbti = st.selectbox("🔮 MBTI 선택", mbtis, index=7)  # 기본 ENFP
with col2:
    user_zodiac = st.selectbox("🌟 별자리 선택", zodiacs, index=10)  # 기본 물병

st.markdown("")

# ========= 운세 생성 로직 (날짜+입력 기반 결정론) =========
def seed_from_today_and_inputs(mbti: str, zodiac: str) -> int:
    today = datetime.now().strftime("%Y-%m-%d")  # 시스템 날짜 기준
    key = f"{today}-{mbti}-{zodiac}"
    h = hashlib.sha256(key.encode()).hexdigest()
    return int(h[:12], 16)  # 충분한 분산

def d_choice(seed, options):
    rnd = random.Random(seed)
    return rnd.choice(options)

def d_score(seed, a=50, b=100):
    rnd = random.Random(seed ^ 0xABCDEF)
    return rnd.randint(a, b)  # 50~100

themes = [
    "🌙 달빛의 가호", "🌠 유성의 축복", "🪄 마력의 소용돌이", "🔭 별자리 정렬",
    "🪽 수호정령의 인도", "🔥 태양 파편", "💧 달의 샘물", "🌫 운명의 안개"
]

tips = [
    "작은 친절 한 번이 큰 행운으로 돌아와요 🤝",
    "첫 느낌을 믿어보세요 — 직관이 정답일 확률 ↑ 🧭",
    "정리부터! 책상 정돈이 생각 정돈으로 연결 🌬️",
    "과감한 메시지 한 통이 판도를 바꿉니다 📱",
    "컨디션 관리는 물 한 잔부터 시작해요 💧",
    "할까 말까? 한다면 오늘! 🚀",
    "기록하면 실수도 줄고 기회는 늘어요 📝",
    "하늘 한 번 보고 심호흡 🌌"
]

lucky_items = [
    "은색 이어폰 🎧", "보라색 형광펜 🖍️", "별 모양 스티커 ⭐",
    "라벤더 핸드크림 🌿", "블루 캔디 🍬", "달 모양 목걸이 🌙",
    "네온 키링 🔑", "반짝이 파우치 ✨"
]

lucky_colors = ["네온 퍼플 💜", "코스믹 블루 💙", "미드나이트 네이비 🌌", "아쿠아 민트 🫧", "일렉트릭 핑크 💖", "라일락 글로우 🪻"]

love_msgs = [
    "따뜻한 메시지로 관계가 한 걸음 가까워져요 💌",
    "솔직함이 최고의 매력 — 단, 톤은 부드럽게 🌷",
    "우연처럼 보인 만남에 별이 깃듭니다 ✨",
    "관심 표현은 디테일에서! 소소한 배려가 포인트 🎀",
    "타이밍이 신—묘—해! 기다리면 신호가 와요 ⏳",
]
study_work_msgs = [
    "기초를 탄탄하게! 작은 복습이 큰 점프를 만듭니다 📚",
    "아이디어 스파크⚡ 메모장 열어두세요!",
    "집중력 버프 ON — 짧고 빡센 스프린트 추천 ⏱️",
    "협업에서 리더십이 반짝! 역할 분담을 제안해보세요 🧩",
    "실수도 데이터! 원인 기록이 다음 성공을 부릅니다 📈",
]
money_luck_msgs = [
    "사소한 지출을 아끼면 기분 좋은 발견이 옵니다 💰",
    "중고/리셀 탐색에 행운 포인트 ✨",
    "급구매는 NO, 위시리스트 24시간 룰! 🛒",
    "작은 경품/이벤트에 의외의 행운 🍀",
    "현금 대신 포인트/쿠폰이 효율 만점 🎟️",
]

def stars_bar(score: int) -> str:
    # 5단계 이모지 바
    filled = min(5, max(1, (score - 1) // 10))  # 50~100 -> 5칸
    return "⭐" * filled + "✩" * (5 - filled)

# ========= 버튼 =========
if st.button("🌠 오늘의 운세 보기! 🌠"):
    seed = seed_from_today_and_inputs(user_mbti, user_zodiac)
    theme = d_choice(seed, themes)
    tip = d_choice(seed + 1, tips)
    item = d_choice(seed + 2, lucky_items)
    color = d_choice(seed + 3, lucky_colors)
    love = d_choice(seed + 4, love_msgs)
    work = d_choice(seed + 5, study_work_msgs)
    money = d_choice(seed + 6, money_luck_msgs)

    s_love = d_score(seed + 7)     # 50~100
    s_work = d_score(seed + 8)
    s_money = d_score(seed + 9)
    s_total = round((s_love + s_work + s_money) / 3)

    # 헤더 카드
    st.markdown(f"""
    <div class="block" style="text-align:center; margin-top:.2rem;">
      <div style="font-size:1.2rem;">{user_mbti} × {user_zodiac}</div>
      <div style="font-size:1.7rem; margin-top:.2rem;">{theme} — 오늘의 총운 {s_total}점 🌟</div>
      <div style="margin-top:.3rem; font-size:1.1rem;">{stars_bar(s_total)}</div>
    </div>
    """, unsafe_allow_html=True)

    # 상세 섹션
    st.markdown("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="block">
        <div style="font-size:1.2rem;">💖 사랑/관계運</div>
        <div style="font-size:1.1rem; margin:.2rem 0;">{stars_bar(s_love)} ({s_love})</div>
        <div style="opacity:.95;">{love}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="block">
        <div style="font-size:1.2rem;">📚 공부·일運</div>
        <div style="font-size:1.1rem; margin:.2rem 0;">{stars_bar(s_work)} ({s_work})</div>
        <div style="opacity:.95;">{work}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="block">
        <div style="font-size:1.2rem;">💰 금전·기회運</div>
        <div style="font-size:1.1rem; margin:.2rem 0;">{stars_bar(s_money)} ({s_money})</div>
        <div style="opacity:.95;">{money}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown(f"""<div class="block" style="text-align:center;">
      <div style="font-size:1.05rem;">🎁 행운 아이템: <b>{item}</b></div>
      <div style="font-size:1.05rem; margin-top:.2rem;">🎨 포춘 컬러: <b>{color}</b></div>
      <div style="font-size:1.05rem; margin-top:.4rem;">💡 오늘의 한 줄 팁: <i>{tip}</i></div>
    </div>""", unsafe_allow_html=True)

else:
    st.markdown(
        '<div class="block" style="text-align:center;">'
        '🌌 상단에서 <b>MBTI</b>와 <b>별자리</b>를 고르고 버튼을 눌러 오늘의 운세를 확인하세요! '
        '별똥별이 지나갈 때 소원을 빌면… 비밀 버프가 걸릴지도? ✨🧙‍♀️'
        '</div>', unsafe_allow_html=True
    )

# ========= 푸터 =========
st.markdown("<div style='text-align:center; opacity:.8; margin-top:1rem;'>"
            "⚡ Just for fun • 운세는 가볍게 즐겨요! 🌠</div>", unsafe_allow_html=True)

import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="😊 감정 분석", 
    page_icon="🎭", 
    layout="wide"
)

# 세션 상태 초기화 (처음 실행시에만)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'  # 시작 페이지

# 감정 리스트 정의
EMOTIONS = {
    'happy': {'emoji': '😊', 'name': '행복', 'color': '#FFD700'},
    'sad': {'emoji': '😢', 'name': '슬픔', 'color': '#4682B4'},
    'angry': {'emoji': '😠', 'name': '화남', 'color': '#DC143C'},
    'surprise': {'emoji': '😮', 'name': '놀람', 'color': '#FF8C00'},
    'fear': {'emoji': '😰', 'name': '불안', 'color': '#800080'},
    'neutral': {'emoji': '😐', 'name': '중립', 'color': '#808080'}
}

# === 페이지 함수들 ===

def show_main_page():
    """메인 선택 페이지"""
    st.title("😊 감정 분석 프로젝트")
    st.markdown("---")
    
    # 설명
    st.markdown("""
    ### 🎭 어떤 방법으로 감정을 분석하고 싶으세요?
    
    두 가지 방법 중 하나를 선택해주세요:
    """)
    
    # 선택 버튼들을 두 개의 컬럼으로 배치
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📹 실시간 웹캠 분석")
        st.write("웹캠을 통해 실시간으로 감정을 분석합니다")
        if st.button("🎥 웹캠으로 분석하기", use_container_width=True):
            st.session_state.current_page = 'webcam'
            st.rerun()  # 페이지 새로고침
    
    with col2:
        st.markdown("#### ✋ 수동으로 감정 선택")
        st.write("직접 감정을 선택해서 결과를 확인합니다")
        if st.button("🎯 직접 선택하기", use_container_width=True):
            st.session_state.current_page = 'manual'
            st.rerun()

    
def show_manual_page():
    """수동 선택 페이지"""
    st.title("✋ 감정을 직접 선택해주세요")
    st.markdown("---")
    
    # 뒤로가기 버튼
    if st.button("🔙 메인으로 돌아가기"):
        st.session_state.current_page = 'main'
        st.rerun()
    
    st.markdown("### 🎭 어떤 감정을 선택하시겠어요?")
    
    # 감정 선택 버튼들을 3x2 그리드로 배치
    cols = st.columns(3)
    
    for i, (emotion_key, emotion_data) in enumerate(EMOTIONS.items()):
        col = cols[i % 3]
        with col:
            # 각 감정별 스타일링된 버튼
            if st.button(
                f"{emotion_data['emoji']} {emotion_data['name']}", 
                use_container_width=True,
                key=f"emotion_{emotion_key}"
            ):
                st.session_state.current_page = 'result'
                st.session_state.selected_emotion = emotion_key
                st.rerun()


def show_webcam_page():
    """웹캠 페이지 (아직 기본 구조만)"""
    st.title("📹 웹캠 감정 분석")
    st.markdown("---")
    
    # 뒤로가기 버튼
    if st.button("🔙 메인으로 돌아가기"):
        st.session_state.current_page = 'main'
        st.rerun()
    
    st.info("🚧 웹캠 기능은 다음 단계에서 구현할 예정입니다!")
    
    # 임시로 테스트용 버튼들
    st.markdown("### 테스트용 감정 결과")
    cols = st.columns(3)
    
    test_emotions = ['happy', 'sad', 'angry']
    for i, emotion in enumerate(test_emotions):
        with cols[i]:
            if st.button(f"테스트: {EMOTIONS[emotion]['name']}", key=f"test_{emotion}"):
                st.session_state.current_page = 'result'
                st.session_state.selected_emotion = emotion
                st.rerun()


def show_result_page():
    """감정 결과 페이지"""
    emotion_key = st.session_state.get('selected_emotion', 'neutral')
    emotion = EMOTIONS[emotion_key]
    
    st.title(f"{emotion['emoji']} {emotion['name']} 감정 결과")
    st.markdown("---")
    
    # 결과 표시
    st.markdown(f"""
    ### 🎯 분석 결과: **{emotion['name']}**
    
    {emotion['emoji']} 당신의 현재 감정은 **{emotion['name']}** 상태로 분석되었습니다!
    """)
    
    # 감정별 맞춤 메시지
    emotion_messages = {
    'angry': {
        'emoji': '😠',
        'korean': '화남',
        'color': '#FF6B6B',
        'description': '분노는 자연스러운 감정입니다. 건설적으로 해소해보세요.',
        'solutions': [
            '🧘‍♀️ 심호흡을 10회 반복하세요',
            '🚶‍♀️ 10-15분간 산책하며 마음을 진정시키세요',
            '🎵 좋아하는 음악을 들으며 휴식하세요',
            '📝 감정을 일기에 써보세요',
            '💪 운동으로 에너지를 발산하세요'
        ],
        'quotes': [
            '"분노는 바보들의 가슴속에서만 살아간다." - 아인슈타인',
            '"화가 날 때는 100까지 세어라. 매우 화가 날 때는 욕설을 퍼부어라." - 마크 트웨인'
        ],
        'tips': '화날 때는 즉각적인 반응보다는 잠시 멈추고 생각하는 시간을 가져보세요.'
    },
    'sad': {
        'emoji': '😢',
        'korean': '슬픔',
        'color': '#4ECDC4',
        'description': '슬픔을 느끼는 것은 정상적인 감정 반응입니다.',
        'solutions': [
            '☕ 따뜻한 차를 마시며 휴식하세요',
            '👥 신뢰할 수 있는 사람과 대화하세요',
            '📖 좋은 책을 읽거나 영화를 보세요',
            '🌅 자연 속에서 시간을 보내세요',
            '🙏 감사할 일들을 적어보세요'
        ],
        'quotes': [
            '"눈물은 마음이 말할 수 없는 것을 말해준다." - 익명',
            '"슬픔도 기쁨과 마찬가지로 삶의 일부다." - 칼릴 지브란'
        ],
        'tips': '슬픔을 억누르지 말고 받아들이되, 도움이 필요할 때는 주변에 요청하세요.'
    },
    'happy': {
        'emoji': '😊',
        'korean': '기쁨',
        'color': '#45B7D1',
        'description': '긍정적인 에너지를 유지하고 다른 사람들과 나누세요!',
        'solutions': [
            '🎉 이 기쁨을 친구들과 나누세요',
            '📸 좋은 순간을 사진으로 남기세요',
            '🎯 새로운 목표를 세워보세요',
            '🎨 창의적인 활동을 해보세요',
            '💝 다른 사람을 도와주세요'
        ],
        'quotes': [
            '"행복은 습관이다. 그것을 몸에 지녀라." - 허버드',
            '"행복한 사람은 희망을 잃지 않는다." - 아리스토텔레스'
        ],
        'tips': '긍정적인 마음가짐을 유지하고, 작은 것에도 감사하는 마음을 가져보세요.'
    },
    'fear': {
        'emoji': '😨',
        'korean': '두려움',
        'color': '#96CEB4',
        'description': '두려움은 우리를 보호하는 자연스러운 감정입니다.',
        'solutions': [
            '🧘 명상으로 마음을 진정시키세요',
            '📝 두려움의 원인을 구체적으로 적어보세요',
            '👨‍👩‍👧‍👦 신뢰할 수 있는 사람과 이야기하세요',
            '📚 관련 정보를 찾아 준비하세요',
            '👶 작은 단계부터 시작해보세요'
        ],
        'quotes': [
            '"용기란 두려움이 없는 것이 아니라 두려움을 극복하는 것이다." - 넬슨 만델라',
            '"두려움은 항상 무지에서 생긴다." - 에머슨'
        ],
        'tips': '두려움을 구체적으로 분석하고, 작은 행동부터 시작해보세요.'
    },
    'surprise': {
        'emoji': '😲',
        'korean': '놀람',
        'color': '#FFEAA7',
        'description': '놀라운 순간을 긍정적으로 받아들여보세요.',
        'solutions': [
            '🤔 상황을 차분히 정리해보세요',
            '🔍 새로운 관점으로 바라보세요',
            '📱 필요하다면 정보를 더 수집하세요',
            '🎢 변화를 즐겨보세요',
            '💡 새로운 기회로 생각해보세요'
        ],
        'quotes': [
            '"인생은 놀라움의 연속이다." - 익명',
            '"예상치 못한 일들이 인생을 흥미롭게 만든다." - 익명'
        ],
        'tips': '예상치 못한 상황도 새로운 배움의 기회로 받아들여보세요.'
    },
    'disgust': {
        'emoji': '🤢',
        'korean': '혐오',
        'color': '#DDA0DD',
        'description': '불쾌감을 느끼는 것은 정상적인 반응입니다.',
        'solutions': [
            '🌿 깨끗하고 쾌적한 환경으로 이동하세요',
            '🕯️ 좋아하는 향기로 기분전환하세요',
            '🧼 손을 씻고 몸을 깔끔하게 하세요',
            '🍃 신선한 공기를 마시세요',
            '🎵 좋아하는 음악으로 기분을 바꿔보세요'
        ],
        'quotes': [
            '"깨끗함은 마음의 평화를 가져다준다." - 익명',
            '"환경이 마음에 미치는 영향은 생각보다 크다." - 익명'
        ],
        'tips': '불쾌한 환경에서 벗어나 마음에 드는 공간으로 이동해보세요.'
    },
    'neutral': {
        'emoji': '😐',
        'korean': '평온',
        'color': '#A8A8A8',
        'description': '평온한 마음 상태를 유지하고 있습니다.',
        'solutions': [
            '📚 새로운 것을 배워보세요',
            '🎯 목표를 설정해보세요',
            '🏃‍♀️ 가벼운 운동을 해보세요',
            '🧘‍♀️ 명상이나 요가를 해보세요',
            '🎨 창의적인 활동을 시작해보세요'
        ],
        'quotes': [
            '"고요한 마음에서 지혜가 나온다." - 붓다',
            '"평온함 속에서 진정한 힘을 찾을 수 있다." - 익명'
        ],
        'tips': '안정된 상태를 바탕으로 새로운 도전이나 목표를 세워보세요.'
    }
}

    
    st.success(emotion_messages.get(emotion_key, "감정 분석이 완료되었습니다!"))
    
    # 액션 버튼들
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 다시 분석하기", use_container_width=True):
            st.session_state.current_page = 'main'
            # 이전 결과 초기화
            if 'selected_emotion' in st.session_state:
                del st.session_state.selected_emotion
            st.rerun()
    
    with col2:
        if st.button("📊 다른 감정 보기", use_container_width=True):
            st.session_state.current_page = 'manual'
            st.rerun()


# === 메인 라우터 ===

def main():
    """메인 라우터 - 현재 페이지에 따라 적절한 함수 호출"""
    
    # 사이드바에 현재 상태 표시 (디버깅용)
    with st.sidebar:
        st.header("🔧 상태 정보")
        st.write(f"현재 페이지: `{st.session_state.current_page}`")
        if 'selected_emotion' in st.session_state:
            emotion = EMOTIONS[st.session_state.selected_emotion]
            st.write(f"선택된 감정: {emotion['emoji']} {emotion['name']}")
    
    # 현재 페이지에 따라 적절한 함수 호출
    if st.session_state.current_page == 'main':
        show_main_page()
    elif st.session_state.current_page == 'manual':
        show_manual_page()
    elif st.session_state.current_page == 'webcam':
        show_webcam_page()
    elif st.session_state.current_page == 'result':
        show_result_page()
    else:
        # 예상치 못한 페이지면 메인으로
        st.session_state.current_page = 'main'
        st.rerun()
    
    # 푸터
    st.markdown("---")
    st.caption("Made with Streamlit 🚀")


# 앱 실행
if __name__ == "__main__":
    main()
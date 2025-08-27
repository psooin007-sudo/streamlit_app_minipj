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
        'happy': "😊 정말 좋은 기분이시네요! 이 기분을 계속 유지하세요!",
        'sad': "😢 조금 우울한 기분이시군요. 괜찮아질 거예요.",
        'angry': "😠 화가 나셨나요? 깊게 숨을 쉬고 진정해보세요.",
        'surprise': "😮 뭔가 놀라운 일이 있었나봐요!",
        'fear': "😰 불안하시군요. 모든 것이 잘 될 거예요.",
        'neutral': "😐 평온한 상태시네요. 차분함을 유지하세요."
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
# streamlit_app.py (배포용 수정버전)
import streamlit as st
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="감정 분석 결과",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 감정별 데이터 (기존과 동일)
EMOTION_DATA = {
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

def safe_get_query_param(param_name, default_value):
    """안전한 쿼리 파라미터 추출"""
    try:
        if hasattr(st, 'query_params'):
            params = st.query_params
            if param_name in params:
                value = params[param_name]
                if isinstance(value, list):
                    return value[0] if value else default_value
                return value
        return default_value
    except Exception as e:
        st.sidebar.error(f"쿼리 파라미터 읽기 오류: {e}")
        return default_value

def create_emotion_gauge(score, color):
    """감정 신뢰도 게이지 차트"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "신뢰도 (%)"},
        delta={'reference': 80},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75, 
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def show_homepage():
    """홈페이지 (쿼리 파라미터가 없을 때)"""
    st.title("🎭 감정 분석 시스템")
    st.markdown("---")
    
    st.markdown("""
    ## 웹캠 감정 분석 사용법
    
    ### 📥 1단계: 로컬 프로그램 다운로드
    
    **방법 1: 직접 다운로드**
    """)
    
    # 코드 다운로드 링크 제공
    with st.expander("💻 웹캠 분석 프로그램 코드"):
        st.code('''
# 이 코드를 webcam_analyzer.py로 저장하세요
# 필요한 라이브러리: pip install opencv-python transformers pillow torch

# (여기에 위의 webcam_to_deployed_app.py 코드 내용을 표시)
        ''', language='python')
    
    st.markdown("""
    **방법 2: GitHub에서 클론**
    ```bash
    git clone [your-repo-url]
    cd [repo-name]
    pip install -r requirements.txt
    python webcam_analyzer.py
    ```
    
    ### 🚀 2단계: 프로그램 실행
    1. `webcam_analyzer.py` 파일을 실행하세요
    2. OpenCV 창이 열리면 얼굴을 카메라에 맞춰주세요
    3. 얼굴을 클릭하거나 'C' 키를 눌러 감정을 캡처하세요
    4. 2초 후 자동으로 이 페이지에서 결과가 표시됩니다!
    
    ### 📋 시스템 요구사항
    - Python 3.7+
    - 웹캠이 연결된 컴퓨터
    - 인터넷 연결 (결과 표시용)
    
    ### 🔧 문제 해결
    - 웹캠이 인식되지 않으면 다른 프로그램에서 카메라를 사용 중인지 확인하세요
    - 모델 로딩이 느리면 처음 실행시에만 발생하는 정상적인 현상입니다
    """)
    
    # 테스트용 감정 선택
    st.markdown("---")
    st.markdown("## 🧪 테스트용 감정 체험")
    st.write("웹캠 없이도 각 감정별 결과를 미리 체험해볼 수 있습니다:")
    
    cols = st.columns(3)
    emotions_to_show = ['happy', 'sad', 'angry', 'fear', 'surprise', 'neutral']
    
    for i, emotion in enumerate(emotions_to_show):
        col = cols[i % 3]
        with col:
            emotion_data = EMOTION_DATA[emotion]
            if st.button(f"{emotion_data['emoji']} {emotion_data['korean']}", 
                        key=f"test_{emotion}", use_container_width=True):
                st.query_params.emotion = emotion
                st.query_params.score = "0.85"
                st.rerun()

def show_result_page(emotion, score):
    """결과 페이지 표시"""
    # 세션 상태 초기화
    if 'emotion_history' not in st.session_state:
        st.session_state.emotion_history = []
    
    # 감정 히스토리 업데이트
    current_time = datetime.now()
    should_add = True
    
    if st.session_state.emotion_history:
        last_entry = st.session_state.emotion_history[-1]
        if (last_entry['emotion'] == emotion and 
            (current_time - last_entry['timestamp']).seconds < 10):
            should_add = False
    
    if should_add:
        st.session_state.emotion_history.append({
            'emotion': emotion,
            'score': score,
            'timestamp': current_time
        })
        
        if len(st.session_state.emotion_history) > 50:
            st.session_state.emotion_history = st.session_state.emotion_history[-50:]
    
    emotion_data = EMOTION_DATA[emotion]
    
    # 메인 헤더
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="color: {emotion_data['color']}; font-size: 4rem; margin: 0;">
                {emotion_data['emoji']}
            </h1>
            <h2 style="color: {emotion_data['color']}; margin: 0.5rem 0;">
                {emotion_data['korean']} ({emotion.upper()})
            </h2>
            <p style="font-size: 1.2rem; color: #666; margin: 0;">
                {emotion_data['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 신뢰도 게이지와 솔루션
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 분석 결과")
        gauge_fig = create_emotion_gauge(score, emotion_data['color'])
        st.plotly_chart(gauge_fig, use_container_width=True)
        st.info(f"🕐 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        st.subheader("💡 추천 솔루션")
        for solution in emotion_data['solutions']:
            st.markdown(f"• {solution}")
        
        st.subheader("🎯 도움이 되는 팁")
        st.markdown(f"💭 {emotion_data['tips']}")
    
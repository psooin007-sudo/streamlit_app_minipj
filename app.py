# streamlit_app.py (수정된 버전)
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

# 감정별 데이터
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
        # Streamlit 버전에 따른 호환성 처리
        if hasattr(st, 'query_params'):
            # 새로운 방식 (Streamlit 1.18+)
            if param_name in st.query_params:
                return st.query_params[param_name]
        elif hasattr(st, 'experimental_get_query_params'):
            # 구버전 방식
            params = st.experimental_get_query_params()
            if param_name in params:
                return params[param_name][0]
        return default_value
    except Exception as e:
        st.error(f"쿼리 파라미터 읽기 오류: {e}")
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
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_history_chart():
    """감정 히스토리 차트"""
    if 'emotion_history' not in st.session_state or not st.session_state.emotion_history:
        return None
    
    history = st.session_state.emotion_history[-20:]  # 최근 20개만
    
    df = pd.DataFrame([
        {
            'time': entry['timestamp'].strftime('%H:%M:%S'),
            'emotion': EMOTION_DATA[entry['emotion']]['korean'],
            'score': entry['score'] * 100,
            'color': EMOTION_DATA[entry['emotion']]['color']
        }
        for entry in history
    ])
    
    fig = px.line(df, x='time', y='score', 
                  title='감정 변화 추이', 
                  markers=True)
    fig.update_layout(
        height=300,
        xaxis_title="시간",
        yaxis_title="신뢰도 (%)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def show_homepage():
    """홈페이지 (쿼리 파라미터가 없을 때)"""
    st.title("🎭 감정 분석 시스템")
    st.markdown("---")
    
    # 인트로
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 2rem;">
            <h2>🎯 실시간 감정 분석</h2>
            <p>AI가 당신의 감정을 분석하고 맞춤형 솔루션을 제공합니다</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 테스트용 감정 체험
    st.subheader("🧪 감정별 결과 미리보기")
    st.write("각 감정별로 어떤 결과가 나오는지 체험해보세요:")
    
    # 감정 버튼들
    cols = st.columns(3)
    emotions_to_show = ['happy', 'sad', 'angry', 'fear', 'surprise', 'neutral']
    
    for i, emotion in enumerate(emotions_to_show):
        col = cols[i % 3]
        with col:
            emotion_data = EMOTION_DATA[emotion]
            button_style = f"""
                <style>
                .stButton > button[key="test_{emotion}"] {{
                    background-color: {emotion_data['color']};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 1.2rem;
                    padding: 1rem;
                    width: 100%;
                }}
                </style>
            """
            st.markdown(button_style, unsafe_allow_html=True)
            
            if st.button(f"{emotion_data['emoji']} {emotion_data['korean']}", 
                        key=f"test_{emotion}", use_container_width=True):
                # URL 파라미터 설정 방법 수정
                st.query_params.emotion = emotion
                st.query_params.score = "0.85"
                st.rerun()
    
    # 사용법 안내
    with st.expander("💡 웹캠 분석 프로그램 사용법", expanded=False):
        st.markdown("""
        ### 📥 1단계: 프로그램 다운로드 및 설정
        
        1. 필요한 라이브러리 설치:
        ```bash
        pip install opencv-python transformers pillow torch streamlit plotly
        ```
        
        2. 웹캠 분석 프로그램을 별도로 실행하세요
        
        ### 🚀 2단계: 실행 방법
        1. 웹캠 프로그램 실행
        2. 얼굴을 카메라에 맞춤
        3. 클릭하거나 'C' 키로 감정 캡처
        4. 이 페이지에서 자동으로 결과 확인
        
        ### 🔧 시스템 요구사항
        - Python 3.7+
        - 웹캠 연결
        - 인터넷 연결
        """)

def show_result_page(emotion, score):
    """결과 페이지 표시"""
    # 세션 상태 초기화
    if 'emotion_history' not in st.session_state:
        st.session_state.emotion_history = []
    
    # 감정 히스토리 업데이트
    current_time = datetime.now()
    should_add = True
    
    # 중복 방지 (10초 내 같은 감정은 추가하지 않음)
    if st.session_state.emotion_history:
        last_entry = st.session_state.emotion_history[-1]
        time_diff = (current_time - last_entry['timestamp']).total_seconds()
        if last_entry['emotion'] == emotion and time_diff < 10:
            should_add = False
    
    if should_add:
        st.session_state.emotion_history.append({
            'emotion': emotion,
            'score': score,
            'timestamp': current_time
        })
        
        # 히스토리 길이 제한
        if len(st.session_state.emotion_history) > 50:
            st.session_state.emotion_history = st.session_state.emotion_history[-50:]
    
    emotion_data = EMOTION_DATA[emotion]
    
    # 메인 헤더
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, {emotion_data['color']}20 0%, {emotion_data['color']}40 100%); border-radius: 15px; margin-bottom: 2rem;">
            <div style="font-size: 5rem; margin: 0;">{emotion_data['emoji']}</div>
            <h2 style="color: {emotion_data['color']}; margin: 1rem 0; font-size: 2.5rem;">
                {emotion_data['korean']}
            </h2>
            <h3 style="color: {emotion_data['color']}; margin: 0.5rem 0; font-size: 1.5rem; text-transform: uppercase;">
                {emotion}
            </h3>
            <p style="font-size: 1.3rem; color: #666; margin: 1rem 0; line-height: 1.6;">
                {emotion_data['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 메인 콘텐츠
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 분석 결과")
        gauge_fig = create_emotion_gauge(score, emotion_data['color'])
        st.plotly_chart(gauge_fig, use_container_width=True)
        
        # 분석 정보
        st.info(f"🕐 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.success(f"✨ 신뢰도: {score*100:.1f}%")
    
    with col2:
        st.subheader("💡 추천 솔루션")
        for i, solution in enumerate(emotion_data['solutions'], 1):
            st.markdown(f"**{i}.** {solution}")
        
        st.subheader("🎯 도움이 되는 팁")
        st.markdown(f"""
        <div style="background: {emotion_data['color']}20; padding: 1rem; border-radius: 10px; border-left: 5px solid {emotion_data['color']};">
            💭 {emotion_data['tips']}
        </div>
        """, unsafe_allow_html=True)
    
    # 명언 섹션
    st.markdown("---")
    st.subheader("📜 관련 명언")
    quote_cols = st.columns(len(emotion_data['quotes']))
    for i, quote in enumerate(emotion_data['quotes']):
        with quote_cols[i]:
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; text-align: center; height: 100px; display: flex; align-items: center; justify-content: center;">
                <em style="color: #666; font-size: 0.9rem; line-height: 1.4;">{quote}</em>
            </div>
            """, unsafe_allow_html=True)
    
    # 히스토리 차트
    if len(st.session_state.emotion_history) > 1:
        st.markdown("---")
        st.subheader("📈 감정 변화 추이")
        history_chart = create_history_chart()
        if history_chart:
            st.plotly_chart(history_chart, use_container_width=True)
    
    # 새로운 분석 버튼
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 홈으로 돌아가기", use_container_width=True, type="primary"):
            # URL 파라미터 클리어
            st.query_params.clear()
            st.rerun()

def main():
    """메인 함수"""
    try:
        # 쿼리 파라미터 읽기
        emotion = safe_get_query_param('emotion', None)
        score_str = safe_get_query_param('score', '0.0')
        
        # 점수 변환
        try:
            score = float(score_str)
        except (ValueError, TypeError):
            score = 0.0
        
        # 페이지 라우팅
        if emotion and emotion in EMOTION_DATA:
            show_result_page(emotion, score)
        else:
            show_homepage()
            
    except Exception as e:
        st.error(f"애플리케이션 오류가 발생했습니다: {str(e)}")
        st.markdown("---")
        st.subheader("🔧 문제 해결")
        st.write("페이지를 새로고침하거나 다시 시도해주세요.")
        
        if st.button("🏠 홈으로 가기"):
            st.query_params.clear()
            st.rerun()

if __name__ == "__main__":
    main()
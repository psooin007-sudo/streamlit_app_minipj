# streamlit_app_enhanced.py (수정된 버전)
import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
import base64
import gzip
import json
from datetime import datetime
import time

# 외부 라이브러리 자동 설치
try:
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    from plotly.subplots import make_subplots
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly", "pandas"])
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="감정 분석 결과",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def safe_get_query_param(param_name, default_value):
    """안전한 쿼리 파라미터 추출"""
    try:
        if hasattr(st, 'query_params'):
            if param_name in st.query_params:
                return st.query_params[param_name]
        elif hasattr(st, 'experimental_get_query_params'):
            params = st.experimental_get_query_params()
            if param_name in params:
                return params[param_name][0]
        return default_value
    except Exception as e:
        st.error(f"쿼리 파라미터 읽기 오류: {e}")
        return default_value

def load_url_history_data():
    """URL에서 압축된 히스토리 데이터 복원"""
    try:
        hist_param = safe_get_query_param('hist', None)
        if not hist_param:
            return []
        
        print(f"📊 URL에서 히스토리 데이터 복원 중... (길이: {len(hist_param)})")
        
        # base64 디코딩 → gzip 압축 해제 → JSON 파싱
        compressed_data = base64.b64decode(hist_param.encode('utf-8'))
        json_str = gzip.decompress(compressed_data).decode('utf-8')
        compact_data = json.loads(json_str)
        
        # 압축된 형식을 원래 형식으로 복원
        restored_history = []
        for item in compact_data:
            try:
                timestamp = datetime.fromtimestamp(item['t'])
                restored_history.append({
                    'emotion': item['e'],
                    'score': float(item['s']),
                    'timestamp': timestamp,
                    'datetime': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'raw_emotion': item['e']
                })
            except (KeyError, ValueError, OSError) as e:
                print(f"⚠️ 데이터 복원 중 오류: {e}")
                continue
        
        print(f"✅ {len(restored_history)}개 히스토리 복원 완료")
        return restored_history
        
    except Exception as e:
        print(f"❌ URL 히스토리 복원 실패: {e}")
        return []

# ✅ 수정: 누락된 함수 추가
def load_local_emotion_history():
    """로컬 감정 히스토리 로드 (파일에서)"""
    try:
        # 로컬 파일에서 히스토리 읽기 시도
        if os.path.exists('emotion_history.json'):
            with open('emotion_history.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                # timestamp 문자열을 datetime 객체로 변환
                for item in data:
                    if isinstance(item['timestamp'], str):
                        item['timestamp'] = datetime.fromisoformat(item['timestamp'])
                return data
    except Exception as e:
        print(f"로컬 히스토리 로드 실패: {e}")
    return []

def load_all_emotion_data():
    """모든 소스에서 감정 데이터 로드"""
    all_history = []
    
    # 1. URL에서 압축된 히스토리 데이터 로드
    url_history = load_url_history_data()
    if url_history:
        all_history.extend(url_history)
        st.sidebar.success(f"📊 URL에서 {len(url_history)}개 기록 로드됨")
    
    # 2. 로컬 파일에서 로드
    local_history = load_local_emotion_history()
    if local_history:
        all_history.extend(local_history)
        st.sidebar.success(f"💾 로컬에서 {len(local_history)}개 기록 로드됨")
    
    # 3. 세션 상태에서 로드
    session_history = st.session_state.get('emotion_history', [])
    if session_history:
        all_history.extend(session_history)
    
    # 4. 중복 제거 (타임스탬프 기준)
    seen_timestamps = set()
    unique_history = []
    
    for entry in sorted(all_history, key=lambda x: x['timestamp']):
        timestamp_key = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        if timestamp_key not in seen_timestamps:
            seen_timestamps.add(timestamp_key)
            unique_history.append(entry)
    
    return unique_history

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
    },
    'disgust': {
        'emoji': '🤢',
        'korean': '혐오',
        'color': '#800080',
        'description': '불쾌한 감정을 건강하게 해소해보세요.',
        'solutions': [
            '🌸 향기로운 것으로 기분 전환하세요',
            '🚿 깨끗하게 씻고 환경을 정리하세요',
            '🎵 좋아하는 음악으로 마음을 달래세요',
            '🌳 신선한 공기를 마시러 나가세요',
            '💭 긍정적인 것들을 떠올려보세요'
        ],
        'quotes': [
            '"불쾌함도 삶의 한 부분이다." - 익명',
            '"나쁜 것을 거부하는 것도 선택의 힘이다." - 익명'
        ],
        'tips': '불쾌한 감정을 느끼는 것은 자연스럽습니다. 환경을 바꿔보세요.'
    }
}

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

def create_enhanced_timeline_chart(history_data, minutes=30):
    """향상된 감정 변화 추이 차트"""
    if not history_data:
        return None
        
    # 최근 N분간 데이터 필터링
    cutoff_time = datetime.now() - timedelta(minutes=minutes)
    recent_data = [h for h in history_data if h['timestamp'] > cutoff_time]
    
    if len(recent_data) < 2:
        return None
    
    # 데이터 준비
    df = pd.DataFrame([
        {
            'time': entry['timestamp'].strftime('%H:%M:%S'),
            'timestamp': entry['timestamp'],
            'emotion': EMOTION_DATA[entry['emotion']]['korean'],
            'emotion_en': entry['emotion'],
            'score': entry['score'] * 100,
            'color': EMOTION_DATA[entry['emotion']]['color'],
            'emoji': EMOTION_DATA[entry['emotion']]['emoji']
        }
        for entry in recent_data
    ])
    
    # 라인 차트 생성
    fig = px.line(df, x='timestamp', y='score',
                  title=f'감정 변화 추이 (최근 {minutes}분)',
                  markers=True,
                  line_shape='spline')
    
    # 감정별로 색상 구분하여 점 추가
    for emotion in df['emotion_en'].unique():
        emotion_data = df[df['emotion_en'] == emotion]
        if not emotion_data.empty:
            fig.add_scatter(
                x=emotion_data['timestamp'],
                y=emotion_data['score'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=EMOTION_DATA[emotion]['color'],
                    symbol='circle',
                    line=dict(width=2, color='white')
                ),
                name=EMOTION_DATA[emotion]['korean'],
                hovertemplate=f"<b>{EMOTION_DATA[emotion]['emoji']} {EMOTION_DATA[emotion]['korean']}</b><br>" +
                             "시간: %{x|%H:%M:%S}<br>" +
                             "신뢰도: %{y:.1f}%<extra></extra>",
                showlegend=True
            )
    
    fig.update_layout(
        height=500,
        xaxis_title="시간",
        yaxis_title="신뢰도 (%)",
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_history_chart():
    """기본 히스토리 차트 함수 (호환성 유지)"""
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

# ✅ 수정: 단일 홈페이지 함수
def show_homepage():
    """홈페이지 (단일 버전)"""
    st.title("🎭 감정 분석 시스템")
    st.markdown("---")
    
    # 📊 대시보드 링크 추가
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 2rem;">
            <h2>🎯 실시간 감정 분석</h2>
            <p>AI가 당신의 감정을 분석하고 맞춤형 솔루션을 제공합니다</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 대시보드 버튼
        if st.button("📊 고급 분석 대시보드", use_container_width=True, type="primary"):
            st.query_params.page = "analytics"
            st.rerun()
    
    # ✅ 수정: 올바른 함수명 사용
    local_history = load_local_emotion_history()
    if local_history:
        st.success(f"✅ 로컬 히스토리: {len(local_history)}개 기록 발견")
        
        # 최근 감정 미리보기
        if len(local_history) > 0:
            recent_emotions = local_history[-5:]
            st.subheader("📈 최근 감정 변화")
            
            cols = st.columns(min(len(recent_emotions), 5))  # 최대 5개 컬럼
            for i, emotion_data in enumerate(recent_emotions):
                with cols[i]:
                    emotion_info = EMOTION_DATA[emotion_data['emotion']]
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; background: {emotion_info['color']}20; border-radius: 10px;">
                        <div style="font-size: 2rem;">{emotion_info['emoji']}</div>
                        <div style="font-size: 0.9rem; color: {emotion_info['color']};">
                            <b>{emotion_info['korean']}</b><br>
                            {emotion_data['score']*100:.1f}%
                        </div>
                        <div style="font-size: 0.7rem; color: #666;">
                            {emotion_data['timestamp'].strftime('%H:%M:%S')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("📭 아직 분석된 감정 데이터가 없습니다. 웹캠 프로그램을 실행해주세요!")

# ✅ 수정: 단일 결과 페이지 함수  
def show_result_page(emotion, score):
    """결과 페이지 표시 (단일 버전)"""
    # URL에서 히스토리 데이터 확인 및 세션 상태 업데이트
    url_history = load_url_history_data()
    
    if url_history:
        if 'emotion_history' not in st.session_state:
            st.session_state.emotion_history = []
        
        # 중복 제거하면서 추가
        existing_times = {h['timestamp'].strftime('%Y-%m-%d %H:%M:%S') 
                         for h in st.session_state.emotion_history}
        
        new_entries = []
        for entry in url_history:
            time_key = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            if time_key not in existing_times:
                new_entries.append(entry)
        
        if new_entries:
            st.session_state.emotion_history.extend(new_entries)
            st.info(f"📊 웹캠에서 {len(new_entries)}개의 새로운 히스토리가 추가되었습니다!")
    
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
            'timestamp': current_time,
            'datetime': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'raw_emotion': emotion
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
    
    # 대시보드 링크 버튼 추가
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📊 자세한 분석 보기", use_container_width=True, type="secondary"):
            st.query_params.page = "analytics"
            st.rerun()
    
    # 새로운 분석 버튼
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📊 대시보드", use_container_width=True, type="secondary"):
            st.query_params.page = "analytics"
            st.rerun()
    with col2:
        if st.button("🔄 홈으로 돌아가기", use_container_width=True, type="primary"):
            st.query_params.clear()
            st.rerun()
    with col3:
        if st.button("🆕 새 분석", use_container_width=True):
            st.query_params.clear()
            st.rerun()

# 나머지 함수들은 기존 코드와 동일...
# (create_emotion_distribution_chart, create_emotion_heatmap, create_emotion_stats_table, show_analytics_page 등)

def main():
    """메인 함수"""
    try:
        # 페이지 파라미터 확인
        page = safe_get_query_param('page', None)
        
        if page == 'analytics':
            show_analytics_page()
            return
        
        # 감정 분석 결과 파라미터 확인
        emotion = safe_get_query_param('emotion', None)
        score_str = safe_get_query_param('score', '0.0')
        
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
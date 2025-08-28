import cv2
import streamlit as st
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
from emotion_model import detect_face_and_analyze, update_latest_emotion, get_latest_emotion, reset_emotion_state
import app as app
import time
import threading


def show_webcam_page():
    """웹캠 페이지 - 실제 웹캠 감정 분석 구현"""    
    st.title("📹 웹캠 감정 분석")
    st.markdown("---")
    
    # 뒤로가기 버튼
    if st.button("🔙 메인으로 돌아가기"):
        reset_emotion_state()
        st.session_state.current_page = 'main'
        st.rerun()
    
    st.markdown("### 🎥 실시간 웹캠 분석")
    st.info("웹캠을 허용해주세요. 얼굴이 감지되면 자동으로 감정을 분석합니다.")
    
    # WebRTC 설정
    RTC_CONFIGURATION = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
    
    class EmotionVideoTransformer(VideoTransformerBase):
        def __init__(self):
            self.frame_count = 0
            
        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            
            # 3프레임마다 감정 분석 (성능 최적화)
            if self.frame_count % 10 == 0:
                emotion, confidence, face_coords = detect_face_and_analyze(img)
                if emotion and confidence > 0.5:  # 신뢰도 50% 이상만
                    update_latest_emotion(emotion, confidence)
                
                # 얼굴 감지된 경우 박스 그리기
                if face_coords:
                    x, y, w, h = face_coords
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    # 감정 텍스트 표시
                    if emotion != 'neutral' and confidence > 0.5:
                        emotion_text = f"{app.EMOTIONS[emotion]['korean']}: {confidence:.2f}"
                        cv2.putText(img, emotion_text, (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            self.frame_count += 1
            return img
    
    # WebRTC 스트리머
    webrtc_ctx = webrtc_streamer(
        key="emotion-detection",
        video_transformer_factory=EmotionVideoTransformer,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    
    # 현재 감정 상태 표시
    emotion, confidence = get_latest_emotion()
    
    if emotion and confidence > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"**감지된 감정**: {app.EMOTIONS[emotion]['emoji']} {app.EMOTIONS[emotion]['korean']}")
            st.write(f"**신뢰도**: {confidence:.2f} ({confidence*100:.1f}%)")
        
        with col2:
            if confidence > 0.6:  # 신뢰도 60% 이상일 때만 결과 페이지 이동 허용
                if st.button("📊 이 결과로 이동하기", key="goto_result"):
                    st.session_state.selected_emotion = emotion
                    st.session_state.current_page = 'result'
                    st.rerun()
            else:
                st.warning("신뢰도가 낮습니다. 얼굴을 더 명확하게 보여주세요.")
    
    else:
        st.info("얼굴을 카메라에 맞춰주세요. 감정 분석을 시작합니다...")
    
    # 사용 안내
    with st.expander("📋 사용 안내"):
        st.write("""
        **웹캠 사용 팁**:
        - 얼굴이 화면 중앙에 오도록 위치해주세요
        - 충분한 조명을 확보해주세요
        - 카메라와 적당한 거리(30-50cm)를 유지해주세요
        - 감정 표현을 자연스럽게 해주세요
        
        **주의사항**:
        - HTTPS 환경에서만 웹캠 접근이 가능합니다
        - 처음 실행 시 브라우저에서 카메라 권한을 허용해야 합니다
        - 신뢰도 60% 이상일 때 결과 페이지로 이동할 수 있습니다
        """)
    
    # 테스트용 감정 결과 (웹캠이 작동하지 않을 때 대안)
    st.markdown("---")
    st.markdown("### 🧪 웹캠이 작동하지 않나요?")
    st.write("테스트용 감정을 선택해서 결과를 확인해보세요:")
    
    cols = st.columns(3)
    test_emotions = ['happy', 'sad', 'angry']
    for i, emotion in enumerate(test_emotions):
        with cols[i]:
            if st.button(f"테스트: {app.EMOTIONS[emotion]['korean']}", key=f"test_{emotion}"):
                st.session_state.current_page = 'result'
                st.session_state.selected_emotion = emotion
                st.rerun()



emotion_lock = threading.Lock()
emotion_history = []

def update_latest_emotion(emotion, confidence):
    global emotion_history, latest_emotion, latest_confidence
    with emotion_lock:
        latest_emotion = emotion
        latest_confidence = confidence
        # 시간과 함께 기록
        emotion_history.append((time.time(), emotion, confidence))

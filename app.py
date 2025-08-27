import streamlit as st

# 페이지 설정
st.set_page_config(page_title="😊 감정 분석 데모", page_icon="🎭", layout="wide")

# 제목
st.title("😊 감정 분석 프로젝트")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("설정")
    st.write("여기에 옵션들을 추가할 수 있어요!")

# 버튼 만들기
if st.button("👉 웹캠 시작하기"):
    st.write("📸 웹캠이 여기에 연결될 거예요!")

else:
    st.write("버튼을 누르면 웹캠이 시작됩니다.")

# 푸터
st.markdown("---")
st.caption("Made with Streamlit 🚀")

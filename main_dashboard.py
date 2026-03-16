import streamlit as st

st.set_page_config(page_title="AI Smart Sugar Mill", layout="wide")

st.title("🏭 AI Smart Sugar Mill System")

st.write("Click any module to open its dashboard")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.subheader("⚙ Fault Detection")
    if st.button("Open Fault Detection"):
        st.switch_page("pages/faultdet.py")

with col2:
    st.subheader("🧪 Juice Clarification")
    if st.button("Open Clarification"):
        st.switch_page("pages/phcalc.py")

with col3:
    st.subheader("🍬 Crystallization")
    if st.button("Open Crystallization"):
        st.switch_page("pages/crystall.py")

with col4:
    st.subheader("🌾 Mill Optimization")
    if st.button("Open Mill Optimization"):
        st.switch_page("pages/mill_opt.py")
import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="AI Machine Monitoring", layout="wide")

st.title("AI Driven Machine Monitoring and Fault Detection/Prediction System")

# ---------------------------
# Train AI Fault Detection Model
# ---------------------------

X = [
    [55,15,110,1000],
    [60,18,115,980],
    [52,14,105,1020],
    [58,16,112,990],
    [90,40,160,1300],
    [95,45,170,1250],
    [100,50,180,750],
    [85,38,150,700]
]

y = [0,0,0,0,1,1,1,1]

model = RandomForestClassifier()
model.fit(X,y)

# ---------------------------
# Store sensor history
# ---------------------------

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=["Temp","Vibration","Pressure","RPM"]
    )

# ---------------------------
# Sensor Simulation
# ---------------------------

def generate_sensor_data():

    temp = np.random.normal(60,8)
    vib = np.random.normal(18,6)
    press = np.random.normal(115,15)
    rpm = np.random.normal(1000,120)

    return round(temp,2),round(vib,2),round(press,2),round(rpm,2)

# ---------------------------
# Fault Logic
# ---------------------------

def check_fault(temp,vib,press,rpm):

    fault_temp = temp > 85
    fault_vib = vib > 35
    fault_press = press > 150
    fault_rpm = rpm > 1200 or rpm < 800

    return fault_temp,fault_vib,fault_press,fault_rpm

# ---------------------------
# Machine Health Score
# ---------------------------

def health_score(temp,vib,press,rpm):

    score = 100

    if temp > 85:
        score -= 25
    if vib > 35:
        score -= 25
    if press > 150:
        score -= 25
    if rpm > 1200 or rpm < 800:
        score -= 25

    return max(score,0)

# ---------------------------
# Predict Future Fault
# ---------------------------

def predict_future_fault(history):

    if len(history) < 6:
        return None

    recent = history.tail(6)

    temp_trend = recent["Temp"].iloc[-1] - recent["Temp"].iloc[0]
    vib_trend = recent["Vibration"].iloc[-1] - recent["Vibration"].iloc[0]
    press_trend = recent["Pressure"].iloc[-1] - recent["Pressure"].iloc[0]
    rpm_trend = recent["RPM"].iloc[-1] - recent["RPM"].iloc[0]

    if vib_trend > 8:
        return "Increasing vibration trend"

    if temp_trend > 10:
        return "Temperature rising rapidly"

    if press_trend > 15:
        return "Pressure increasing"

    if rpm_trend > 200:
        return "RPM instability"

    return None


placeholder = st.empty()

while True:

    temp,vib,press,rpm = generate_sensor_data()

    prediction = model.predict([[temp,vib,press,rpm]])[0]

    fault_temp,fault_vib,fault_press,fault_rpm = check_fault(temp,vib,press,rpm)

    health = health_score(temp,vib,press,rpm)

    new_row = pd.DataFrame(
        [[temp,vib,press,rpm]],
        columns=["Temp","Vibration","Pressure","RPM"]
    )

    st.session_state.history = pd.concat(
        [st.session_state.history,new_row]
    )

    st.session_state.history = st.session_state.history.tail(50)

    with placeholder.container():

        st.subheader("Live Sensor Monitoring")

        col1,col2,col3,col4 = st.columns(4)

        # Temperature
        if fault_temp:
            col1.markdown(
                f"<h2 style='color:red;text-align:center;'>🔥 Temperature<br>{temp} °C</h2>",
                unsafe_allow_html=True
            )
        else:
            col1.metric("Temperature (°C)",temp)

        # Vibration
        if fault_vib:
            col2.markdown(
                f"<h2 style='color:red;text-align:center;'>🔥 Vibration<br>{vib}</h2>",
                unsafe_allow_html=True
            )
        else:
            col2.metric("Vibration",vib)

        # Pressure
        if fault_press:
            col3.markdown(
                f"<h2 style='color:red;text-align:center;'>🔥 Pressure<br>{press}</h2>",
                unsafe_allow_html=True
            )
        else:
            col3.metric("Pressure",press)

        # RPM
        if fault_rpm:
            col4.markdown(
                f"<h2 style='color:red;text-align:center;'>🔥 RPM<br>{rpm}</h2>",
                unsafe_allow_html=True
            )
        else:
            col4.metric("RPM",rpm)

        st.markdown("---")

        # Machine Health

        st.subheader("Machine Health")

        st.progress(health/100)

        st.write(f"Machine Health Score: **{health}%**")

        st.markdown("---")

        # Predict Future Fault

        future_fault = predict_future_fault(st.session_state.history)

        if future_fault:

            st.warning("⚠ Predicted Fault in 30 seconds")

            st.info(f"Possible Cause: {future_fault}")

        # Decision Engine

        if prediction == 1:

            st.error("⚠ FAULT DETECTED – Maintenance Required")

            # Toast notification
            st.toast("⚠ Fault detected, attention required / maintenance required")

            # Popup alert
            st.markdown(
                """
                <script>
                alert("⚠ FAULT DETECTED! Maintenance Required.");
                </script>
                """,
                unsafe_allow_html=True
            )

        else:

            st.success("Machine Running Normally")

        st.markdown("---")

        # Sensor History Graph

        st.subheader("Sensor History (Last 50 Readings)")

        st.line_chart(st.session_state.history)

    time.sleep(5)
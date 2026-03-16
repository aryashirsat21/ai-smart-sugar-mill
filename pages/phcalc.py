import streamlit as st
import pandas as pd
import random
import time
from sklearn.linear_model import LinearRegression

# -----------------------------
# Training dataset (simulated sugar factory data)
# -----------------------------

data = {
    "pH":[4.8,5.0,5.2,5.4,5.6],
    "temperature":[70,72,75,78,80],   # °C
    "turbidity":[200,180,150,120,100], # NTU
    "brix":[15,16,17,18,19],           # °Bx
    "lime_dose":[12,10,8,6,5]          # kg / 1000 L juice
}

df = pd.DataFrame(data)

X = df[["pH","temperature","turbidity","brix"]]
y = df["lime_dose"]

model = LinearRegression()
model.fit(X,y)

# -----------------------------
# Streamlit UI
# -----------------------------

st.title("AI Sugarcane Juice Clarification System")

st.subheader("Live Sensor Data from Juice Tank")

placeholder = st.empty()

sensor_data = []

for i in range(30):

    # -----------------------------
    # Simulated Sensors
    # -----------------------------

    ph = round(random.uniform(4.8,5.6),2)          # pH (unitless)
    temp = random.randint(70,80)                   # °C
    turbidity = random.randint(100,200)            # NTU
    brix = round(random.uniform(15,19),1)          # °Bx

    new_data = pd.DataFrame(
        [[ph,temp,turbidity,brix]],
        columns=["pH","temperature","turbidity","brix"]
    )

    prediction = model.predict(new_data)

    sensor_data.append({
        "pH":ph,
        "Temperature (°C)":temp,
        "Turbidity (NTU)":turbidity,
        "Brix (°Bx)":brix,
        "Lime Dose (kg/1000L)":round(prediction[0],2)
    })

    sensor_df = pd.DataFrame(sensor_data)

    with placeholder.container():

        # -----------------------------
        # Live Metrics
        # -----------------------------

        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)

        col1.metric("pH Sensor", ph)
        col2.metric("Temperature (°C)", temp)

        col3.metric("Turbidity (NTU)", turbidity)
        col4.metric("Brix (°Bx)", brix)

        # -----------------------------
        # AI Recommendation
        # -----------------------------

        st.success(
            f"Recommended Lime Dose: {prediction[0]:.2f} kg per 1000 L juice"
        )

        # -----------------------------
        # Sensor Trend Graph
        # -----------------------------

        st.subheader("Sensor Trends")

        st.line_chart(sensor_df)

    time.sleep(3)
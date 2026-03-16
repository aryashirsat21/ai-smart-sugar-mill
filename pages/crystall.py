import streamlit as st
import pandas as pd
import random
import time
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI Sugar Crystallization Control", layout="wide")

st.title("AI Sugar Crystallization Monitoring System")

st.write(
"AI monitors **vacuum pan crystallization process** using temperature, brix, pressure, level "
"and supersaturation sensors to optimize crystal growth."
)

# -----------------------------
# Training dataset (simulated)
# -----------------------------

data = pd.DataFrame({

"temperature":[110,112,114,116,118],      # °C
"brix":[70,72,74,76,78],                  # °Bx
"pressure":[-0.85,-0.87,-0.90,-0.92,-0.95], # bar vacuum
"level":[50,55,60,65,70],                 # %
"supersaturation":[1.15,1.20,1.25,1.30,1.35],
"crystal_quality":[70,75,80,85,90]        # %

})

X = data[["temperature","brix","pressure","level","supersaturation"]]
y = data["crystal_quality"]

model = LinearRegression()
model.fit(X,y)

placeholder = st.empty()

history = []

# -----------------------------
# Live simulation loop
# -----------------------------

while True:

    temperature = random.randint(110,118)          # °C
    brix = random.randint(70,78)                   # °Bx
    pressure = round(random.uniform(-0.95,-0.85),2) # bar vacuum
    level = random.randint(50,70)                  # %
    supersat = round(random.uniform(1.15,1.35),2)

    input_data = pd.DataFrame(
        [[temperature,brix,pressure,level,supersat]],
        columns=["temperature","brix","pressure","level","supersaturation"]
    )

    crystal_quality = model.predict(input_data)[0]

    history.append({

        "Temperature (°C)":temperature,
        "Brix (°Bx)":brix,
        "Vacuum Pressure (bar)":pressure,
        "Pan Level (%)":level,
        "Supersaturation":supersat,
        "Crystal Quality (%)":crystal_quality

    })

    df_history = pd.DataFrame(history)

    with placeholder.container():

        st.subheader("⚙ Vacuum Pan Sensor Monitoring")

        c1,c2,c3,c4,c5 = st.columns(5)

        c1.metric("Temperature (°C)",temperature)
        c2.metric("Brix (°Bx)",brix)
        c3.metric("Vacuum Pressure (bar)",pressure)
        c4.metric("Pan Level (%)",level)
        c5.metric("Supersaturation",supersat)

        st.markdown("---")

        # AI prediction

        st.success(f"Predicted Crystal Quality: **{crystal_quality:.2f}%**")

        # Control recommendation

        if crystal_quality > 85:

            st.success("🟢 Optimal Crystal Growth")

        elif crystal_quality > 75:

            st.warning("🟡 Adjust Steam Flow or Feed Syrup")

        else:

            st.error("🔴 Poor Crystallization - Increase Supersaturation")

        st.markdown("---")

        # Crystal growth trend

        st.subheader("📈 Crystal Growth Trend")

        st.line_chart(df_history["Crystal Quality (%)"])

        # Sensor history

        st.subheader("📊 Process History")

        st.dataframe(df_history.tail(10), use_container_width=True)

    time.sleep(5)
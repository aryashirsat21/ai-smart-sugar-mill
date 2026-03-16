import streamlit as st
import pandas as pd
import random
import time
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI Sugar Mill Optimization", layout="wide")

# ----------------------------
# Card UI
# ----------------------------
def render_card(title,value,unit):

    st.markdown(
        f"""
        <div style="
        background:#1f2937;
        padding:20px;
        border-radius:12px;
        text-align:center;
        color:white;
        box-shadow:0px 3px 10px rgba(0,0,0,0.3)">
        <h4>{title}</h4>
        <h2 style="color:#22c55e">{value} {unit}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("AI Sugar Mill Optimization Dashboard")

st.write(
"AI system monitors **mill load, roller pressure, bagasse moisture and imbibition water flow** "
"to predict optimal extraction efficiency."
)

# --------------------------------
# Training Dataset
# --------------------------------

data = pd.DataFrame({

    "mill_load":[60,65,70,75,80],
    "roller_pressure":[180,190,200,210,220],
    "bagasse_moisture":[50,48,45,42,40],
    "imbibition_flow":[30,32,35,38,40],
    "efficiency":[72,76,81,86,90]

})

X = data[["mill_load","roller_pressure","bagasse_moisture","imbibition_flow"]]
y = data["efficiency"]

model = LinearRegression()
model.fit(X,y)

placeholder = st.empty()

history = []

while True:

    # ----------------------------
    # Simulated Sensors
    # ----------------------------

    mill_load = random.randint(60,80)            # TPH
    roller_pressure = random.randint(180,220)    # bar
    bagasse_moisture = random.randint(40,50)     # %
    imbibition_flow = random.randint(30,40)      # m3/hr

    input_data = pd.DataFrame(
        [[mill_load,roller_pressure,bagasse_moisture,imbibition_flow]],
        columns=["mill_load","roller_pressure","bagasse_moisture","imbibition_flow"]
    )

    efficiency = model.predict(input_data)[0]

    history.append({

        "Mill Load (TPH)":mill_load,
        "Roller Pressure (bar)":roller_pressure,
        "Bagasse Moisture (%)":bagasse_moisture,
        "Imbibition Flow (m3/hr)":imbibition_flow,
        "Extraction Efficiency (%)":efficiency

    })

    df_history = pd.DataFrame(history)

    with placeholder.container():

        st.subheader("⚙ Live Mill Parameters")

        c1,c2,c3,c4 = st.columns(4)

        with c1:
            render_card("Mill Load",mill_load,"TPH")

        with c2:
            render_card("Roller Pressure",roller_pressure,"bar")

        with c3:
            render_card("Bagasse Moisture",bagasse_moisture,"%")

        with c4:
            render_card("Imbibition Water Flow",imbibition_flow,"m³/hr")

        st.markdown("---")

        # --------------------------------
        # AI Efficiency Prediction
        # --------------------------------

        st.success(
        f"Predicted Extraction Efficiency: **{efficiency:.2f}%**"
        )

        if efficiency > 88:
            st.success("🟢 Mill Operating at Optimal Efficiency")

        elif efficiency > 78:
            st.warning("🟡 Moderate Efficiency - Adjust Conveyor Speed")

        else:
            st.error("🔴 Low Efficiency - Check Roller Pressure & Imbibition Flow")

        st.markdown("---")

        # --------------------------------
        # Efficiency Trend
        # --------------------------------

        st.subheader("📈 Efficiency Trend")

        st.line_chart(df_history["Extraction Efficiency (%)"])

        # --------------------------------
        # Historical Data
        # --------------------------------

        st.subheader("📊 Historical Sensor Data")

        st.dataframe(df_history.tail(10), use_container_width=True)

    time.sleep(5)
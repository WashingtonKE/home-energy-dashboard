import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly

st.set_page_config(page_title="Power Forecast", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("HomeC.zip")
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df

df = load_data()

st.title("🔮 Forecast Future Power Usage")

# Resample to hourly
df_hour = df.resample("H", on="time")["use [kW]"].mean().reset_index()
df_hour.columns = ["ds", "y"]

# Forecast slider
periods = st.sidebar.slider("Forecast Horizon (hours)", 24, 720, 168)

# Train Prophet
model = Prophet(daily_seasonality=True, weekly_seasonality=True)
model.fit(df_hour)

# Future
future = model.make_future_dataframe(periods=periods, freq="H")
forecast = model.predict(future)

st.subheader("📈 Forecast Plot")
fig = plot_plotly(model, forecast)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📉 Components (Trend / Seasonality)")
fig2 = model.plot_components(forecast)
st.pyplot(fig2)
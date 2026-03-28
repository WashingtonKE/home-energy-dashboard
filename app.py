import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Home Energy Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("HomeC.zip")  # loads zipped CSV
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

df = load_data()

st.title("🏡 Home Energy Dashboard")

# KPIs
total_use = df['use [kW]'].sum()
avg_use = df['use [kW]'].mean()
max_use = df['use [kW]'].max()

c1, c2, c3 = st.columns(3)
c1.metric("Total Energy Used (kW)", f"{total_use:,.2f}")
c2.metric("Average Power (kW)", f"{avg_use:.3f}")
c3.metric("Peak Power (kW)", f"{max_use:.3f}")

# Line chart
st.subheader("📈 Power Usage Over Time")
fig = px.line(df, x="time", y="use [kW]", title="Household Power Consumption")
st.plotly_chart(fig, use_container_width=True)

# Appliance breakdown
st.subheader("🔌 Appliance Consumption Breakdown")
appliances = [
    'Dishwasher [kW]','Furnace 1 [kW]','Furnace 2 [kW]',
    'Home office [kW]','Fridge [kW]','Wine cellar [kW]',
    'Garage door [kW]','Kitchen 12 [kW]','Kitchen 14 [kW]',
    'Kitchen 38 [kW]','Microwave [kW]','Living room [kW]',
    'Barn [kW]','Well [kW]'
]
totals = df[appliances].sum().sort_values(ascending=False)

fig2 = px.bar(
    totals,
    x=totals.index,
    y=totals.values,
    title="Total Energy Use by Appliance"
)
st.plotly_chart(fig2, use_container_width=True)

# Solar vs grid
st.subheader("☀️ Solar vs Grid Usage")
df["grid_use"] = df["use [kW]"] - df["Solar [kW]"]

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df["time"], y=df["Solar [kW]"], name="Solar"))
fig3.add_trace(go.Scatter(x=df["time"], y=df["grid_use"], name="Grid"))
fig3.update_layout(title="Solar vs Grid Consumption")
st.plotly_chart(fig3, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Kenya Maternal Health Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/FelixBeruTheAnalyst/kenya-maternal-health-anc-analysis/main/kenya_maternal_health_master.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Header
st.title("🏥 Kenya Maternal & Child Health Dashboard")
st.markdown("**A Four-Part County-Level Analysis | KDHS 2022**")
st.markdown("*By Felix Beru | Data Analyst | Nairobi, Kenya*")
st.divider()

# Key metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("National ANC Coverage", f"{df['ANC_Coverage'].mean():.1f}%")
with col2:
    st.metric("Under-5 Mortality", f"{df['Under5_Mortality'].mean():.0f} per 1,000")
with col3:
    st.metric("Facility Delivery Rate", f"{df['Facility_Delivery'].mean():.1f}%")
with col4:
    st.metric("4+ ANC Visits", f"{df['ANC_4plus_visits'].mean():.1f}%")

st.divider()

# Sidebar
st.sidebar.title("🔍 Explore")
st.sidebar.markdown("Filter and explore maternal health indicators across Kenya")

selected_indicator = st.sidebar.selectbox(
    "Select Indicator",
    options=[
        'ANC_Coverage',
        'Under5_Mortality',
        'Facility_Delivery',
        'ANC_4plus_visits',
        'No_ANC',
        'First_visit_under4months'
    ],
    format_func=lambda x: {
        'ANC_Coverage': '1. Skilled ANC Coverage (%)',
        'Under5_Mortality': '2. Under-5 Mortality (per 1,000)',
        'Facility_Delivery': '3. Facility Delivery Rate (%)',
        'ANC_4plus_visits': '4. Women with 4+ ANC Visits (%)',
        'No_ANC': '5. Women with No ANC (%)',
        'First_visit_under4months': '6. First Trimester Initiation (%)'
    }[x]
)

selected_county = st.sidebar.selectbox(
    "Select County for Spotlight",
    options=sorted(df['County'].tolist())
)

st.sidebar.divider()
st.sidebar.markdown("🔴 **Crisis Counties:** Mandera, Wajir, Garissa")
st.sidebar.markdown("🟢 **Top Counties:** Nairobi City, Nyeri, Kiambu")

# Main chart — selected indicator
crisis_counties = ['Mandera', 'Wajir', 'Garissa']
top_counties = ['Nairobi City', 'Nyeri', 'Kiambu']

def get_color(county):
    if county in crisis_counties: return '#e74c3c'
    elif county in top_counties: return '#2ecc71'
    else: return '#3498db'

st.subheader(f"📊 {selected_indicator.replace('_', ' ')} by County")

df_sorted = df.sort_values(selected_indicator, ascending=True)
colors = [get_color(c) for c in df_sorted['County']]

fig = go.Figure(go.Bar(
    x=df_sorted[selected_indicator],
    y=df_sorted['County'],
    orientation='h',
    marker_color=colors,
    hovertemplate='<b>%{y}</b><br>Value: %{x:.1f}<extra></extra>'
))

fig.add_vline(
    x=df[selected_indicator].mean(),
    line_dash='dash',
    line_color='navy',
    annotation_text=f"National Avg: {df[selected_indicator].mean():.1f}"
)

fig.update_layout(
    height=600,
    plot_bgcolor='#f8f9fa',
    paper_bgcolor='white',
    yaxis=dict(tickfont=dict(size=9))
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# County spotlight
st.subheader(f"🔍 County Spotlight — {selected_county}")

county_data = df[df['County'] == selected_county].iloc[0]

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("ANC Coverage", f"{county_data['ANC_Coverage']:.1f}%",
              delta=f"{county_data['ANC_Coverage'] - df['ANC_Coverage'].mean():.1f}% vs national avg")
    st.metric("Facility Delivery", f"{county_data['Facility_Delivery']:.1f}%",
              delta=f"{county_data['Facility_Delivery'] - df['Facility_Delivery'].mean():.1f}% vs national avg")
with c2:
    st.metric("Under-5 Mortality", f"{county_data['Under5_Mortality']:.0f} per 1,000",
              delta=f"{county_data['Under5_Mortality'] - df['Under5_Mortality'].mean():.0f} vs national avg",
              delta_color='inverse')
    st.metric("4+ ANC Visits", f"{county_data['ANC_4plus_visits']:.1f}%",
              delta=f"{county_data['ANC_4plus_visits'] - df['ANC_4plus_visits'].mean():.1f}% vs national avg")
with c3:
    st.metric("No ANC", f"{county_data['No_ANC']:.1f}%",
              delta=f"{county_data['No_ANC'] - df['No_ANC'].mean():.1f}% vs national avg",
              delta_color='inverse')
    st.metric("First Trimester Visits", f"{county_data['First_visit_under4months']:.1f}%",
              delta=f"{county_data['First_visit_under4months'] - df['First_visit_under4months'].mean():.1f}% vs national avg")

st.divider()

# Crisis counties table
st.subheader("⚠️ Crisis Counties — Consistently Underperforming")
crisis_df = df[df['County'].isin(crisis_counties)][
    ['County', 'ANC_Coverage', 'Under5_Mortality', 'Facility_Delivery', 'ANC_4plus_visits']
].set_index('County')
st.dataframe(crisis_df.style.highlight_min(color='#ffcccc'), use_container_width=True)

st.divider()
st.caption("Source: Kenya Demographic and Health Survey (KDHS) 2022 | Built by Felix Beru")
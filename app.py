import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="Kenya Maternal Health Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    master_url = "https://raw.githubusercontent.com/FelixBeruTheAnalyst/kenya-maternal-health-anc-analysis/main/kenya_maternal_health_master.csv"
    scorecard_url = "https://raw.githubusercontent.com/FelixBeruTheAnalyst/kenya-maternal-health-anc-analysis/main/kenya_kcmhi_scorecard.csv"
    df = pd.read_csv(master_url)
    df_scorecard = pd.read_csv(scorecard_url)
    return df, df_scorecard

df, df_scorecard = load_data()

# Color functions
def get_color(county):
    crisis = ['Mandera', 'Wajir', 'Garissa']
    top = ['Nairobi City', 'Nyeri', 'Kiambu']
    if county in crisis: return '#e74c3c'
    elif county in top: return '#2ecc71'
    else: return '#3498db'

def tier_color(tier):
    if 'High' in tier: return '#2ecc71'
    elif 'Moderate' in tier: return '#3498db'
    elif 'At Risk' in tier: return '#f39c12'
    else: return '#e74c3c'

# Sidebar
st.sidebar.title("🏥 Kenya Maternal Health")
st.sidebar.markdown("**KDHS 2022 Analysis**")
st.sidebar.markdown("*By Felix Beru | Data Analyst*")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "🏆 KCMHI Scorecard", "🔍 County Spotlight"]
)

st.sidebar.divider()
st.sidebar.markdown("🔴 **Crisis Counties**")
st.sidebar.markdown("Mandera • Wajir • Garissa")
st.sidebar.markdown("🟢 **Top Counties**")
st.sidebar.markdown("Nairobi City • Nyeri • Kiambu")
st.sidebar.divider()
st.sidebar.caption("Source: KDHS 2022 | KNBS Kenya")

# =====================
# PAGE 1 — DASHBOARD
# =====================
if page == "📊 Dashboard":
    st.title("🏥 Kenya Maternal & Child Health Dashboard")
    st.markdown("**A Four-Part County-Level Analysis | KDHS 2022**")
    st.divider()

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("National ANC Coverage",
                  f"{df['ANC_Coverage'].mean():.1f}%")
    with col2:
        st.metric("Under-5 Mortality",
                  f"{df['Under5_Mortality'].mean():.0f} per 1,000")
    with col3:
        st.metric("Facility Delivery Rate",
                  f"{df['Facility_Delivery'].mean():.1f}%")
    with col4:
        st.metric("4+ ANC Visits",
                  f"{df['ANC_4plus_visits'].mean():.1f}%")

    st.divider()

    # Indicator selector
    selected_indicator = st.selectbox(
        "Select Indicator to Explore",
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
        annotation_text=f"◄ National Avg: {df[selected_indicator].mean():.1f}",
        annotation_font_color='navy',
        annotation_font_size=11
    )

    # Tighten axis
    x_min = max(0, df[selected_indicator].min() - 5)
    fig.update_layout(
        height=600,
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        yaxis=dict(tickfont=dict(size=9)),
        xaxis=dict(range=[x_min, df[selected_indicator].max() + 5])
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================
# PAGE 2 — SCORECARD
# =====================
elif page == "🏆 KCMHI Scorecard":
    st.title("🏆 Kenya County Maternal Health Index (KCMHI)")
    st.markdown("**Composite Policy Scorecard — All 47 Counties Ranked**")
    st.divider()

    # Tier metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high = len(df_scorecard[df_scorecard['Tier'].str.contains('High')])
        st.metric("🟢 High Performing", f"{high} counties")
    with col2:
        mod = len(df_scorecard[df_scorecard['Tier'].str.contains('Moderate')])
        st.metric("🔵 Moderate", f"{mod} counties")
    with col3:
        risk = len(df_scorecard[df_scorecard['Tier'].str.contains('At Risk')])
        st.metric("🟡 At Risk", f"{risk} counties")
    with col4:
        crit = len(df_scorecard[df_scorecard['Tier'].str.contains('Critical')])
        st.metric("🔴 Critical", f"{crit} counties")

    st.divider()

    # Scorecard chart
    df_sc_sorted = df_scorecard.sort_values('KCMHI_Score', ascending=True)
    colors_sc = [tier_color(t) for t in df_sc_sorted['Tier']]

    nat_avg_sc = df_scorecard['KCMHI_Score'].mean()

    fig2 = go.Figure(go.Bar(
        x=df_sc_sorted['KCMHI_Score'],
        y=df_sc_sorted['County'],
        orientation='h',
        marker_color=colors_sc,
        hovertemplate='<b>%{y}</b><br>KCMHI Score: %{x:.1f}<br>Rank: #' +
                      df_sc_sorted['Rank'].astype(str) + '<extra></extra>',
        text=df_sc_sorted['KCMHI_Score'].round(1),
        textposition='outside'
    ))

    fig2.add_vline(
        x=nat_avg_sc,
        line_dash='dash',
        line_color='navy',
        annotation_text=f"◄ National Avg: {nat_avg_sc:.1f}",
        annotation_font_color='navy',
        annotation_font_size=11
    )

    fig2.update_layout(
        height=700,
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        yaxis=dict(tickfont=dict(size=9)),
        xaxis=dict(range=[15, 105],
                   title='KCMHI Score (0-100)'),
        title='KCMHI Composite Score by County'
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Methodology
    with st.expander("📋 View Methodology & Weights"):
        st.markdown("""
        ### How the KCMHI Score is Calculated
        Each county is scored from 0-100 based on six weighted indicators:

        | Indicator | Weight | Direction |
        |---|---|---|
        | Under-5 Mortality | 25% | Lower = Better |
        | Facility Delivery Rate | 20% | Higher = Better |
        | 4+ ANC Visits | 20% | Higher = Better |
        | No ANC | 15% | Lower = Better |
        | First Trimester Initiation | 10% | Higher = Better |
        | ANC Coverage | 10% | Higher = Better |

        Each indicator is normalized to a 0-100 scale before weighting.
        Under-5 Mortality carries the highest weight as the ultimate 
        outcome indicator of maternal and child health system performance.
        """)

    # Full scorecard table
    st.subheader("📋 Full Scorecard Table")
    st.dataframe(
        df_scorecard[['Rank', 'County', 'KCMHI_Score', 'Tier']].set_index('Rank'),
        use_container_width=True,
        height=400
    )

# =====================
# PAGE 3 — COUNTY SPOTLIGHT
# =====================
elif page == "🔍 County Spotlight":
    st.title("🔍 County Spotlight")
    st.markdown("**Explore all indicators for any county**")
    st.divider()

    selected_county = st.selectbox(
        "Select County",
        options=sorted(df['County'].tolist())
    )

    county_data = df[df['County'] == selected_county].iloc[0]
    scorecard_data = df_scorecard[df_scorecard['County'] == selected_county]

    # KCMHI Score
    if not scorecard_data.empty:
        score = scorecard_data.iloc[0]['KCMHI_Score']
        rank = scorecard_data.iloc[0]['Rank']
        tier = scorecard_data.iloc[0]['Tier']
        st.markdown(f"### KCMHI Score: **{score}** | Rank: **#{rank}/47** | Tier: **{tier}**")
        st.progress(int(score))

    st.divider()

    # All indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ANC Coverage",
                  f"{county_data['ANC_Coverage']:.1f}%",
                  delta=f"{county_data['ANC_Coverage'] - df['ANC_Coverage'].mean():.1f}% vs avg")
        st.metric("Facility Delivery",
                  f"{county_data['Facility_Delivery']:.1f}%",
                  delta=f"{county_data['Facility_Delivery'] - df['Facility_Delivery'].mean():.1f}% vs avg")
    with col2:
        st.metric("Under-5 Mortality",
                  f"{county_data['Under5_Mortality']:.0f} per 1,000",
                  delta=f"{county_data['Under5_Mortality'] - df['Under5_Mortality'].mean():.0f} vs avg",
                  delta_color='inverse')
        st.metric("4+ ANC Visits",
                  f"{county_data['ANC_4plus_visits']:.1f}%",
                  delta=f"{county_data['ANC_4plus_visits'] - df['ANC_4plus_visits'].mean():.1f}% vs avg")
    with col3:
        st.metric("No ANC",
                  f"{county_data['No_ANC']:.1f}%",
                  delta=f"{county_data['No_ANC'] - df['No_ANC'].mean():.1f}% vs avg",
                  delta_color='inverse')
        st.metric("First Trimester",
                  f"{county_data['First_visit_under4months']:.1f}%",
                  delta=f"{county_data['First_visit_under4months'] - df['First_visit_under4months'].mean():.1f}% vs avg")

    st.divider()

    # Radar chart
    st.subheader(f"📡 {selected_county} — Performance Radar")

    categories = ['ANC Coverage', 'Facility Delivery',
                  '4+ ANC Visits', 'First Trimester',
                  'No ANC (inverted)', 'U5 Mortality (inverted)']

    # Normalize for radar
    def norm(val, col, invert=False):
        min_v = df[col].min()
        max_v = df[col].max()
        n = (val - min_v) / (max_v - min_v) * 100
        return 100 - n if invert else n

    values = [
        norm(county_data['ANC_Coverage'], 'ANC_Coverage'),
        norm(county_data['Facility_Delivery'], 'Facility_Delivery'),
        norm(county_data['ANC_4plus_visits'], 'ANC_4plus_visits'),
        norm(county_data['First_visit_under4months'], 'First_visit_under4months'),
        norm(county_data['No_ANC'], 'No_ANC', invert=True),
        norm(county_data['Under5_Mortality'], 'Under5_Mortality', invert=True),
    ]
    values += values[:1]
    categories += categories[:1]

    fig3 = go.Figure(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(52, 152, 219, 0.3)',
        line=dict(color='#3498db', width=2),
        name=selected_county
    ))

    fig3.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        height=450,
        title=f'{selected_county} — Performance Across All Indicators'
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.caption("Kenya Demographic and Health Survey (KDHS) 2022 | "
           "Built by Felix Beru | Data Analyst | Nairobi, Kenya | "
           "github.com/FelixBeruTheAnalyst")

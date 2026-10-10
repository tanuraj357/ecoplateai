import os
import joblib
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- PAGE SETTINGS ----------
st.set_page_config(
    page_title="Eco Plate AI | Smart Food Planning",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #f4faf5 0%, #edf7f2 50%, #f8fbf7 100%);
}
h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: #153e32;
}
.hero {
    padding: 34px;
    border-radius: 24px;
    background: linear-gradient(120deg, #123c30, #16745b, #32a879);
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 12px 32px rgba(18, 80, 57, .18);
    animation: appear .7s ease-out;
}
.hero h1 { color: white !important; font-size: 38px; margin: 0; }
.hero p { color: #e1f7e9; font-size: 16px; margin-bottom: 0; }
.eyebrow {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
    color: #b8f3ce;
}
.metric-card {
    background: rgba(255,255,255,.94);
    border: 1px solid #dcece2;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 5px 18px rgba(22, 70, 49, .06);
    transition: transform .22s ease, box-shadow .22s ease;
    min-height: 125px;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 25px rgba(22, 70, 49, .12);
}
.metric-label { color: #647b70; font-size: 13px; font-weight: 600; }
.metric-value { color: #174c39; font-size: 30px; font-weight: 800; margin-top: 8px; }
.metric-icon { font-size: 22px; }
.section-card {
    background: white;
    padding: 22px;
    border: 1px solid #e1eee5;
    border-radius: 20px;
    box-shadow: 0 5px 18px rgba(22, 70, 49, .045);
}
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #123c30, #1b5944);
}
div[data-testid="stSidebar"] * { color: #f1fff5; }
div[data-testid="stSidebar"] label { font-weight: 600; }
.stButton > button {
    background: linear-gradient(100deg, #16745b, #2aa876);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 700;
    transition: .2s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 16px rgba(22,116,91,.25);
    color: white;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #dcece2;
    border-radius: 14px;
}
@keyframes appear {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.footer {
    text-align: center;
    color: #688176;
    padding: 24px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD FILES ----------
@st.cache_resource
def load_model():
    return joblib.load(os.path.join(BASE_DIR, "model.pkl"))

@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE_DIR, "train_merged.csv"))

@st.cache_data
def load_features():
    return joblib.load(os.path.join(BASE_DIR, "features.pkl"))

try:
    model = load_model()
    df = load_data()
    features = load_features()
except Exception as e:
    st.error(f"Unable to load the project files: {e}")
    st.info("Check that model.pkl, features.pkl and train_merged.csv are in the same folder as app.py.")
    st.stop()

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">🌎 Sustainable food intelligence</div>
    <h1>Eco Plate AI</h1>
    <p>Smarter demand planning. Better food decisions. A greener tomorrow.</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR FILTERS ----------
st.sidebar.markdown("## 🌿 Eco Plate AI")
st.sidebar.caption("YOUR FOOD PLANNING WORKSPACE")
st.sidebar.divider()
st.sidebar.markdown("### 🎛️ Choose your data")

categories = sorted(df["category"].dropna().unique().tolist())
cuisines = sorted(df["cuisine"].dropna().unique().tolist())
centers = sorted(df["center_id"].dropna().unique().tolist())
weeks = sorted(df["week"].dropna().unique().tolist())

category = st.sidebar.selectbox("Food category", categories)
cuisine = st.sidebar.selectbox("Cuisine", cuisines)
center = st.sidebar.selectbox("Food center", centers)
week = st.sidebar.selectbox("Historical week", weeks)

st.sidebar.divider()
st.sidebar.caption("Built to support smarter food preparation 🌱")

# ---------- FILTER DATA ----------
filtered = df[
    (df["category"] == category) &
    (df["cuisine"] == cuisine) &
    (df["center_id"] == center) &
    (df["week"] == week)
].copy()

# ---------- KPI CARDS ----------
st.markdown("### 📈 Your sustainability snapshot")

total_orders = int(filtered["num_orders"].sum()) if not filtered.empty else 0
record_count = len(filtered)
average_orders = filtered["num_orders"].mean() if record_count else 0
average_price = filtered["checkout_price"].mean() if record_count else 0

k1, k2, k3, k4 = st.columns(4)

def metric_card(col, icon, label, value):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

metric_card(k1, "🧾", "Historical orders", f"{total_orders:,}")
metric_card(k2, "🍽️", "Matching records", f"{record_count:,}")
metric_card(k3, "📊", "Average orders", f"{average_orders:,.1f}")
metric_card(k4, "💰", "Average checkout price", f"{average_price:,.2f}")

st.write("")

# ---------- TABS ----------
overview_tab, forecast_tab, planner_tab, data_tab , risk_radar= st.tabs([
    "🌿 Overview", "🔮 Demand Insights", "🍲 Preparation Planner", "📋 Explore Data", "risk radar!"
])

with overview_tab:
    st.markdown("### 📊 Order patterns")
    if filtered.empty:
        st.warning("No records match these filters. Please change your selections.")
    else:
        left, right = st.columns(2)

        with left:
            category_data = (
                df.groupby("category", as_index=False)["num_orders"]
                .sum().sort_values("num_orders", ascending=False)
            )
            fig = px.bar(
                category_data, x="category", y="num_orders",
                title="Orders by food category",
                color="num_orders",
                color_continuous_scale=["#b9ebc9", "#38a878", "#12533d"],
                labels={"category": "Food category", "num_orders": "Orders"}
            )
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_family="DM Sans", title_font_size=17,
                coloraxis_showscale=False, margin=dict(l=10, r=10, t=55, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            weekly = (
                df.groupby("week", as_index=False)["num_orders"]
                .sum().sort_values("week")
            )
            fig = px.area(
                weekly, x="week", y="num_orders",
                title="Historical demand trend",
                markers=True,
                color_discrete_sequence=["#16a085"],
                labels={"week": "Week", "num_orders": "Orders"}
            )
            fig.update_traces(
                fill="tozeroy",
                fillcolor="rgba(22,160,133,0.14)",
                line=dict(width=3)
            )
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_family="DM Sans", title_font_size=17,
                margin=dict(l=10, r=10, t=55, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.caption("These charts summarize the historical dataset, not measured food waste.")

with forecast_tab:
    st.markdown("### 🔮 Model-based demand estimate")
    st.write("Estimate orders for the selected historical records using your trained model.")

    if filtered.empty:
        st.warning("No matching records. Change the sidebar filters.")
    else:
        X = filtered[features].copy()
        predictions = model.predict(X)
        predictions = pd.Series(predictions).clip(lower=0)

        actual_total = int(filtered["num_orders"].sum())
        predicted_total = int(round(predictions.sum()))

        a, b = st.columns(2)
        metric_card(a, "🧾", "Actual historical orders", f"{actual_total:,}")
        metric_card(b, "🤖", "Model estimated orders", f"{predicted_total:,}")

        chart_df = pd.DataFrame({
            "Record": range(1, len(filtered) + 1),
            "Actual orders": filtered["num_orders"].to_numpy(),
            "Predicted orders": predictions.to_numpy()
        }).melt(
            id_vars="Record",
            var_name="Series",
            value_name="Orders"
        )

        fig = px.line(
            chart_df, x="Record", y="Orders", color="Series",
            title="Actual vs predicted orders",
            color_discrete_map={
                "Actual orders": "#1677d2",
                "Predicted orders": "#16a085"
            },
            markers=True
        )
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_size=18,
            legend_title_text="", margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            "Prototype limitation: this view predicts records from the selected historical week. "
            "It is not yet a future-week forecast, and the project does not have measured food-waste data."
        )

with planner_tab:
    st.markdown("### 🍲 Smart preparation planner")
    st.write("Create a preparation estimate from the model output.")

    if filtered.empty:
        st.warning("No matching records. Change the sidebar filters.")
    else:
        predictions = pd.Series(model.predict(filtered[features])).clip(lower=0)
        base_demand = max(0, int(round(predictions.sum())))

        col1, col2 = st.columns([1, 1])

        with col1:
            buffer_pct = st.slider("Preparation buffer (%)", 0, 30, 10)
            stock = st.number_input(
                "Usable meals already available",
                min_value=0, value=0, step=10
            )

        planned_total = int(round(base_demand * (1 + buffer_pct / 100)))
        additional = max(0, planned_total - int(stock))
        surplus_risk = max(0, int(stock) - planned_total)

        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Preparation recommendation")
            st.metric("Estimated demand", f"{base_demand:,} meals")
            st.metric("Planned total including buffer", f"{planned_total:,} meals")
            st.metric("Additional meals to prepare", f"{additional:,} meals")
            st.metric("Stock above planned quantity", f"{surplus_risk:,} meals")
            st.markdown('</div>', unsafe_allow_html=True)

        st.caption(
            "This is a planning aid, not a measured waste prediction. "
            "Review shelf life, existing inventory and food safety before preparing meals."
        )

with data_tab:
    st.markdown("### 📋 Historical data explorer")
    st.write(f"Showing up to 200 rows from {len(df):,} records.")
    st.dataframe(
        df[[
            "week", "center_id", "category", "cuisine",
            "checkout_price", "num_orders"
        ]].head(200),
        use_container_width=True,
        hide_index=True
    )

    csv = df.head(200).to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download sample data (CSV)",
        data=csv,
        file_name="eco_plate_sample.csv",
        mime="text/csv"
    )

st.markdown("""
<div class="footer">
    🌱 <b>Eco Plate AI</b> · Smarter food planning for a more sustainable future<br>
    <small>Hackathon prototype · Predictions are estimates, not guarantees of reduced waste.</small>
</div>
""", unsafe_allow_html=True)

with risk_radar:
    st.markdown("## FOOD WASTE AND STOCK OUT RISK RADAR!!")
    st.write(
        "estimtae potential food waste and stock storages using"
        "the model's demand predictions and your current stock."
        )
    if filtered.empty:
        st.warning(
            "No data matches your current filters"
            "change the filters in the sidebar and try again!"
            )
    else:
        predictions=model.predict(filtered[features])
        estimated_demand=max(
            0, int(round(float(predictions.sum())))
            )
        col1, col2 = st.columns(2)

        with col1:
            preparation_buffer = st.slider(
                "Extra preparation buffer (%)",
                min_value=0,
                max_value=30,
                value=10,
                step=5,
                key="radar_buffer"
            )

        with col2:
            available_stock = st.number_input(
                "Current usable stock (portions)",
                min_value=0,
                value=0,
                step=10,
                key="radar_stock"
            )

        # Calculate suggested preparation.
        planned_preparation = int(
            round(
                estimated_demand
                * (1 + preparation_buffer / 100)
            )
        )

        # Rule-based risk indicators, not probabilities.
        waste_risk = int(
            round(
                max(planned_preparation - estimated_demand, 0)
                / max(planned_preparation, 1)
                * 100
            )
        )

        stockout_risk = int(
            round(
                max(estimated_demand - available_stock, 0)
                / max(estimated_demand, 1)
                * 100
            )
        )

        surplus_risk = int(
            round(
                max(available_stock - estimated_demand, 0)
                / max(available_stock, 1)
                * 100
            )
        )

        demand_gap = int(
            round(
                max(estimated_demand - available_stock, 0)
                / max(estimated_demand, 1)
                * 100
            )
        )

        # Display important values.
        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Estimated demand",
            f"{estimated_demand:,} portions"
        )

        metric2.metric(
            "Suggested preparation",
            f"{planned_preparation:,} portions"
        )

        metric3.metric(
            "Current stock",
            f"{available_stock:,} portions"
        )

        # Create interactive radar chart.
        categories = [
            "Waste risk",
            "Stock-out risk",
            "Surplus stock",
            "Demand gap"
        ]

        scores = [
            waste_risk,
            stockout_risk,
            surplus_risk,
            demand_gap
        ]

        radar_fig = go.Figure()

        radar_fig.add_trace(
            go.Scatterpolar(
                r=scores + [scores[0]],
                theta=categories + [categories[0]],
                fill="toself",
                name="Risk indicators",
                line=dict(
                    color="#159570",
                    width=3
                ),
                fillcolor="rgba(21,149,112,0.25)",
                hovertemplate=(
                    "%{theta}: %{r}/100"
                    "<extra></extra>"
                )
            )
        )

        radar_fig.update_layout(
            title="Live Food Risk Indicators",
            polar=dict(
                bgcolor="rgba(255,255,255,0.8)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    ticksuffix="/100"
                )
            ),
            showlegend=False,
            height=480,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            radar_fig,
            use_container_width=True
        )

        # Warning levels.
        st.markdown("### Risk warnings")

        if stockout_risk >= 60:
            st.error(
                "🔴 HIGH STOCK-OUT RISK: Available stock is "
                "well below estimated demand. Consider preparing "
                "additional portions."
            )
        elif stockout_risk >= 30:
            st.warning(
                "🟠 MEDIUM STOCK-OUT RISK: Review stock levels "
                "and consider preparing more."
            )
        else:
            st.success(
                "🟢 LOW STOCK-OUT RISK: Current stock covers "
                "most or all of the estimated demand."
            )

        if waste_risk >= 30 or surplus_risk >= 30:
            st.warning(
                "⚠️ Potential surplus detected. Review your "
                "preparation buffer and stock before preparing more."
            )
        else:
            st.info(
                "No major surplus signal from these simplified indicators."
            )

        st.caption(
            "These are rule-based planning indicators, not calibrated "
            "probabilities. Total demand is calculated from the records "
            "currently selected by your dashboard filters."
        )

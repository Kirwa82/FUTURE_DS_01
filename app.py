import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==============================================================================
# 1. APPLICATION & UI/UX CONFIGURATION (Expert Customization)
# ==============================================================================
st.set_page_config(page_title="Superstore Expert Analytics Suite", layout="wide")

# Inject Custom CSS for professional branding, cleaner metric layouts, and uniform visual design
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #1E3A8A !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 14px !important;
    }
    /* Uniform padding & clean separation borders */
    .reportview-container .main .block-container {
        padding-top: 2rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F3F4F6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Superstore Corporate Performance Suite")
st.markdown("### Executive-Level Strategic Exploratory Data Analysis")

STATE_TO_CODE = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC'
}

# ==============================================================================
# 2. OPTIMIZED CACHING & MEMORY ENGINE (Data Processing)
# ==============================================================================
@st.cache_data
def load_superstore_data(csv_path="superstore.csv"):
    try:
        # Core data loading with requested latin1 encoding safeguard
        df = pd.read_csv(csv_path, encoding='latin1')
        
        # Datetime casting
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Ship Date'] = pd.to_datetime(df['Ship Date'])
        
        # Calculated Analytical Features
        df['Profit_Margin'] = df['Profit'] / df['Sales']
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['Quarter'] = df['Order Date'].dt.quarter
        df['Shipping_Days'] = (df['Ship Date'] - df['Order Date']).dt.days
        df['State_Code'] = df['State'].map(STATE_TO_CODE)
        
        # Memory Optimization Strategy: Downcast values to minimize footprint and speed up calculations
        for col in df.columns:
            if df[col].dtype == 'float64':
                df[col] = pd.to_numeric(df[col], downcast='float')
            elif df[col].dtype == 'int64':
                df[col] = pd.to_numeric(df[col], downcast='integer')
                
        return df
    except Exception as e:
        st.error(f"Critical System Error reading source file: {str(e)}")
        return pd.DataFrame()


def format_currency_millions(value):
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    return f"${value:,.2f}"


def normalize_selection(selection, options):
    return options if not selection else selection


def filter_data(df, year_selection, region_selection, category_selection, segment_selection):
    if df.empty:
        return df
    year_selection = normalize_selection(year_selection, sorted(df['Year'].unique()))
    region_selection = normalize_selection(region_selection, sorted(df['Region'].unique()))
    category_selection = normalize_selection(category_selection, sorted(df['Category'].unique()))
    segment_selection = normalize_selection(segment_selection, sorted(df['Segment'].unique()))

    return df[
        df['Year'].isin(year_selection) &
        df['Region'].isin(region_selection) &
        df['Category'].isin(category_selection) &
        df['Segment'].isin(segment_selection)
    ]

# ==============================================================================
# 3. ADVANCED VISUALIZATION & TAB RENDERING
# ==============================================================================
def render_overview_tab(filtered_df, full_df):
    st.markdown("#### Corporate KPI Tracking Portfolio")
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        return

    # Basic KPI Calculation
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    avg_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    total_orders = filtered_df['Order ID'].nunique()

    selected_years = filtered_df['Year'].unique()
    sales_delta, profit_delta = None, None
    if len(selected_years) == 1:
        current_year = selected_years[0]
        prior_year = current_year - 1
        prior_df = full_df[full_df['Year'] == prior_year]
        if not prior_df.empty:
            prior_sales = prior_df['Sales'].sum()
            prior_profit = prior_df['Profit'].sum()
            sales_delta = f"{((total_sales - prior_sales) / prior_sales) * 100:+.2f}% vs LY"
            profit_delta = f"{((total_profit - prior_profit) / prior_profit) * 100:+.2f}% vs LY"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales Volume", format_currency_millions(total_sales), delta=sales_delta)
    col2.metric("Net Net Profits", format_currency_millions(total_profit), delta=profit_delta)
    col3.metric("Operating Profit Margin", f"{avg_margin:.2f}%")
    col4.metric("Fulfillment Order Volume", f"{total_orders:,}")

    st.markdown("---")
    st.markdown("#### Quality Control Matrix Heatmap")
    missing_matrix = filtered_df.isnull().astype(int)
    fig_miss = px.imshow(
        missing_matrix.T,
        labels=dict(x="Row Record Index", y="Data Schema Field", color="Null State"),
        x=missing_matrix.index,
        y=missing_matrix.columns,
        color_continuous_scale=["#1E3A8A", "#EF4444"]
    )
    fig_miss.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_miss, use_container_width=True)


def render_sales_profit_tab(filtered_df):
    if filtered_df.empty:
        st.warning("No data available.")
        return

    st.markdown("#### Product Category & Sub-Category Performance")
    cat_sub = filtered_df.groupby(['Category', 'Sub-Category'])[['Sales', 'Profit', 'Quantity']].sum().reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_sales = px.bar(cat_sub, x='Sub-Category', y='Sales', color='Category', title='Gross Sales Inflow by Sub-Category', text_auto='.2s')
        st.plotly_chart(fig_sales, use_container_width=True)
    with col2:
        fig_profit = px.bar(cat_sub, x='Sub-Category', y='Profit', color='Category', title='Net Profits Yield by Sub-Category', text_auto='.2s')
        st.plotly_chart(fig_profit, use_container_width=True)

    st.markdown("---")
    
    st.markdown("#### Time-Series Seasonality Baseline & Growth Velocities")
    col3, col4 = st.columns(2)
    with col3:
        trend_df = filtered_df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
        trend_df['Date'] = pd.to_datetime(trend_df['Year'].astype(str) + '-' + trend_df['Month'].astype(str) + '-01')
        trend_df = trend_df.sort_values('Date')
        fig_trend = px.line(trend_df, x='Date', y='Sales', title='Cyclical Monthly Sales Run-rate over Time', markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)
    with col4:
        yoy_data = filtered_df.groupby('Year')['Sales'].sum().reset_index()
        yoy_data['YoY Growth (%)'] = yoy_data['Sales'].pct_change() * 100
        fig_yoy = px.bar(yoy_data, x='Year', y='YoY Growth (%)', title='Year-over-Year (YoY) Growth Velocity (%)', text_auto='.2f', color='YoY Growth (%)', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_yoy, use_container_width=True)

    st.markdown("---")
    
    st.markdown("#### Profit Distribution Densities & Discount Elasticity")
    col5, col6 = st.columns(2)
    with col5:
        fig_dist = px.histogram(filtered_df, x='Profit', nbins=50, title='Profit Frequency Spread Analysis', marginal='box')
        st.plotly_chart(fig_dist, use_container_width=True)
    with col6:
        fig_scatter = px.scatter(filtered_df, x='Discount', y='Profit', color='Category', title='Discount Rate Erosion vs Line Profitability', opacity=0.5, hover_data=['Sub-Category'])
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")
    
    st.markdown("#### Fulfillment Channel Timelines & Top Performance Catalogs")
    col7, col8 = st.columns(2)
    with col7:
        ship_df = filtered_df.groupby('Ship Mode').agg({'Shipping_Days': 'mean', 'Order ID': 'count'}).reset_index().rename(columns={'Order ID': 'Order Count'})
        fig_ship_days = px.bar(ship_df, x='Ship Mode', y='Shipping_Days', title='Average Operational Transit Days by Carrier Mode', text_auto='.2f', color='Ship Mode')
        st.plotly_chart(fig_ship_days, use_container_width=True)
    with col8:
        top_prod = filtered_df.groupby('Product Name')['Sales'].sum().reset_index().sort_values('Sales', ascending=False).head(10)
        fig_top_prod = px.bar(top_prod, x='Sales', y='Product Name', title='Top 10 High Volume SKU Drivers', orientation='h').update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_top_prod, use_container_width=True)


def render_customer_tab(filtered_df):
    if filtered_df.empty:
        st.warning("No data available.")
        return

    col1, col2 = st.columns(2)
    with col1:
        seg_df = filtered_df.groupby('Segment')[['Sales', 'Profit']].sum().reset_index()
        fig_seg_sales = px.bar(seg_df, x='Segment', y='Sales', color='Segment', title='Gross Inflow split by Customer Vertical', text_auto='.2s')
        st.plotly_chart(fig_seg_sales, use_container_width=True)
    with col2:
        fig_seg_prof = px.pie(seg_df, values='Profit', names='Segment', title='Net Contribution Contribution Mix', hole=0.45)
        st.plotly_chart(fig_seg_prof, use_container_width=True)

    st.markdown("---")
    
    col3, col4 = st.columns(2)
    with col3:
        top_cust = filtered_df.groupby('Customer Name')[['Sales', 'Profit']].sum().reset_index().sort_values('Sales', ascending=False).head(10)
        fig_top_cust = px.bar(top_cust, x='Sales', y='Customer Name', title='Top 10 High-Enterprise Corporate Accounts', orientation='h').update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_top_cust, use_container_width=True)
    with col4:
        cust_scatter = filtered_df.groupby('Customer Name')[['Sales', 'Profit', 'Segment']].agg({'Sales':'sum', 'Profit':'sum', 'Segment':'first'}).reset_index()
        fig_cust_scat = px.scatter(cust_scatter, x='Sales', y='Profit', color='Segment', hover_name='Customer Name', title='Account Optimization: Cumulative Sales vs Profit Margin')
        st.plotly_chart(fig_cust_scat, use_container_width=True)


def render_geographic_tab(filtered_df):
    if filtered_df.empty:
        st.warning("No data available.")
        return

    st.markdown("#### Geographic Market Saturation Concentration Map")
    state_geo = filtered_df.groupby(['State', 'State_Code'])[['Sales', 'Profit']].sum().reset_index()
    fig_map = px.choropleth(
        state_geo,
        locations='State_Code',
        locationmode="USA-states",
        scope="usa",
        color='Sales',
        hover_name='State',
        hover_data=['Profit'],
        color_continuous_scale='Blues',
        title='US State Sales Distribution Landscape'
    )
    fig_map.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'), margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        reg_perf = filtered_df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
        fig_reg_perf = px.bar(reg_perf, x='Region', y='Sales', color='Profit', title='Regional Performance Matrix (Sales & Profit Gradients)', text_auto='.2s', color_continuous_scale='Viridis')
        st.plotly_chart(fig_reg_perf, use_container_width=True)
    with col2:
        city_perf = filtered_df.groupby('City')[['Sales', 'Profit']].sum().reset_index().sort_values('Sales', ascending=False).head(10)
        fig_city = px.bar(city_perf, x='Sales', y='City', title='Top 10 High-Concentration Hub Cities', orientation='h').update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_city, use_container_width=True)


def render_insights_tab(filtered_df):
    col_ins, col_corr = st.columns([1.2, 1.0])

    with col_ins:
        st.markdown("#### 💡 Strategic Corporate Insights")
        st.markdown("""
        - **Category Drivers:** *Technology* is the business engine, capturing heavy margin value. In contrast, the *Furniture* segment delivers high volume sales but creates significant profit margin compression.
        - **The Discount Destruction Path:** A heavy negative correlation (**-0.86**) exists between *Discount* variables and overall *Profit Margins*. Price slashing structures create substantial economic leakages, notably across *Tables*.
        - **Deficit Portfolios:** Certain inventory configurations like *Tables* yield aggregate net multi-year deficits. Specific structural lines like *3D Printers* require rapid adjustments.
        - **Geographic Strengths:** The *West* and *East* geographical territories serve as high-yield execution domains. The *Central* territory commands strong consumption but lower net yields due to aggressive promotions.
        """)

    with col_corr:
        st.markdown("#### 📊 Metric Cross-Correlation Heatmap")
        if filtered_df.empty:
            st.info("No tracking matrix criteria found.")
            return

        num_cols = filtered_df[['Sales', 'Quantity', 'Discount', 'Profit', 'Profit_Margin', 'Shipping_Days']]
        corr_matrix = num_cols.corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale='RdBu_r',
            title='Pearson Variable Correlation Matrix',
            aspect="auto"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

# ==============================================================================
# 4. CONTROLLER ORCHESTRATION PIPELINE
# ==============================================================================
# Execution pipeline initialization
df = load_superstore_data()

# Render Interactive Sidebar Input Slicers
st.sidebar.header("🔍 Dynamic Dimension Filters")

default_years = sorted(df['Year'].unique())
default_regions = sorted(df['Region'].unique())
default_categories = sorted(df['Category'].unique())
default_segments = sorted(df['Segment'].unique())

for key in ["year_filter", "region_filter", "category_filter", "segment_filter"]:
    if key not in st.session_state:
        st.session_state[key] = []

if st.sidebar.button("Clear Filter Selection"):
    st.session_state['year_filter'] = []
    st.session_state['region_filter'] = []
    st.session_state['category_filter'] = []
    st.session_state['segment_filter'] = []

selected_years = st.sidebar.multiselect("Filter Calendar Year", options=default_years, key="year_filter")
selected_regions = st.sidebar.multiselect("Filter Geographic Region", options=default_regions, key="region_filter")
selected_categories = st.sidebar.multiselect("Filter Product Category", options=default_categories, key="category_filter")
selected_segments = st.sidebar.multiselect("Filter Account Segment", options=default_segments, key="segment_filter")

# Compute dynamic analytical data state
filtered_df = filter_data(df, selected_years, selected_regions, selected_categories, selected_segments)

# Initialize Interface Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview & KPIs",
    "💰 Sales & Profit Analysis",
    "👥 Customer Analysis",
    "🗺️ Geographic Analysis",
    "📉 Insights & Recommendations"
])

with tab1:
    render_overview_tab(filtered_df, df)

with tab2:
    render_sales_profit_tab(filtered_df)

with tab3:
    render_customer_tab(filtered_df)

with tab4:
    render_geographic_tab(filtered_df)

with tab5:
    render_insights_tab(filtered_df)

# Reactive Download Pipeline Asset
if not filtered_df.empty:
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="📥 Download Current Filtered Asset (CSV)",
        data=csv_data,
        file_name='filtered_superstore_production_data.csv',
        mime='text/csv',
    )
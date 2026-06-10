"""
Bank Customer Retention Analytics Dashboard
Multi-page Streamlit Application
Customer Engagement & Product Utilization Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# ============================================================================
# PAGE CONFIGURATION & THEME
# ============================================================================

st.set_page_config(
    page_title="Bank Retention Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom theme
st.markdown("""
    <style>
        :root {
            --primary-color: #2E86DE;
            --secondary-color: #A23B72;
            --success-color: #06A77D;
            --danger-color: #F74271;
        }
        .metric-card {
            padding: 20px;
            border-radius: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# LOAD DATA & CACHE
# ============================================================================

@st.cache_data
def load_data():
    """Load and prepare dataset"""
    df = pd.read_csv('bank_customer_data.csv')
    return df

@st.cache_data
def load_kpi_summary():
    """Load KPI summary"""
    with open('kpi_summary.json', 'r') as f:
        return json.load(f)

try:
    df = load_data()
    kpi_data = load_kpi_summary()
except FileNotFoundError:
    st.error("⚠️ Data files not found. Please run eda_analysis.py first.")
    st.stop()

# ============================================================================
# SIDEBAR NAVIGATION & FILTERS
# ============================================================================

with st.sidebar:
    st.image("https://via.placeholder.com/200x60?text=Bank+Analytics", use_column_width=True)
    st.title("🏦 Bank Retention Hub")
    
    page = st.radio(
        "📊 Navigation",
        ["🎯 Executive Dashboard", 
         "👥 Engagement Analysis",
         "📦 Product Utilization",
         "⚠️ At-Risk Customers",
         "📈 Retention Insights",
         "🔍 Customer Deep Dive"]
    )
    
    st.markdown("---")
    st.subheader("🔧 Global Filters")
    
    # Filters
    selected_geography = st.multiselect(
        "Geography",
        options=df['Geography'].unique(),
        default=df['Geography'].unique()
    )
    
    selected_age_range = st.slider(
        "Age Range",
        min_value=int(df['Age'].min()),
        max_value=int(df['Age'].max()),
        value=(int(df['Age'].min()), int(df['Age'].max()))
    )
    
    selected_balance_range = st.slider(
        "Balance Range ($)",
        min_value=0,
        max_value=int(df['Balance'].max()),
        value=(0, int(df['Balance'].quantile(0.95))),
        step=10000
    )
    
    # Apply filters
    mask = (
        (df['Geography'].isin(selected_geography)) &
        (df['Age'] >= selected_age_range[0]) &
        (df['Age'] <= selected_age_range[1]) &
        (df['Balance'] >= selected_balance_range[0]) &
        (df['Balance'] <= selected_balance_range[1])
    )
    filtered_df = df[mask].copy()
    
    st.markdown("---")
    st.metric("Filtered Records", len(filtered_df), f"{len(filtered_df)/len(df)*100:.1f}% of total")

# ============================================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ============================================================================

if page == "🎯 Executive Dashboard":
    st.title("🎯 Executive Dashboard - Key Insights at a Glance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Customers",
            f"{len(filtered_df):,}",
            f"{len(filtered_df)/len(df)*100:.1f}% of database"
        )
    
    with col2:
        churn_rate = (filtered_df['Exited'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric(
            "Overall Churn Rate",
            f"{churn_rate:.1f}%",
            f"{filtered_df['Exited'].sum():.0f} customers churned"
        )
    
    with col3:
        retention_rate = 100 - churn_rate
        st.metric(
            "Retention Rate",
            f"{retention_rate:.1f}%",
            "Active relationships"
        )
    
    with col4:
        total_balance = filtered_df['Balance'].sum()
        st.metric(
            "Total Balance AUM",
            f"${total_balance/1e6:.1f}M",
            f"Average: ${filtered_df['Balance'].mean():,.0f}"
        )
    
    st.markdown("---")
    
    # Main KPI Row
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.metric(
            "🔗 Engagement Ratio",
            f"{kpi_data['engagement_retention_ratio']:.2f}x",
            "Active vs Inactive"
        )
    
    with kpi_col2:
        st.metric(
            "📦 Product Depth Index",
            f"{kpi_data['product_depth_index']:.2f}x",
            "Multi vs Single"
        )
    
    with kpi_col3:
        st.metric(
            "💳 CC Stickiness Score",
            f"{kpi_data['cc_stickiness_score']:.2f}x",
            "With vs Without"
        )
    
    with kpi_col4:
        st.metric(
            "⚠️ At-Risk Premium",
            f"{kpi_data['at_risk_premium_count']:.0f}",
            f"{kpi_data['at_risk_premium_churn_rate']*100:.1f}% churn"
        )
    
    with kpi_col5:
        rsi_gap = kpi_data['avg_relationship_strength_retained'] - kpi_data['avg_relationship_strength_churned']
        st.metric(
            "💪 RSI Gap",
            f"{rsi_gap:.1f}pts",
            "Retained vs Churned"
        )
    
    st.markdown("---")
    
    # Charts Row 1
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("📊 Churn Distribution by Engagement Status")
        engagement_data = filtered_df.groupby('IsActiveMember')['Exited'].agg(['count', 'sum', 'mean'])
        engagement_data.index = ['Inactive', 'Active']
        
        fig_engagement = px.bar(
            x=engagement_data.index,
            y=engagement_data['mean'] * 100,
            title="Churn Rate by Engagement",
            labels={'y': 'Churn Rate (%)', 'x': 'Member Status'},
            color=['#F74271', '#06A77D'],
            text_auto='.1f'
        )
        fig_engagement.update_traces(textposition='outside')
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    with chart_col2:
        st.subheader("📦 Product Impact on Retention")
        product_data = filtered_df.groupby('NumOfProducts')['Exited'].agg(['count', 'sum', 'mean'])
        
        fig_product = px.bar(
            x=product_data.index,
            y=(1 - product_data['mean']) * 100,
            title="Retention Rate by Product Count",
            labels={'y': 'Retention Rate (%)', 'x': 'Number of Products'},
            color=['#2E86DE', '#A23B72', '#06A77D', '#F74271'],
            text_auto='.1f'
        )
        fig_product.update_traces(textposition='outside')
        st.plotly_chart(fig_product, use_container_width=True)
    
    # Charts Row 2
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.subheader("🌍 Churn Rate by Geography")
        geo_data = filtered_df.groupby('Geography')['Exited'].agg(['count', 'sum', 'mean'])
        
        fig_geo = px.pie(
            values=geo_data['count'],
            names=geo_data.index,
            title="Customer Distribution by Country",
            hole=0.3
        )
        st.plotly_chart(fig_geo, use_container_width=True)
    
    with chart_col4:
        st.subheader("💳 Credit Card Effect")
        cc_data = filtered_df.groupby('HasCrCard')['Exited'].agg(['count', 'sum', 'mean'])
        cc_data.index = ['No Credit Card', 'Has Credit Card']
        
        fig_cc = px.bar(
            x=cc_data.index,
            y=cc_data['mean'] * 100,
            title="Churn Rate by Credit Card Status",
            labels={'y': 'Churn Rate (%)', 'x': 'Credit Card Status'},
            color=['#F74271', '#06A77D'],
            text_auto='.1f'
        )
        fig_cc.update_traces(textposition='outside')
        st.plotly_chart(fig_cc, use_container_width=True)

# ============================================================================
# PAGE 2: ENGAGEMENT ANALYSIS
# ============================================================================

elif page == "👥 Engagement Analysis":
    st.title("👥 Customer Engagement & Segmentation Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        active_count = (filtered_df['IsActiveMember'] == 1).sum()
        st.metric("Active Members", f"{active_count:,}", f"{active_count/len(filtered_df)*100:.1f}%")
    
    with col2:
        inactive_count = (filtered_df['IsActiveMember'] == 0).sum()
        st.metric("Inactive Members", f"{inactive_count:,}", f"{inactive_count/len(filtered_df)*100:.1f}%")
    
    with col3:
        active_churn = filtered_df[filtered_df['IsActiveMember'] == 1]['Exited'].mean() * 100
        inactive_churn = filtered_df[filtered_df['IsActiveMember'] == 0]['Exited'].mean() * 100
        ratio = inactive_churn / (active_churn + 0.01)
        st.metric("Churn Risk Ratio", f"{ratio:.1f}x", "Inactive vs Active")
    
    st.markdown("---")
    
    # Engagement Profiles
    st.subheader("🎯 Engagement Profiles Distribution")
    
    engagement_profile_data = filtered_df['EngagementProfile'].value_counts()
    profile_churn = filtered_df.groupby('EngagementProfile')['Exited'].agg(['count', 'sum', 'mean'])
    
    profile_col1, profile_col2 = st.columns(2)
    
    with profile_col1:
        fig_profile_dist = px.pie(
            values=engagement_profile_data.values,
            names=engagement_profile_data.index,
            title="Customer Segment Distribution",
            color_discrete_sequence=['#2E86DE', '#A23B72', '#06A77D', '#F74271']
        )
        st.plotly_chart(fig_profile_dist, use_container_width=True)
    
    with profile_col2:
        profile_churn_pct = profile_churn['mean'] * 100
        fig_profile_churn = px.bar(
            x=profile_churn_pct.index,
            y=profile_churn_pct.values,
            title="Churn Rate by Engagement Profile",
            labels={'y': 'Churn Rate (%)', 'x': 'Profile'},
            text_auto='.1f',
            color=profile_churn_pct.values,
            color_continuous_scale='RdYlGn_r'
        )
        fig_profile_churn.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_profile_churn, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Profile Analysis Table
    st.subheader("📋 Detailed Engagement Profile Analysis")
    
    profile_summary = filtered_df.groupby('EngagementProfile').agg({
        'CustomerId': 'count',
        'Exited': ['sum', 'mean'],
        'Balance': 'mean',
        'Age': 'mean',
        'Tenure': 'mean',
        'NumOfProducts': 'mean',
        'RelationshipStrengthIndex': 'mean'
    }).round(2)
    
    profile_summary.columns = ['Total Customers', 'Churned', 'Churn Rate', 'Avg Balance', 
                               'Avg Age', 'Avg Tenure', 'Avg Products', 'Avg RSI']
    profile_summary['Churn Rate'] = (profile_summary['Churn Rate'] * 100).round(2).astype(str) + '%'
    profile_summary['Avg Balance'] = '$' + (profile_summary['Avg Balance']/1000).round(0).astype(int).astype(str) + 'K'
    
    st.dataframe(profile_summary, use_container_width=True)
    
    # Behavioral Heatmap
    st.subheader("🔥 Age vs Tenure: Engagement Heatmap")
    
    heatmap_data = filtered_df.pivot_table(
        values='Exited',
        index=pd.cut(filtered_df['Age'], bins=5),
        columns=pd.cut(filtered_df['Tenure'], bins=5),
        aggfunc='mean'
    ) * 100
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns.astype(str),
        y=heatmap_data.index.astype(str),
        colorscale='RdYlGn_r',
        text=np.round(heatmap_data.values, 1),
        texttemplate='%{text:.1f}%',
        textfont={"size": 10},
        colorbar=dict(title='Churn Rate (%)')
    ))
    
    fig_heatmap.update_layout(
        title="Churn Rate Heatmap: Age vs Tenure",
        xaxis_title="Tenure Range (Years)",
        yaxis_title="Age Range (Years)",
        height=500
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ============================================================================
# PAGE 3: PRODUCT UTILIZATION
# ============================================================================

elif page == "📦 Product Utilization":
    st.title("📦 Product Utilization & Cross-Sell Strategy")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        single_product = (filtered_df['NumOfProducts'] == 1).sum()
        st.metric("Single Product", f"{single_product:,}", f"{single_product/len(filtered_df)*100:.1f}%")
    
    with col2:
        multi_product = (filtered_df['NumOfProducts'] > 1).sum()
        st.metric("Multi-Product", f"{multi_product:,}", f"{multi_product/len(filtered_df)*100:.1f}%")
    
    with col3:
        single_churn = filtered_df[filtered_df['NumOfProducts'] == 1]['Exited'].mean() * 100
        st.metric("Single Churn Rate", f"{single_churn:.1f}%", "Risk Level")
    
    with col4:
        multi_churn = filtered_df[filtered_df['NumOfProducts'] > 1]['Exited'].mean() * 100
        st.metric("Multi Churn Rate", f"{multi_churn:.1f}%", "Lower Risk")
    
    st.markdown("---")
    
    # Product Analysis Charts
    prod_col1, prod_col2 = st.columns(2)
    
    with prod_col1:
        st.subheader("📊 Product Count Distribution")
        product_dist = filtered_df['NumOfProducts'].value_counts().sort_index()
        
        fig_prod_dist = px.bar(
            x=product_dist.index,
            y=product_dist.values,
            title="Number of Products per Customer",
            labels={'x': 'Number of Products', 'y': 'Customer Count'},
            text_auto=True,
            color=product_dist.values,
            color_continuous_scale='Blues'
        )
        fig_prod_dist.update_layout(showlegend=False)
        st.plotly_chart(fig_prod_dist, use_container_width=True)
    
    with prod_col2:
        st.subheader("💾 Retention by Product Count")
        product_retention = filtered_df.groupby('NumOfProducts')['Exited'].apply(
            lambda x: ((1 - x.mean()) * 100)
        )
        
        fig_prod_ret = px.line(
            x=product_retention.index,
            y=product_retention.values,
            markers=True,
            title="Retention Improvement with Products",
            labels={'x': 'Number of Products', 'y': 'Retention Rate (%)'},
            line_shape='spline'
        )
        fig_prod_ret.update_traces(marker=dict(size=10), line=dict(width=3))
        st.plotly_chart(fig_prod_ret, use_container_width=True)
    
    st.markdown("---")
    
    # Cross-sell Opportunity Analysis
    st.subheader("🎯 Cross-Sell Opportunity Matrix")
    
    single_inactive = filtered_df[
        (filtered_df['NumOfProducts'] == 1) & 
        (filtered_df['IsActiveMember'] == 0)
    ]
    single_active = filtered_df[
        (filtered_df['NumOfProducts'] == 1) & 
        (filtered_df['IsActiveMember'] == 1)
    ]
    
    opportunity_col1, opportunity_col2 = st.columns(2)
    
    with opportunity_col1:
        st.metric(
            "Single-Product Inactive",
            f"{len(single_inactive):,}",
            f"{len(single_inactive)/len(filtered_df)*100:.1f}% - Highest Priority"
        )
        st.write(f"**Churn Rate:** {single_inactive['Exited'].mean()*100:.1f}%")
        st.write(f"**Avg Balance:** ${single_inactive['Balance'].mean():,.0f}")
    
    with opportunity_col2:
        st.metric(
            "Single-Product Active",
            f"{len(single_active):,}",
            f"{len(single_active)/len(filtered_df)*100:.1f}% - Medium Priority"
        )
        st.write(f"**Churn Rate:** {single_active['Exited'].mean()*100:.1f}%")
        st.write(f"**Avg Balance:** ${single_active['Balance'].mean():,.0f}")
    
    st.markdown("---")
    
    # Product Mix Analysis
    st.subheader("🧮 Detailed Product Utilization Analysis")
    
    product_analysis = filtered_df.groupby('NumOfProducts').agg({
        'CustomerId': 'count',
        'Exited': ['sum', 'mean'],
        'Balance': ['mean', 'sum'],
        'Age': 'mean',
        'HasCrCard': 'mean',
        'IsActiveMember': 'mean'
    }).round(2)
    
    product_analysis.columns = ['Total Customers', 'Churned', 'Churn Rate', 
                                'Avg Balance', 'Total Balance', 'Avg Age', 'CC %', 'Active %']
    product_analysis['Churn Rate'] = (product_analysis['Churn Rate'] * 100).round(1).astype(str) + '%'
    product_analysis['CC %'] = (product_analysis['CC %'] * 100).round(1).astype(str) + '%'
    product_analysis['Active %'] = (product_analysis['Active %'] * 100).round(1).astype(str) + '%'
    
    st.dataframe(product_analysis, use_container_width=True)

# ============================================================================
# PAGE 4: AT-RISK CUSTOMERS
# ============================================================================

elif page == "⚠️ At-Risk Customers":
    st.title("⚠️ At-Risk Premium Customer Detection & Intervention")
    
    balance_75th = filtered_df['Balance'].quantile(0.75)
    at_risk = filtered_df[
        (filtered_df['Balance'] > balance_75th) & 
        (filtered_df['IsActiveMember'] == 0)
    ]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("At-Risk Premium Customers", f"{len(at_risk):,}", 
                 f"{len(at_risk)/len(filtered_df)*100:.1f}% of total")
    
    with col2:
        at_risk_churn = at_risk['Exited'].mean() * 100
        st.metric("Churn Rate", f"{at_risk_churn:.1f}%", 
                 f"{at_risk['Exited'].sum():.0f} already churned")
    
    with col3:
        at_risk_aum = at_risk['Balance'].sum()
        st.metric("AUM at Risk", f"${at_risk_aum/1e6:.1f}M", 
                 f"Avg: ${at_risk['Balance'].mean():,.0f}")
    
    with col4:
        risk_multiplier = at_risk_churn / (filtered_df['Exited'].mean() * 100)
        st.metric("Risk Multiplier", f"{risk_multiplier:.1f}x", 
                 f"vs Overall Average")
    
    st.markdown("---")
    
    # Detailed At-Risk Analysis
    risk_col1, risk_col2 = st.columns(2)
    
    with risk_col1:
        st.subheader("🚨 At-Risk Customers - Churn Status")
        at_risk_status = at_risk['Exited'].value_counts()
        
        fig_at_risk = px.pie(
            values=at_risk_status.values,
            names=['Retained', 'Churned'],
            title="At-Risk Premium: Retention vs Churn",
            color_discrete_map={'Retained': '#06A77D', 'Churned': '#F74271'},
            hole=0.4
        )
        st.plotly_chart(fig_at_risk, use_container_width=True)
    
    with risk_col2:
        st.subheader("💰 Balance Distribution - At-Risk vs Others")
        
        fig_balance_dist = go.Figure()
        
        fig_balance_dist.add_trace(go.Box(
            y=at_risk['Balance'],
            name='At-Risk Premium',
            marker_color='#F74271'
        ))
        
        other_customers = filtered_df[
            ~filtered_df['CustomerId'].isin(at_risk['CustomerId'])
        ]
        fig_balance_dist.add_trace(go.Box(
            y=other_customers['Balance'],
            name='Other Customers',
            marker_color='#2E86DE'
        ))
        
        fig_balance_dist.update_layout(
            title="Balance Distribution Comparison",
            yaxis_title="Balance ($)",
            height=400
        )
        st.plotly_chart(fig_balance_dist, use_container_width=True)
    
    st.markdown("---")
    
    # At-Risk Customer Segmentation
    st.subheader("🎯 At-Risk Customer Segmentation by Profile")
    
    at_risk_profile = at_risk.groupby('StickyProfile').agg({
        'CustomerId': 'count',
        'Exited': ['sum', 'mean'],
        'Balance': 'mean',
        'Age': 'mean',
        'Tenure': 'mean'
    })
    
    at_risk_profile.columns = ['Count', 'Churned', 'Churn Rate', 'Avg Balance', 'Avg Age', 'Avg Tenure']
    at_risk_profile['Churn Rate'] = (at_risk_profile['Churn Rate'] * 100).round(1).astype(str) + '%'
    at_risk_profile['Avg Balance'] = '$' + (at_risk_profile['Avg Balance']/1000).round(0).astype(int).astype(str) + 'K'
    
    st.dataframe(at_risk_profile, use_container_width=True)
    
    # Intervention Strategy
    st.markdown("---")
    st.subheader("💡 Recommended Intervention Strategies")
    
    intervention_col1, intervention_col2, intervention_col3 = st.columns(3)
    
    with intervention_col1:
        st.success("✅ **High Priority: Activate Inactive**")
        st.write(f"Target {len(at_risk)} premium customers with:")
        st.write("- Personalized engagement campaigns")
        st.write("- Premium product recommendations")
        st.write("- Dedicated relationship manager")
    
    with intervention_col2:
        st.warning("⚠️ **Medium Priority: Cross-Sell**")
        st.write("Offer complementary products:")
        st.write("- Investment products for high balance")
        st.write("- Premium banking features")
        st.write("- Exclusive credit card benefits")
    
    with intervention_col3:
        st.info("ℹ️ **Monitor & Report**")
        st.write("Track intervention results:")
        st.write("- Activation rate KPI")
        st.write("- Product adoption rate")
        st.write("- Churn reduction metrics")

# ============================================================================
# PAGE 5: RETENTION INSIGHTS
# ============================================================================

elif page == "📈 Retention Insights":
    st.title("📈 Retention Drivers & Predictive Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        retained = filtered_df[filtered_df['Exited'] == 0]
        avg_rsi_retained = retained['RelationshipStrengthIndex'].mean()
        st.metric("Avg RSI (Retained)", f"{avg_rsi_retained:.1f}/100", 
                 f"{len(retained):,} customers")
    
    with col2:
        churned = filtered_df[filtered_df['Exited'] == 1]
        avg_rsi_churned = churned['RelationshipStrengthIndex'].mean()
        st.metric("Avg RSI (Churned)", f"{avg_rsi_churned:.1f}/100", 
                 f"{len(churned):,} customers")
    
    with col3:
        rsi_gap = avg_rsi_retained - avg_rsi_churned
        st.metric("RSI Difference", f"{rsi_gap:.1f} points", 
                 f"{(rsi_gap/avg_rsi_churned)*100:.0f}% higher for retained")
    
    st.markdown("---")
    
    # RSI Distribution
    st.subheader("💪 Relationship Strength Index Distribution")
    
    fig_rsi = go.Figure()
    
    fig_rsi.add_trace(go.Histogram(
        x=retained['RelationshipStrengthIndex'],
        name='Retained',
        opacity=0.7,
        marker_color='#06A77D'
    ))
    
    fig_rsi.add_trace(go.Histogram(
        x=churned['RelationshipStrengthIndex'],
        name='Churned',
        opacity=0.7,
        marker_color='#F74271'
    ))
    
    fig_rsi.update_layout(
        title="RSI Distribution: Retained vs Churned",
        xaxis_title="Relationship Strength Index",
        yaxis_title="Count",
        barmode='overlay',
        height=400
    )
    st.plotly_chart(fig_rsi, use_container_width=True)
    
    st.markdown("---")
    
    # Retention Drivers Analysis
    st.subheader("🔍 Key Retention Drivers")
    
    driver_col1, driver_col2 = st.columns(2)
    
    with driver_col1:
        st.write("**Engagement Impact**")
        active_retention = (1 - filtered_df[filtered_df['IsActiveMember'] == 1]['Exited'].mean()) * 100
        inactive_retention = (1 - filtered_df[filtered_df['IsActiveMember'] == 0]['Exited'].mean()) * 100
        
        fig_engagement_driver = px.bar(
            x=['Active', 'Inactive'],
            y=[active_retention, inactive_retention],
            title="Engagement Drives 26% Higher Retention",
            labels={'y': 'Retention Rate (%)', 'x': 'Status'},
            text_auto='.1f',
            color=['#06A77D', '#F74271']
        )
        fig_engagement_driver.update_traces(textposition='outside')
        st.plotly_chart(fig_engagement_driver, use_container_width=True)
    
    with driver_col2:
        st.write("**Product Depth Impact**")
        single_retention = (1 - filtered_df[filtered_df['NumOfProducts'] == 1]['Exited'].mean()) * 100
        multi_retention = (1 - filtered_df[filtered_df['NumOfProducts'] >= 2]['Exited'].mean()) * 100
        
        fig_product_driver = px.bar(
            x=['Single Product', 'Multi-Product'],
            y=[single_retention, multi_retention],
            title="Multi-Product Strategy Increases Retention",
            labels={'y': 'Retention Rate (%)', 'x': 'Product Type'},
            text_auto='.1f',
            color=['#F74271', '#06A77D']
        )
        fig_product_driver.update_traces(textposition='outside')
        st.plotly_chart(fig_product_driver, use_container_width=True)
    
    st.markdown("---")
    
    # Sticky Profile Analysis
    st.subheader("⭐ Sticky Customer Profiles")
    
    sticky_analysis = filtered_df.groupby('StickyProfile').agg({
        'CustomerId': 'count',
        'Exited': ['sum', 'mean'],
        'RelationshipStrengthIndex': 'mean',
        'Balance': 'mean',
        'Tenure': 'mean'
    })
    
    sticky_analysis.columns = ['Count', 'Churned', 'Churn Rate', 'Avg RSI', 'Avg Balance', 'Avg Tenure']
    sticky_analysis['Retention %'] = (100 - sticky_analysis['Churn Rate'] * 100).round(1)
    sticky_analysis['Churn Rate'] = (sticky_analysis['Churn Rate'] * 100).round(1).astype(str) + '%'
    sticky_analysis['Avg Balance'] = '$' + (sticky_analysis['Avg Balance']/1000).round(0).astype(int).astype(str) + 'K'
    sticky_analysis = sticky_analysis[['Count', 'Churn Rate', 'Retention %', 'Avg RSI', 'Avg Balance', 'Avg Tenure']]
    
    st.dataframe(sticky_analysis, use_container_width=True)
    
    # Recommendations
    st.markdown("---")
    st.subheader("📋 Strategic Recommendations")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.success("**Priority 1: Engagement Programs**")
        st.write(f"• Activate {(filtered_df['IsActiveMember'] == 0).sum():,} inactive members")
        st.write(f"• Expected impact: {(inactive_retention - active_retention):.1f}% retention improvement")
    
    with rec_col2:
        st.success("**Priority 2: Product Bundling**")
        st.write(f"• Cross-sell to {(filtered_df['NumOfProducts'] == 1).sum():,} single-product customers")
        st.write(f"• Expected impact: {(multi_retention - single_retention):.1f}% retention improvement")

# ============================================================================
# PAGE 6: CUSTOMER DEEP DIVE
# ============================================================================

elif page == "🔍 Customer Deep Dive":
    st.title("🔍 Customer Deep Dive & Profile Analysis")
    
    st.subheader("🔎 Search Customer by ID")
    
    col1, col2 = st.columns(2)
    
    with col1:
        customer_id = st.number_input(
            "Enter Customer ID",
            min_value=1,
            max_value=len(filtered_df),
            value=1
        )
    
    with col2:
        search_customer = filtered_df[filtered_df['CustomerId'] == customer_id]
        if len(search_customer) > 0:
            st.success("✅ Customer Found")
        else:
            st.error("❌ Customer Not Found")
    
    if len(search_customer) > 0:
        cust = search_customer.iloc[0]
        
        st.markdown("---")
        
        # Customer Profile
        profile_col1, profile_col2, profile_col3, profile_col4 = st.columns(4)
        
        with profile_col1:
            st.metric("Customer ID", int(cust['CustomerId']))
            st.metric("Age", int(cust['Age']), "years")
        
        with profile_col2:
            st.metric("Geography", cust['Geography'])
            st.metric("Gender", cust['Gender'])
        
        with profile_col3:
            st.metric("Tenure", int(cust['Tenure']), "years")
            status = "🟢 Active" if cust['IsActiveMember'] == 1 else "🔴 Inactive"
            st.write(f"**Status:** {status}")
        
        with profile_col4:
            churn_status = "🚨 Churned" if cust['Exited'] == 1 else "✅ Retained"
            st.write(f"**Churn Status:** {churn_status}")
        
        st.markdown("---")
        
        # Financial Profile
        st.subheader("💰 Financial Profile")
        
        fin_col1, fin_col2, fin_col3, fin_col4 = st.columns(4)
        
        with fin_col1:
            st.metric("Balance", f"${cust['Balance']:,.0f}")
        
        with fin_col2:
            st.metric("Salary", f"${cust['EstimatedSalary']:,.0f}")
        
        with fin_col3:
            st.metric("Credit Score", int(cust['CreditScore']))
        
        with fin_col4:
            cc_status = "💳 Yes" if cust['HasCrCard'] == 1 else "❌ No"
            st.write(f"**Credit Card:** {cc_status}")
        
        st.markdown("---")
        
        # Product & Engagement
        st.subheader("📦 Product & Engagement Profile")
        
        product_col1, product_col2, product_col3 = st.columns(3)
        
        with product_col1:
            st.metric("Products Held", int(cust['NumOfProducts']))
        
        with product_col2:
            st.metric("Engagement Profile", cust['EngagementProfile'])
        
        with product_col3:
            st.metric("Sticky Profile", cust['StickyProfile'])
        
        st.markdown("---")
        
        # Relationship Strength Index
        st.subheader("💪 Relationship Strength Assessment")
        
        rsi_score = cust['RelationshipStrengthIndex']
        
        fig_rsi_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=rsi_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Relationship Strength Index"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 33], 'color': "#F74271"},
                    {'range': [33, 66], 'color': "#FFB700"},
                    {'range': [66, 100], 'color': "#06A77D"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        st.plotly_chart(fig_rsi_gauge, use_container_width=True)
        
        # Risk Assessment
        st.markdown("---")
        st.subheader("⚠️ Risk Assessment")
        
        risk_factors = []
        
        if cust['IsActiveMember'] == 0:
            risk_factors.append(("🔴 Low Engagement", "Customer is inactive"))
        
        if cust['NumOfProducts'] == 1:
            risk_factors.append(("🟡 Single Product", "Limited product depth"))
        
        if cust['Age'] > 60:
            risk_factors.append(("🟡 Age Factor", "Older customers have higher churn"))
        
        if cust['Tenure'] < 2:
            risk_factors.append(("🟡 Low Tenure", "New customers are at risk"))
        
        if cust['Balance'] < filtered_df['Balance'].quantile(0.25):
            risk_factors.append(("🟢 Low Balance Risk", "Lower AUM exposure"))
        
        if len(risk_factors) == 0:
            st.success("✅ Low Risk Customer - Healthy Profile")
        else:
            for risk_label, risk_desc in risk_factors:
                st.warning(f"{risk_label}: {risk_desc}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888; font-size: 12px;'>
    <p>Bank Customer Retention Analytics Dashboard | Data Source: European Central Bank</p>
    <p>Last Updated: """ + datetime.now().strftime("%B %d, %Y") + """</p>
    </div>
    """, unsafe_allow_html=True)

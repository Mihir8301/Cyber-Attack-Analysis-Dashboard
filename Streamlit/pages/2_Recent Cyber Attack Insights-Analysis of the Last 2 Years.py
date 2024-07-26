import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from babel.numbers import format_decimal

# Load the dataset
data = pd.read_csv('F:/University Material/ADT/Project/Extract_Data_from_Warehouse/Extracted_data_cyber_attack_dataset01.csv')

# Extract year from AttackDate and ensure AttackYear is treated as a categorical variable
data['AttackYear'] = pd.to_datetime(data['AttackDate']).dt.year.astype(str)

# Order months correctly
data['AttackMonth'] = pd.Categorical(data['AttackMonth'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Add a count column for grouping
data['Count'] = 1

# Define attack columns
attack_columns = ['Spam(%)', 'Ransomware(%)', 'Local Infection(%)', 'Exploit(%)', 
                  'Malicious Mail(%)', 'Network Attack(%)', 'On Demand Scan(%)', 'Web Threat(%)']

# Ensure numeric columns for summation
for column in attack_columns:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# Streamlit App Configuration
st.set_page_config(
    page_title='Cyber Attack Analysis Dashboard',
    page_icon=':shield:',
    layout='wide',
)

# Streamlit App Title and Description
st.title("🔍 Recent Cyber Attack Insights-Analysis of the Last 2 Years")
st.markdown("""
Explore further insights into the latest trends and patterns in cyber attacks over the past two years. This section highlights key trends and patterns to help understand recent threats and their impact.
""")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Year filter
years = data['AttackYear'].unique().tolist()
selected_years = st.sidebar.multiselect("Select Year(s)", options=years, default=years)

# Country filter
countries = data['Country'].unique().tolist()
selected_countries = st.sidebar.multiselect("Select Country(ies)", options=countries, default=countries)

# Attack Type filter
selected_attack_types = st.sidebar.multiselect("Select Attack Type(s)", options=attack_columns, default=attack_columns)

# Filter data based on sidebar selections
filtered_data = data[(data['AttackYear'].isin(selected_years)) & (data['Country'].isin(selected_countries))]

# Ensure selected attack types are part of the DataFrame columns
selected_attack_types = [atk for atk in selected_attack_types if atk in filtered_data.columns]



# Attack Type Distribution (Percentage)
st.subheader("🎯 Attack Type Distribution (in %)")

col1, col2 = st.columns(2)
with col1:
    year = '2022'
    year_data = filtered_data[filtered_data['AttackYear'] == year]
    fig_pie_2022 = go.Figure()
    
    fig_pie_2022.add_trace(go.Pie(
        labels=selected_attack_types,
        values=year_data[selected_attack_types].sum().values,
        hole=.3,
        pull=[0.05]*len(selected_attack_types)
    ))

    fig_pie_2022.update_traces(textinfo='percent+label')
    fig_pie_2022.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),
        title_text=f"Attack in {year}",  
        showlegend=True,
        template='plotly_white'
    )

    st.plotly_chart(fig_pie_2022, use_container_width=True)

with col2:
    year = '2023'
    year_data = filtered_data[filtered_data['AttackYear'] == year]
    fig_pie_2023 = go.Figure()
    
    fig_pie_2023.add_trace(go.Pie(
        labels=selected_attack_types,
        values=year_data[selected_attack_types].sum().values,
        hole=.3,
        pull=[0.05]*len(selected_attack_types)
    ))

    fig_pie_2023.update_traces(textinfo='percent+label')
    fig_pie_2023.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),
         title=f"Attack in {year}",
        showlegend=True,
        template='plotly_white'
    )

    st.plotly_chart(fig_pie_2023, use_container_width=True)



# Global Attack Distribution by Country
st.subheader("🌍 Global Attack Distribution by Country")
country_data = filtered_data.groupby('Country')[selected_attack_types].sum().reset_index()
country_data['Total'] = country_data[selected_attack_types].sum(axis=1)

fig_choropleth = px.choropleth(
    country_data,
    locations='Country',
    locationmode='country names',
    color='Total',
    hover_name='Country',
    color_continuous_scale=px.colors.sequential.Plasma,
    labels={'Total': 'Total Attacks'},
    height=500
)

fig_choropleth.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
    geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
    template='plotly_white'
)

st.plotly_chart(fig_choropleth, use_container_width=True)
# Business Requirement 01: Multiple Bar Chart
st.subheader("📊 Monthly Attack Count by Year")
monthly_data = filtered_data.groupby(['AttackYear', 'AttackMonth'])['Count'].sum().reset_index()
monthly_data['Count'] = monthly_data['Count'].apply(lambda x: format_decimal(x, locale='en_US'))

fig_bar = px.bar(
    monthly_data,
    x='AttackMonth',
    y='Count',
    color='AttackYear',
    barmode='group',
    labels={'Count': 'Total Count of Attacks', 'AttackMonth': 'Month'},
    color_discrete_map={'2022': '#636EFA', '2023': '#EF553B'},
    height=400
)

fig_bar.update_layout(
    xaxis=dict(title='Month'),
    yaxis=dict(title='Total Count of Attacks'),
    legend=dict(title='Year'),
    margin=dict(l=50, r=50, t=50, b=50),
    template='plotly_white'
)

st.plotly_chart(fig_bar, use_container_width=True)

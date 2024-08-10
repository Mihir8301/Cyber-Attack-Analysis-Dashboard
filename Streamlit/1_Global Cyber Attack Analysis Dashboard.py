import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from langchain_community.llms import Ollama



# Load the new dataset
data = pd.read_excel('F:/University Material/ADT/Project/Extract_Data_from_Warehouse/Extracted_data_cyber_attack_dataset02.xlsx')

# Extract year from event_date
data['EventYear'] = pd.to_datetime(data['event_date']).dt.year.astype(str)

# Set up Streamlit app configuration
st.set_page_config(
    page_title='Cyber Attack Analysis Dashboard',
    page_icon=':shield:',
    layout='wide',
)

# Streamlit App Title and Description
st.title("🌐 Global Cyber Attack Analysis Dashboard")
st.markdown("""
Welcome to our Interactive Cyber Attack Analysis Dashboard. Explore comprehensive insights into global cyber threats with the interactive dashboard. Analyze attack trends across different years, countries, industries, and attack types to gain a deeper understanding of the evolving cyber landscape.
""")

# Sidebar filters
st.sidebar.header("Filter Options")
selected_year = st.sidebar.multiselect(
    "Select Year",
    options=data['EventYear'].unique(),
    default=data['EventYear'].unique()
)

selected_country = st.sidebar.multiselect(
    "Select Country",
    options=data['affected_country'].unique(),
    default=data['affected_country'].unique()
)

selected_industry = st.sidebar.multiselect(
    "Select Industry",
    options=data['affected_industry'].unique(),
    default=data['affected_industry'].unique()
)

selected_attack_type = st.sidebar.multiselect(
    "Select Attack Type",
    options=data['event_type'].unique(),
    default=data['event_type'].unique()
)

# Filter data based on selections
filtered_data = data[
    (data['EventYear'].isin(selected_year)) &
    (data['affected_country'].isin(selected_country)) &
    (data['affected_industry'].isin(selected_industry)) &
    (data['event_type'].isin(selected_attack_type))
]

# 1. Yearly Attack Trends (Line Chart)
st.subheader("📈 Yearly Attack Trends")

# Group by year and count attacks
yearly_attack_counts = filtered_data.groupby('EventYear')['event_date'].count().reset_index()
yearly_attack_counts.rename(columns={'event_date': 'TotalCount'}, inplace=True)

fig_line = px.line(
    yearly_attack_counts,
    x='EventYear',
    y='TotalCount',
    markers=True,
    labels={'TotalCount': 'Total Count of Attacks', 'EventYear': 'Year'},
    height=400,
    line_shape='spline',
    color_discrete_sequence=['#2CA02C']
)

fig_line.update_traces(line=dict(width=3))
fig_line.update_layout(
    xaxis=dict(title='Year'),
    yaxis=dict(title='Total Count of Attacks'),
    margin=dict(l=50, r=50, t=50, b=50),
    template='plotly_white'
)

st.plotly_chart(fig_line, use_container_width=True)

# 2. & 3. Top 10 Countries Attacked Most and Top 5 Actor Countries (Side by Side)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Top 10 Countries Attacked Most")

    # Filter out 'undetermined' entries
    data_filtered = filtered_data[filtered_data['affected_country'].str.lower() != 'undetermined']

    # Group by country and count attacks
    country_attack_counts = data_filtered.groupby('affected_country')['event_date'].count().reset_index()
    country_attack_counts.rename(columns={'event_date': 'TotalCount'}, inplace=True)
    country_attack_counts = country_attack_counts.sort_values(by='TotalCount', ascending=False).head(10)

    fig_bar = px.bar(
        country_attack_counts,
        x='affected_country',
        y='TotalCount',
        labels={'TotalCount': 'Total Count of Attacks', 'affected_country': 'Affected Country'},
        color='TotalCount',
        height=400,
        color_continuous_scale='Viridis'
    )

    fig_bar.update_layout(
        xaxis=dict(title='Affected Country'),
        yaxis=dict(title='Total Count of Attacks'),
        margin=dict(l=50, r=50, t=50, b=50),
        template='plotly_white'
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🦹‍♂️ Top 5 Actor Countries")

    # Group by actor country and count attacks
    actor_country_counts = filtered_data.groupby('actor')['event_date'].count().reset_index()
    actor_country_counts.rename(columns={'event_date': 'TotalCount'}, inplace=True)

    # Remove 'Undetermined' entries
    actor_country_counts = actor_country_counts[actor_country_counts['actor'].str.lower() != 'undetermined']

    # Get the top 5 actor countries
    top_actors = actor_country_counts.groupby('actor')['TotalCount'].sum().nlargest(5).index
    top_actor_country_counts = actor_country_counts[actor_country_counts['actor'].isin(top_actors)]

    fig_donut = px.pie(
        top_actor_country_counts,
        names='actor',
        values='TotalCount',
        labels={'TotalCount': 'Total Count of Attacks', 'actor': 'Actor Country'},
        height=400,
        hole=0.4  # Creates the donut hole effect
    )

    fig_donut.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),
        template='plotly_white'
    )

    st.plotly_chart(fig_donut, use_container_width=True)

# 4. Industry-Specific Threats and Trends (Stacked Bar Chart)
st.subheader("📊 Industry-Specific Threats and Trends")

# Prepare data for stacked bar chart
# Group by affected industry and event_type, count occurrences
industry_event_type_counts = filtered_data.groupby(['affected_industry', 'event_type'])['event_date'].count().reset_index()
industry_event_type_counts.rename(columns={'event_date': 'TotalCount'}, inplace=True)

# Ensure event_type categories are consistent
event_type_categories = ['Undetermined', 'Disruptive', 'Mixed']
industry_event_type_counts['event_type'] = pd.Categorical(
    industry_event_type_counts['event_type'],
    categories=event_type_categories,
    ordered=True
)

fig_stacked_bar = px.bar(
    industry_event_type_counts,
    x='affected_industry',
    y='TotalCount',
    color='event_type',
    labels={'TotalCount': 'Total Count of Attacks', 'affected_industry': 'Affected Industry', 'event_type': 'Event Type'},
    height=600,
    color_discrete_map={
        'Undetermined': '#636EFA',
        'Disruptive': '#EF553B',
        'Mixed': '#00CC96'
    },
    text='TotalCount',
    barmode='stack'
)

fig_stacked_bar.update_layout(
    xaxis=dict(title='Affected Industry'),
    yaxis=dict(title='Total Count of Attacks'),
    margin=dict(l=50, r=50, t=50, b=50),
    template='plotly_white'
)

st.plotly_chart(fig_stacked_bar, use_container_width=True)

# 5. Detailed Breakdown of Event Subtypes (Stacked Bar Chart)
st.subheader("📊 Detailed Breakdown of Event Subtypes")

# Group by event_type and event_subtype, count occurrences
event_subtype_counts = filtered_data.groupby(['event_type', 'event_subtype'])['event_date'].count().reset_index()
event_subtype_counts.rename(columns={'event_date': 'TotalCount'}, inplace=True)

# Get top 5 event subtypes
top_event_subtypes = event_subtype_counts.groupby('event_subtype')['TotalCount'].sum().nlargest(5).index
top_event_subtype_counts = event_subtype_counts[event_subtype_counts['event_subtype'].isin(top_event_subtypes)]

fig_subtype_bar = px.bar(
    top_event_subtype_counts,
    x='TotalCount',
    y='event_type',
    color='event_subtype',
    labels={'TotalCount': 'Total Count', 'event_type': 'Event Type', 'event_subtype': 'Event Subtype'},
    height=600,
    color_discrete_sequence=px.colors.qualitative.Plotly,
    barmode='stack'
)

fig_subtype_bar.update_layout(
    xaxis=dict(title='Total Count'),
    yaxis=dict(title='Event Type'),
    margin=dict(l=50, r=50, t=50, b=50),
    template='plotly_white'
)

st.plotly_chart(fig_subtype_bar, use_container_width=True)

# 6. Hierarchical Breakdown of Attack Types and Subtypes (Treemap Chart)
st.subheader("🌳 Hierarchical Breakdown of Attack Types and Subtypes")

# Prepare data for treemap chart
treemap_data = filtered_data.groupby(['event_type', 'event_subtype', 'affected_industry'])['event_date'].count().reset_index()
treemap_data.rename(columns={'event_date': 'TotalCount'}, inplace=True)

fig_treemap = px.treemap(
    treemap_data,
    path=['event_type', 'event_subtype', 'affected_industry'],
    values='TotalCount',
    labels={'TotalCount': 'Total Count', 'event_type': 'Event Type', 'event_subtype': 'Event Subtype', 'affected_industry': 'Affected Industry'},
    height=600
)

fig_treemap.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
    template='plotly_white'
)

st.plotly_chart(fig_treemap, use_container_width=True)



# Initialize the chatbot model
llm = Ollama(model="llama3")



# Chatbot section
st.title("🤖 CyberSentinel Chatbot")
st.markdown("""
Interact with the CyberSentinel Chatbot for insights and queries related to cybersecurity.
""")
prompt = st.text_area("Enter your question:")
if st.button("Answer"):
    if prompt:
        with st.spinner("Generating your answer..."):
            response = llm.invoke(prompt, stop=['<|eot_id|>'])
            st.write(response)

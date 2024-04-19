import pandas as pd

data = {
    'client': ['Client A', 'Client B', 'Client C', ...],
    'resources_planned': [10, 5, 8, ...],
    'rate_card': [100, 150, 80, ...],
    'planned_start': pd.to_datetime(['2024-01-01', '2024-04-01', '2024-02-15', ...]),
    'planned_end': pd.to_datetime(['2024-12-31', '2024-09-30', '2024-06-30', ...]),
    'actual_start': pd.to_datetime(['2024-01-01', '2024-05-15', '2024-03-01', ...]),
    'actual_end': pd.to_datetime(['2024-06-30', '2024-12-31', '2024-07-15', ...]) 
}

df = pd.DataFrame(data)

import streamlit as st
import altair as alt  # Or your preferred visualization library

# Load data (replace with your data loading mechanism)
df = pd.read_csv('your_data.csv') 

# App Title
st.title("Resource Allocation and Planning")

# --- User Inputs ---
st.sidebar.header("Filters")
selected_client = st.sidebar.selectbox("Select Client", df['client'].unique())
# Add more filters if needed

# --- Calculations ---
def calculate_resources_remaining(df, selected_client):
    client_data = df[df['client'] == selected_client]

    # 1. Calculate Total Planned Resources 
    total_planned_resources = client_data['resources_planned'].sum()

    # 2. Calculate Actual Months of Service Used
    client_data['months_used'] = (
        client_data['actual_end'].dt.to_period('M') - client_data['actual_start'].dt.to_period('M')
    ) + 1  # Add 1 to include both start and end months

    # 3. Calculate Actual Resources Consumed
    client_data['actual_resources'] = client_data['months_used'] * client_data['rate_card'] / 12  # Assuming monthly rate card

    total_actual_resources = client_data['actual_resources'].sum()

    # 4. Calculate Resources Remaining
    resources_remaining = total_planned_resources - total_actual_resources

    return resources_remaining

# --- Visualization ---
def create_resource_chart(df, selected_client):
   # ... Altair or other chart code ...
  chart = alt.Chart(df[df['client'] == selected_client]).mark_area().encode(
    x='month(actual_start):T',  # Month of the actual start date
    y=alt.Y('sum(resources_planned):Q', stack='zero'),
    y2=alt.Y2('sum(actual_resources):Q'),
    color='type:N',  # Distinguish 'planned' vs 'actual_resources'
  ) 
  chart = alt.Chart(df).mark_bar().encode(
    x='client:N',
    y='sum(resources_planned):Q'
  )




# --- Display Results ---
st.header("Resource Summary")
st.dataframe(df[df['client'] == selected_client])  # Show data table

resources_remaining = calculate_resources_remaining(df, selected_client)
st.metric("Resources Remaining to Sell", resources_remaining)

chart = create_resource_chart(df, selected_client)
st.altair_chart(chart)


st.metric("Resources Remaining to Sell", resources_remaining)




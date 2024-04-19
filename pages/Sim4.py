import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- Dummy Data Generation ---
np.random.seed(42)  # For reproducible results
data = {
    'client': ['Client A', 'Client B', 'Client C', 'Client D', 'Client E'] * 6,
    'resources_planned': np.random.randint(5, 15, size=30),
    'rate_card': np.random.randint(80, 200, size=30),
    'planned_start': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01'] * 6),
    'planned_end': pd.to_datetime(['2024-04-30', '2024-06-30', '2024-08-31', '2024-10-31', '2024-12-31'] * 6),
}
df = pd.DataFrame(data)

df['months_used'] = (df['actual_end'].dt.to_period('M') - df['actual_start'].dt.to_period('M')) + 1

df['actual_start'] = df['planned_start'].where(df['planned_start'] > datetime.now(), datetime.now())
df['actual_end'] = df.apply(lambda x: datetime.now() if pd.isna(x['actual_end']) else x['actual_end'], axis=1)

# --- App Structure ---
st.title("Resource Allocation and Planning")

# User Input
selected_client = st.sidebar.selectbox("Select Client", df['client'].unique())

# Calculations
def calculate_metrics(df, selected_client):
    client_data = df[df['client'] == selected_client]
    total_planned = client_data['resources_planned'].sum()

    client_data['months_used'] = (client_data['actual_end'].dt.to_period('M') - client_data['actual_start'].dt.to_period('M')) + 1
    actual_used = client_data['months_used'] * client_data['rate_card'] / 12 
    total_actual = actual_used.sum()

    remaining_months = 12 - datetime.now().month  
    resources_to_allocate = max(0, total_planned - total_actual) 
    monthly_allocation = resources_to_allocate / remaining_months

    return total_planned, total_actual, resources_to_allocate, monthly_allocation

total_planned, total_actual, to_allocate, monthly_allocation = calculate_metrics(df.copy(), selected_client)

# Display Metrics
st.header("Metrics")
st.metric("Total Resources Planned", total_planned)
st.metric("Total Resources Used", total_actual)
st.metric("Resources to Allocate (Remaining Year)", to_allocate)
st.metric("Recommended Monthly Allocation", monthly_allocation) 

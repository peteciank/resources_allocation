import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- Dummy Data Generation (Revised) ---
np.random.seed(42)
data = {
    'client': ['Client A', 'Client B', 'Client C', 'Client D', 'Client E'] * 6,
    'resources_planned': np.random.randint(5, 15, size=30),
    'rate_card': np.random.randint(80, 200, size=30),
    'planned_start': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01'] * 6),
    'planned_end': pd.to_datetime(['2024-04-30', '2024-06-30', '2024-08-31', '2024-10-31', '2024-12-31'] * 6)
}
df = pd.DataFrame(data)

df['actual_start'] = df['planned_start'].where(df['planned_start'] > datetime.now(), datetime.now())
df['actual_end'] = df.apply(lambda x: datetime.now() if pd.isna(x['actual_end']) else x['actual_end'], axis=1)

# --- App Structure ---
st.title("Resource Allocation and Planning")

# User Input
selected_client = st.sidebar.selectbox("Select Client", df['client'].unique())

# Calculations
def calculate_metrics(df, selected_client):
    # ... (Your calculation logic, same as before)

total_planned, total_actual, to_allocate, monthly_allocation = calculate_metrics(df.copy(), selected_client)

# Display Metrics
st.header("Metrics")
st.metric("Total Resources Planned", total_planned)
st.metric("Total Resources Used", total_actual)
st.metric("Resources to Allocate (Remaining Year)", to_allocate)
st.metric("Recommended Monthly Allocation", monthly_allocation) 

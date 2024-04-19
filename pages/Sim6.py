import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- Dummy Data Generation ---
np.random.seed(42)
data = {
    # ... (Your data structure)
}
df = pd.DataFrame(data)

# Ensure start/end date columns definitely exist
print(df.columns)  # DEBUGGING

# --- App Structure ---
st.title("Resource Allocation and Planning")

# User Input
selected_client = st.sidebar.selectbox("Select Client", df['client'].unique())

# Calculations
def calculate_metrics(df, selected_client):
    client_data = df[df['client'] == selected_client].copy()  # Work on a copy

    # DEBUGGING: Print the client data 
    print(client_data) 

    # --- (Rest of your calculation logic) ---

    # Ensure actual_end is always populated
    client_data['actual_end'] = client_data.apply(lambda x: datetime.now() if pd.isna(x['actual_end']) else x['actual_end'], axis=1)

    #  --- (Rest of your calculation logic) ---

    return total_planned, total_actual, to_allocate, monthly_allocation 

# ... (Rest of your Streamlit code) 

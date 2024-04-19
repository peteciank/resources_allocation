import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to generate dummy dates within a range
def generate_dates(start_date, end_date, n):
    delta = end_date - start_date
    return [start_date + timedelta(days=np.random.randint(delta.days + 1)) for _ in range(n)]

# Function to generate dummy data
def generate_dummy_data(n_clients):
    clients = ['Client_' + str(i) for i in range(1, n_clients + 1)]
    people = ['Person_' + str(i) for i in range(1, 11)]
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    data = {
        'Person': np.random.choice(people, size=100),
        'Client': np.random.choice(clients, size=100),
        'Planned Start Date': generate_dates(start_date, end_date, 100),
        'Planned End Date': generate_dates(start_date, end_date, 100),
        'Actual Start Date': [None] * 100,
        'Actual End Date': [None] * 100,
        'Rate Card': np.random.randint(50, 200, size=100)
    }
    return pd.DataFrame(data)

# Streamlit app
st.title('Resource Allocation Analysis')

# Generate dummy data
df = generate_dummy_data(10)

# Display dummy data
st.subheader('Dummy Data')
st.write(df)

# Slicer to simulate allocation
st.subheader('Simulate Allocation')
allocated_resources = st.slider('Allocate Resources', min_value=0, max_value=10, step=1)

# Update actual allocation based on user input
df.loc[df['Person'] == 'Missing', 'Actual Start Date'] = datetime.now().strftime('%Y-%m-%d')
df.loc[df['Person'] == 'Missing', 'Actual End Date'] = (datetime.now() + timedelta(days=allocated_resources)).strftime('%Y-%m-%d')

# Calculation
planned_allocation = df.shape[0]
actual_allocation = df['Actual Start Date'].count()
remaining_resources = planned_allocation - actual_allocation

# Metrics
st.subheader('Resource Allocation Metrics')
st.write(f'Planned Allocation: {planned_allocation}')
st.write(f'Actual Allocation: {actual_allocation}')
st.write(f'Remaining Resources: {remaining_resources}')

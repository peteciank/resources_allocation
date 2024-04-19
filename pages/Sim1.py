import streamlit as st
import pandas as pd
import numpy as np


import pandas as pd
import numpy as np
import datetime

# Create dummy data
np.random.seed(0)
n_resources = 30
n_clients = 10

resources = {
    'Resource ID': range(1, n_resources + 1),
    'Client': np.random.choice(range(1, n_clients + 1), n_resources),
    'Rate Card': np.random.randint(50, 200, n_resources),
    'Planned Start Date': [datetime.date(2024, np.random.randint(1, 13), 1) for _ in range(n_resources)],
    'Planned End Date': [datetime.date(2024, np.random.randint(1, 13), 28) for _ in range(n_resources)],
    'Current Start Date': [datetime.date(2024, np.random.randint(1, 13), 1) for _ in range(n_resources)],
    'Current End Date': [datetime.date(2024, np.random.randint(1, 13), 28) for _ in range(n_resources)]
}

# Create DataFrame
df = pd.DataFrame(resources)

# Display table
print(df)

data = df
# Load data
# Replace this with your data loading logic
#data = pd.read_csv('your_data.csv')

# Display data
st.title('Resource Allocation Analysis')
st.subheader('Planned vs Actual Allocation')

# Display tables or plots here to show planned vs actual allocation
# Example:
st.write(data)

# Calculation
planned_allocation = data['Planned Allocation'].sum()
actual_allocation = data['Actual Allocation'].sum()
remaining_resources = planned_allocation - actual_allocation

# Display results
st.subheader('Calculation Results')
st.write(f'Planned Allocation: {planned_allocation}')
st.write(f'Actual Allocation: {actual_allocation}')
st.write(f'Remaining Resources: {remaining_resources}')

# User input
n_clients = st.number_input('Number of Clients', min_value=1, value=10)
resource_per_client = st.number_input('Resource Quantity per Client', min_value=1, value=100)

# Calculate required resources to sell
required_resources = n_clients * resource_per_client - remaining_resources
required_months = np.ceil(required_resources / resource_per_client)

# Display required resources and months
st.write(f'Required Resources to Sell: {required_resources}')
st.write(f'Required Months to Cover Plan: {required_months}')

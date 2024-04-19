import streamlit as st
import pandas as pd
import numpy as np

# Create dummy data
data = {
    'Client': ['Client_' + str(i) for i in range(1, 11)],
    'Planned Allocation': [3, 4, 2, 5, 3, 4, 3, 2, 1, 3],
    'Actual Allocation': [2, 3, 1, 4, 2, 3, 2, 1, 1, 2]
}

# Create DataFrame
df = pd.DataFrame(data)

# Add missing resources
missing_resources = {'Client': ['Missing'] * 10,
                     'Planned Allocation': [1] * 10,
                     'Actual Allocation': [0] * 10}
missing_df = pd.DataFrame(missing_resources)

# Concatenate DataFrames
df = pd.concat([df, missing_df])

# Reset index
df.reset_index(drop=True, inplace=True)

# Streamlit app
st.title('Resource Allocation Analysis')

# Slicer to simulate allocation
st.subheader('Simulate Allocation')
allocated_resources = st.slider('Allocate Resources', min_value=0, max_value=10, step=1)

# Update actual allocation based on user input
df.loc[df['Client'] == 'Missing', 'Actual Allocation'] = allocated_resources

# Calculation
planned_allocation = df['Planned Allocation'].sum()
actual_allocation = df['Actual Allocation'].sum()
remaining_resources = planned_allocation - actual_allocation

# Metrics
st.subheader('Resource Allocation Metrics')
st.write(f'Planned Allocation: {planned_allocation}')
st.write(f'Actual Allocation: {actual_allocation}')
st.write(f'Remaining Resources: {remaining_resources}')

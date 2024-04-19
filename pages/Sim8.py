import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Dummy data generation function
def generate_dummy_data(num_clients, num_resources):
    # Generate rate cards for resources
    rate_cards = np.random.uniform(100, 500, num_resources)
    
    # Generate planned and actual dates within a fiscal year
    fiscal_year_start = datetime(2023, 1, 1)
    dates_range = [fiscal_year_start + timedelta(days=i) for i in range(365)]
    
    def random_date_pairs(start, end):
        p_start = np.random.choice(dates_range[start:end])
        p_end = np.random.choice(dates_range[dates_range.index(p_start):end])
        return p_start, p_end
    
    clients_data = {
        'Client ID': [f'Client_{i+1}' for i in range(num_clients)],
        'Planned Start': [],
        'Planned End': [],
        'Actual Start': [],
        'Actual End': [],
        'Resource': np.random.choice(range(1, num_resources + 1), num_clients),
        'Rate Card': np.random.choice(rate_cards, num_clients)
    }
    
    for _ in range(num_clients):
        p_start, p_end = random_date_pairs(0, 200) # Planned dates in the first half of the year
        a_start, a_end = random_date_pairs(100, 265) # Actual dates with possible delay
        clients_data['Planned Start'].append(p_start)
        clients_data['Planned End'].append(p_end)
        clients_data['Actual Start'].append(a_start)
        clients_data['Actual End'].append(a_end)
    
    return pd.DataFrame(clients_data)

# Resource allocation calculation function
def calculate_allocation(df, fiscal_year_end):
    # Calculate planned and actual allocations
    df['Planned Allocation'] = (df['Planned End'] - df['Planned Start']).dt.days * df['Rate Card']
    df['Actual Allocation'] = (df['Actual End'] - df['Actual Start']).dt.days * df['Rate Card']
    
    # Calculate total planned and actuals
    total_planned = df['Planned Allocation'].sum()
    total_actual = df['Actual Allocation'].sum()
    
    # Calculate the remaining allocation amount to meet the plan
    remaining_allocation = total_planned - total_actual
    
    # Calculate time left in the fiscal year
    time_left = (fiscal_year_end - datetime.today()).days
    
    # Estimate the daily allocation needed
    daily_allocation_needed = remaining_allocation / time_left
    return remaining_allocation, time_left, daily_allocation_needed

# Main app function
def main():
    st.title("Resource Allocation Analysis")

    # Sidebar inputs for number of clients and resources
    st.sidebar.header('Configuration')
    num_clients = st.sidebar.number_input('Number of Clients', min_value=10, value=10)
    num_resources = st.sidebar.number_input('Number of Resources', min_value=30, value=30)
    
    # Generate dummy data
    df_clients = generate_dummy_data(num_clients, num_resources)
    
    # Show raw data
    st.subheader('Client Resource Allocations (Dummy)')
    st.dataframe(df_clients)

    # Calculate allocations
    fiscal_year_end = datetime(2023, 12, 31)
    remaining_allocation, time_left, daily_allocation_needed = calculate_allocation(df_clients, fiscal_year_end)
    
    # Display remaining allocation needs
    st.subheader('Remaining Allocation Needs')
    st.write(f"Remaining Allocation Amount: ${remaining_allocation}")
    st.write(f"Days Left in Fiscal Year: {time_left}")
    st.write(f"Daily Allocation Needed: ${daily_allocation_needed:.2f}")

    # Visualization of the planned vs actual allocations
    st.subheader('Planned vs Actual Allocations')
    
    fig, ax = plt.subplots()
    df_clients.set_index('Client ID')[['Planned Allocation', 'Actual Allocation']].plot(kind='bar', ax=ax)
    ax.set_ylabel('Allocation Amount ($)')
    st.pyplot(fig)

    # (Optional) Additional visualizations and statistics can be added here

if __name__ == "__main__":
    main()

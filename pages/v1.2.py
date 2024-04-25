import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Resource Allocation Simulator")

# Sidebar for user inputs
st.sidebar.title('Edit Resource Details')

# Pre-populated dataframe with roles, seniorities, rates, and quantities
data = {
    'Role': ['Project Manager', 'Project Manager', 'Project Manager',
             'Product Manager', 'Product Manager', 'Product Manager',
             'Product Owner', 'Product Owner', 'Product Owner',
             'Scrum Master', 'Scrum Master', 'Scrum Master',
             'Developer', 'Developer', 'Developer'],
    'Seniority': ['Senior', 'Semi Senior', 'Junior'] * 5,
    'Rate': [60, 45, 25, 65, 45, 25, 65, 45, 25, 65, 45, 25, 80, 50, 35],
    'Quantity': [3, 6, 7, 3, 6, 7, 3, 6, 7, 3, 6, 7, 3, 6, 7]
}

df = pd.DataFrame(data)

# Store dataframe in session state if it is not already there
if 'editable_df' not in st.session_state:
    st.session_state['editable_df'] = df.copy()

# Function to update the dataframe with new values
def update_values():
    index = st.session_state['index']
    st.session_state['editable_df'].loc[index, 'Rate'] = st.sidebar.number_input('Rate USD/hour', value=current_rate)
    st.session_state['editable_df'].loc[index, 'Quantity'] = st.sidebar.number_input('Quantity', value=current_quantity)
    update_calculations()

# Function to recalculate the forecast and invoice amount
def update_calculations():
    total_invoice_amount = (st.session_state['editable_df']['Rate'] * st.session_state['editable_df']['Quantity']).sum()
    invoice_progression = total_invoice_amount * (pd.Timestamp.now().month / 12)
    forecast = total_invoice_amount * (12 - pd.Timestamp.now().month) / 12
    
    # Update the total invoice amount and forecast in session state
    st.session_state['total_invoice_amount'] = total_invoice_amount
    st.session_state['forecast'] = forecast
    st.session_state['invoice_progression'] = invoice_progression

    # Update the chart
    display_progression_chart(invoice_progression)

# Function to plot the progression chart
def display_progression_chart(current_progression):
    plt.figure(figsize=(10, 4))
    months = list(range(1, 13))  # Months from January to December
    progression = [current_progression * (month / 12) for month in months]
    
    plt.plot(months, progression, marker='o')
    plt.title('Invoice Progression Chart')
    plt.xlabel('Month')
    plt.ylabel('Invoicing (USD)')
    plt.grid(True)
    st.pyplot(plt)

# Allow user to select role and seniority to update rate and quantity
selected_role = st.sidebar.selectbox('Role', df['Role'].unique(), key='role')
selected_seniority = st.sidebar.selectbox('Seniority', df['Seniority'].unique(), key='seniority')

# Determine the current rate and quantity
selected_index = df[(df['Role'] == selected_role) & (df['Seniority'] == selected_seniority)].index
st.session_state['index'] = selected_index[0]
current_rate = df.loc[selected_index, 'Rate'].values[0]
current_quantity = df.loc[selected_index, 'Quantity'].values[0]

# Display the current values to user and allow for editing
if 'update_values' not in st.session_state:
    st.sidebar.button('Update Values', on_click=update_values)

# Show the invoice amount and forecast
if 'total_invoice_amount' in st.session_state:
    st.metric(label='Total Invoice Amount', value=f"${st.session_state['total_invoice_amount']:,.2f}")
if 'forecast' in st.session_state:
    st.metric(label='Forecast for the Rest of the Year', value=f"${st.session_state['forecast']:,.2f}")

# Show the main DataFrame table
st.subheader("Resource Rates and Quantities")
st.dataframe(st.session_state['editable_df'].style.format({'Rate': "${:.2f}", 'Quantity': "{:.0f}"}))

# Display chart for progression if available
if 'invoice_progression' in st.session_state:
    display_progression_chart(st.session_state['invoice_progression'])

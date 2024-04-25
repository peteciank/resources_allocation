import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Resource Allocation Simulator")

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

# To allow users to edit the table, we will need to use the Session State feature to store the dataframe
if 'editable_df' not in st.session_state:
    st.session_state['editable_df'] = df.copy()

def update_table():
    idx = (st.session_state['editable_df']['Role'] == selected_role) & \
          (st.session_state['editable_df']['Seniority'] == selected_seniority)
    st.session_state['editable_df'].loc[idx, 'Rate'] = st.session_state['rate_input']
    st.session_state['editable_df'].loc[idx, 'Quantity'] = st.session_state['quantity_input']
    recalculate()

def recalculate():
    invoice_amount = (st.session_state['editable_df']['Rate'] * st.session_state['editable_df']['Quantity']).sum()
    months_remaining = 12 - pd.Timestamp.now().month
    forecast = invoice_amount * months_remaining
    st.session_state['invoice_amount'] = invoice_amount
    st.session_state['forecast'] = forecast
    display_progression(invoice_amount)

def display_progression(invoice_amount):
    current_month = pd.Timestamp.now().month
    monthly_invoicing = invoice_amount / current_month
    months = list(range(1, 13)) # Months from January to December
    progression = [monthly_invoicing * month for month in months]
    
    plt.figure(figsize=(10, 4))
    plt.plot(months, progression, marker='o')
    plt.title('Invoicing Progression Over the Year')
    plt.xlabel('Month')
    plt.ylabel('Cumulative Invoicing (USD)')
    plt.grid(True)
    st.pyplot(plt)

# Display and update the editable dataframe
selected_role = st.selectbox('Select the Role to Edit:', df['Role'].unique())
selected_seniority = st.selectbox('Select the Seniority Level to Edit:', df['Seniority'].unique())

# Prefill the current rate and quantity based on the role and seniority selected
current_values = df[(df['Role'] == selected_role) & (df['Seniority'] == selected_seniority)]
if not current_values.empty:
    current_rate, current_quantity = current_values.iloc[0][['Rate', 'Quantity']]
else:
    current_rate, current_quantity = 0, 0

st.session_state['rate_input'] = st.number_input('Edit Rate', value=current_rate)
st.session_state['quantity_input'] = st.number_input('Edit Quantity', value=current_quantity)

# Update button
if st.button('Update Values'):
    update_table()

# Display the current state of the dataframe
st.subheader("Current Resource Rates and Quantities")
st.table(st.session_state['editable_df'])

# Display results
st.subheader('Resource Allocation Results')
if 'invoice_amount' in st.session_state:
    st.write(f"Total Invoice Amount: ${st.session_state['invoice_amount']:,.2f}")
if 'forecast' in st.session_state:
    st.write(f"Forecast for the Rest of the Year: ${st.session_state['forecast']:,.2f}")

# Display progression chart
if 'invoice_amount' in st.session_state:
    display_progression(st.session_state['invoice_amount'])

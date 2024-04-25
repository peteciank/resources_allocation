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

if 'editable_df' not in st.session_state:
    st.session_state['editable_df'] = df.copy()

st.sidebar.title('Resource Details')

selected_role = st.sidebar.selectbox('Select Role', options=df['Role'].unique())
selected_seniority = st.sidebar.selectbox('Select Seniority', options=df['Seniority'].unique())

# Update the rate and quantity based on the user's selection
mask = (st.session_state.editable_df['Role'] == selected_role) & (st.session_state.editable_df['Seniority'] == selected_seniority)
selected_index = st.session_state.editable_df.index[mask].tolist()
if selected_index:
    selected_index = selected_index[0]
    rate = st.sidebar.number_input('Rate USD/hour', value=st.session_state.editable_df.at[selected_index, 'Rate'])
    quantity = st.sidebar.number_input('Quantity', value=st.session_state.editable_df.at[selected_index, 'Quantity'])

    # Update the DataFrame and recalculate if changes are detected
    if rate != st.session_state.editable_df.at[selected_index, 'Rate'] or quantity != st.session_state.editable_df.at[selected_index, 'Quantity']:
        st.session_state.editable_df.at[selected_index, 'Rate'] = rate
        st.session_state.editable_df.at[selected_index, 'Quantity'] = quantity

# Calculate the total invoice amount and forecast
total_invoice_amount = (st.session_state.editable_df['Rate'] * st.session_state.editable_df['Quantity']).sum()
current_month = pd.Timestamp.now().month
monthly_invoice = total_invoice_amount / current_month
forecast = monthly_invoice * (12 - current_month)

st.metric(label='Total Invoice Amount', value=f"${total_invoice_amount:,.2f}")
st.metric(label='Forecast for the Rest of the Year', value=f"${forecast:,.2f}")

st.subheader("Resource Rates and Quantities")
st.table(st.session_state.editable_df.style.format({'Rate': "${:.2f}", 'Quantity': "{:.0f}"}))

# Plotting the progression chart
plt.figure(figsize=(10, 4))
months = list(range(1, 13)) # Months from January to December
progression = [monthly_invoice * month for month in months]

plt.plot(months, progression, marker='o')
plt.title('Invoicing Progression Over the Year')
plt.xlabel('Month')
plt.ylabel('Cumulative Invoicing (USD)')
plt.grid(True)
st.pyplot(plt)  # Fixes issue of plotting twice by only calling plt once

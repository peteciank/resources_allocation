import streamlit as st
import pandas as pd

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
    st.session_state['editable_df'] = df

# Define Session State key for updating the dataframe from the user input
st.session_state['update'] = False

def update_table():
    st.session_state['update'] = True

# Display the dataframe for editing
st.subheader("Resource Rates and Quantities")

with st.expander("Resource Allocation Table"):
    st.table(st.session_state['editable_df'])


with st.sidebar:
    # User input to edit the dataframe
    role_to_edit = st.selectbox('Select the Role to Edit:', df['Role'].unique())
    seniority_to_edit = st.selectbox('Select the Seniority Level to Edit:', df['Seniority'].unique())
    new_rate = st.number_input('Edit Rate', min_value=0)
    new_quantity = st.number_input('Edit Quantity', min_value=0)
    edit_button = st.button('Update Values', on_click=update_table)

    # Update the dataframe if the user clicks the update button
    if edit_button and new_rate and new_quantity:
        idx = (st.session_state['editable_df']['Role'] == role_to_edit) & \
            (st.session_state['editable_df']['Seniority'] == seniority_to_edit)
        st.session_state['editable_df'].loc[idx, 'Rate'] = new_rate
        st.session_state['editable_df'].loc[idx, 'Quantity'] = new_quantity



    # Recalculate the forecast and approximated invoicing after any update
    if st.session_state['update']:
        invoice_amount = (st.session_state['editable_df']['Rate'] * st.session_state['editable_df']['Quantity']).sum()
        months_remaining = 12 - pd.Timestamp.now().month
        forecast = invoice_amount * months_remaining
        st.session_state['update'] = False

        st.subheader('Resource Allocation Results')
        st.write(f"Total Invoice Amount: ${invoice_amount:,.2f}")
        st.write(f"Forecast for the Rest of the Year: ${forecast:,.2f}")


invoice_amount = (st.session_state['editable_df']['Rate'] * st.session_state['editable_df']['Quantity']).sum()
months_remaining = 12 - pd.Timestamp.now().month
forecast = invoice_amount * months_remaining
st.subheader('Resource Allocation Results')
st.write(f"Total Invoice Amount: ${invoice_amount:,.2f}")
st.write(f"Forecast for the Rest of the Year: ${forecast:,.2f}")

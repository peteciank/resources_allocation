import pandas as pd
import numpy as np

# Generate dummy data
np.random.seed(0)
n_clients = 10
n_resources = 30
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq='MS')

# Clients and resources
clients = [f"Client {i+1}" for i in range(n_clients)]
resources = [f"Resource {i+1}" for i in range(n_resources)]
rate_cards = np.random.randint(100, 1000, size=n_resources)

# Planned and actual data
data = {
    'Client': np.random.choice(clients, n_resources),
    'Resource': resources,
    'Rate Card': rate_cards,
    'Planned Start': np.random.choice(dates, n_resources),
    'Planned End': np.random.choice(dates, n_resources),
    'Actual Start': np.random.choice(dates, n_resources),
    'Actual End': np.random.choice(dates, n_resources)
}

df = pd.DataFrame(data)
df['Planned Start'] = pd.to_datetime(df['Planned Start']).dt.date
df['Planned End'] = pd.to_datetime(df['Planned End']).dt.date
df['Actual Start'] = pd.to_datetime(df['Actual Start']).dt.date
df['Actual End'] = pd.to_datetime(df['Actual End']).dt.date

# Ensure end dates are after start dates
df['Planned End'] = df.apply(lambda row: max(row['Planned End'], row['Planned Start']), axis=1)
df['Actual End'] = df.apply(lambda row: max(row['Actual End'], row['Actual Start']), axis=1)

print(df.head())

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data (assuming the above data preparation is in the same script or imported)
# df = ...

def load_data():
    # This function would return the DataFrame we created earlier
    return df

def main():
    st.title("Resource Allocation Dashboard")

    df = load_data()

    st.write("## Resource Overview")
    st.dataframe(df)

    st.write("## Visualization")
    # Example visualization: Resources per client
    fig, ax = plt.subplots()
    df['Client'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title("Resources per Client")
    ax.set_xlabel("Client")
    ax.set_ylabel("Number of Resources")
    st.pyplot(fig)

    # More analysis and visualizations can be added here

if __name__ == "__main__":
    main()
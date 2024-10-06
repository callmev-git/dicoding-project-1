# First, let's create the code to structure the Streamlit app based on the notebook contents

streamlit_code = """
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Title of the Streamlit App
st.title("Bike Sharing Data Analysis")

# Load the dataset
@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/selva86/datasets/master/Bike-Sharing-Dataset/day.csv'
    data = pd.read_csv(url)
    return data

data = load_data()

# Display the dataset
if st.checkbox('Show raw data'):
    st.write(data)

# EDA Section
st.subheader('Exploratory Data Analysis')

# Plot Total Rentals by Temperature
st.write('### Total Rentals by Temperature')
plt.figure(figsize=(10,6))
sns.lineplot(x='temp', y='cnt', data=data)
plt.title('Total Rentals by Temperature')
plt.xlabel('Normalized Temperature')
plt.ylabel('Total Rentals')
st.pyplot(plt)

# Plot Rentals by Season
st.write('### Rentals by Season')
season_rentals = data.groupby('season')['cnt'].sum()
plt.figure(figsize=(8,8))
plt.pie(season_rentals, labels=['Winter', 'Spring', 'Summer', 'Fall'], autopct='%1.1f%%', startangle=90, colors=['#4D77FF','#FF9999','#66FF66','#FFCC66'])
plt.title('Bike Rentals by Season')
plt.axis('equal')
st.pyplot(plt)

# Machine Learning Section
st.subheader('Bike Rental Prediction Model')

# Select features and target variable
features = ['temp', 'atemp', 'hum', 'windspeed']
X = data[features]
y = data['cnt']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Display Metrics
mse = mean_squared_error(y_test, y_pred)
st.write(f'### Mean Squared Error of the model: {mse:.2f}')

# Conclusion Section
st.subheader('Conclusion')
st.write('- The temperature significantly influences the number of bike rentals. Rentals tend to increase with temperature but drop after a certain point.')
st.write('- Fall season sees the highest bike rentals compared to other seasons.')
"""

# Save the Streamlit code to a file
streamlit_file_path = '/mnt/data/bike_sharing_streamlit_app.py'
with open(streamlit_file_path, 'w') as streamlit_file:
    streamlit_file.write(streamlit_code)

streamlit_file_path

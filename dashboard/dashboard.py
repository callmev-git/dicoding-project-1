import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

sns.set(style='dark')

st.title('Proyek Analisis Data: Bike sharing')
st.markdown("""
- **Nama:** Muhammad Vitro Ramadhan
- **Email:** muvira123@gmail.com
- **ID Dicoding:** muhammadvitro
""")

st.header('Pertanyaan Bisnis')
st.markdown("""
- Pertanyaan 1 : Bagaimana pengaruh suhu terhadap total peminjaman sepeda?
- Pertanyaan 2 : Bagaimana pengaruh musim terhadap total peminjaman sepeda?
- Pertanyaan 3 : Bagaimana performa peminjaman sepeda dari tahun ke tahun?
""")

# Load the dataset
data = pd.read_csv('https://raw.githubusercontent.com/callmev-git/dicoding-project-1/main/Bike-sharing-dataset/hour.csv')

# Title of the dashboard
st.title('Analisis Peminjaman Sepeda')

# Question 1: Pengaruh Suhu terhadap Total Peminjaman Sepeda
st.header('Pengaruh Suhu terhadap Total Peminjaman Sepeda')

# Sidebar for filtering temperature
min_temp = float(data['temp'].min())
max_temp = float(data['temp'].max())
temp_filter = st.sidebar.slider('Filter Suhu', min_temp, max_temp, (min_temp, max_temp))

# Filter the data based on temperature
filtered_data = data[(data['temp'] >= temp_filter[0]) & (data['temp'] <= temp_filter[1])]

# Calculate average rentals in the filtered data
average_rentals = filtered_data['cnt'].mean()

# Group the data by temperature and calculate the mean rentals
mean_rentals = filtered_data.groupby('temp')['cnt'].mean().reset_index()

# Create a line chart with Altair
line_chart = alt.Chart(mean_rentals).mark_line(color='blue').encode(
    x=alt.X('temp', title='Suhu (Ternormalisasi)'),
    y=alt.Y('cnt', title='Rata-rata Peminjaman'),
    tooltip=['temp', 'cnt']
).properties(
    title='Rata-rata Peminjaman Sepeda Berdasarkan Suhu'
)

# Show the line chart in Streamlit
st.altair_chart(line_chart, use_container_width=True)

# Display the filtered data
st.markdown(f"- Rata-rata peminjaman sepeda: {average_rentals:.2f}")

# Question 2: Pengaruh Musim terhadap Total Peminjaman Sepeda
st.header('Pengaruh Musim terhadap Total Peminjaman Sepeda')

# Menamai setiap musim
season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
data['season_name'] = data['season'].map(season_mapping)

# Calculate average rentals for each season
average_rentals_by_season = data.groupby('season_name')['cnt'].mean().reset_index()

# Filter untuk memilih musim
default_seasons = ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur']
selected_seasons = st.sidebar.multiselect("Pilih Musim:", options=default_seasons, default=default_seasons)

# Filter data berdasarkan musim yang dipilih
filtered_data = average_rentals_by_season[average_rentals_by_season['season_name'].isin(selected_seasons)]

# Create a bar chart using Altair
bar_chart = alt.Chart(filtered_data).mark_bar(color='steelblue').encode(
    x=alt.X('season_name', title='Musim', sort=filtered_data['cnt']),
    y=alt.Y('cnt', title='Rata-rata Peminjaman'),
    tooltip=['season_name', 'cnt']
).properties(
    title="Distribusi Rata-rata Peminjaman Sepeda Berdasarkan Musim"
)

# Display the bar chart in Streamlit
st.altair_chart(bar_chart, use_container_width=True)

# Additional information
st.markdown("""
            - Peminjaman terbanyak terdapat pada musim gugur.
""")

# Question 3: Bagaimana performa peminjaman sepeda setiap tahunnya?
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
data['months'] = data['mnth'].apply(lambda x: months[x - 1])

# Filter data for the years 2011 and 2012
data_2011 = data[data['yr'] == 0]  # 0 represents the year 2011
data_2012 = data[data['yr'] == 1]  # 1 represents the year 2012

# Group data by year and calculate total rentals for each year
yearly_data = data.groupby('yr')['cnt'].sum().reset_index()

# Create a pie chart using Altair
pie_chart = alt.Chart(yearly_data).mark_arc().encode(
    theta=alt.Theta(field="cnt", type="quantitative", title="Total Peminjaman"),
    color=alt.Color(field="yr", type="nominal", title="Tahun"),
    tooltip=['yr', 'cnt']
).properties(
    title="Distribusi Total Peminjaman Sepeda per Tahun"
)

# Display the pie chart in Streamlit
st.header("Distribusi Total Peminjaman Sepeda (2011 vs 2012)")
st.altair_chart(pie_chart, use_container_width=True)

st.markdown("""
            - Peminjaman pada tahun 2011: 1243103 pengguna
            - Peminjaman pada tahun 2012: 2049576 pengguna
""")

st.header('Distribusi Peminjaman Sepeda Setiap Bulan')

# Pisahkan data berdasarkan tahun
data_2011 = data[data['yr'] == 0]  # 2011
data_2012 = data[data['yr'] == 1]  # 2012

# Agregasi peminjaman sepeda berdasarkan bulan untuk setiap tahun
rentals_2011 = data_2011.groupby('mnth')['cnt'].sum()
rentals_2012 = data_2012.groupby('mnth')['cnt'].sum()

# Group data by month and calculate total rentals for each month
monthly_data_2011 = data_2011.groupby('months')['cnt'].sum().reset_index()
monthly_data_2012 = data_2012.groupby('months')['cnt'].sum().reset_index()

# Create pie chart for 2011
pie_chart_2011 = alt.Chart(monthly_data_2011).mark_arc().encode(
    theta=alt.Theta(field="cnt", type="quantitative", title="Total Rentals"),
    color=alt.Color(field="months", type="nominal", title="Bulan"),
    tooltip=['months', 'cnt']
)

# Create pie chart for 2012
pie_chart_2012 = alt.Chart(monthly_data_2012).mark_arc().encode(
    theta=alt.Theta(field="cnt", type="quantitative", title="Total Peminjaman"),
    color=alt.Color(field="months", type="nominal", title="Bulan"),
    tooltip=['months', 'cnt']
)

# Layout the two pie charts side by side
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Tahun 2011")
    st.altair_chart(pie_chart_2011, use_container_width=True)

with right_column:
    st.subheader("Tahun 2012")
    st.altair_chart(pie_chart_2012, use_container_width=True)
st.markdown("""
            - Peminjaman terbanyak terdapat pada bulan Juni untuk tahun 2011 dan bulan September untuk tahun 2012
""")

# Membuat kesimpulan
st.title("Conclusion")
st.markdown("""
- Pertanyaan 1: Dapat disimpulkan bahwa suhu memiliki pengaruh terhadap total peminjaman sepeda. Sebagaimana pada grafik yang telah dibuat, total pengguna sepeda meningkat seiring bertambahnya suhu. Hal ini menunjukkan pengguna sepeda lebih memilih meminjam sepeda ketika suhunya hangat, tetapi juga tidak terlalu panas.
- Pertanyaan 2: Dapat disimpulkan bahwa sebagian besar pengguna sepeda lebih memilih menggunakan sepeda pada musim gugur, sebagaimana yang ditunjukkan pada grafik distribusi peminjaman sepeda lintas musim, dengan persentase penggunanya sebesar 32.2%.
- Pertanyaan 3: Dapat disimpulkan performa peminjaman sepeda meningkat dari tahun ke tahun dengan cukup signifikan. 
""")

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
- Pertanyaan 1 : Adakah pengaruh suhu terhadap total peminjaman sepeda?
- Pertanyaan 2 : Adakah pengaruh musim terhadap total peminjaman sepeda?
- Pertanyaan 3 : Pada tahun berapa peminjaman sepeda tertinggi?
- Pertanyaan 4 : Pada bulan apa setiap tahunnya peminjaman sepeda tertinggi? 
""")

# Load the dataset
data = pd.read_csv('https://raw.githubusercontent.com/callmev-git/dicoding-project-1/main/Bike-sharing-dataset/hour.csv')

# Title of the dashboard
st.title('Analisis Peminjaman Sepeda')

# Question 1: Pengaruh Suhu terhadap Total Peminjaman Sepeda
st.header('Pengaruh Suhu terhadap Total Peminjaman Sepeda')

# Membuat Clustering untuk Temperatur
data["temp_bins"] = pd.cut(data["temp"], bins=11, labels=range(0, 11))

# Plot temperature vs bike rentals
fig, ax = plt.subplots()
sns.barplot(x=data['temp_bins'], y=data['cnt'], ax=ax)
ax.set_title('Hubungan Suhu dengan Total Peminjaman Sepeda')
ax.set_xlabel('Suhu (Normalized)')
ax.set_ylabel('Total Peminjaman Sepeda')
st.pyplot(fig)

# Sidebar for filtering temperature
min_temp = float(data['temp'].min())
max_temp = float(data['temp'].max())
temp_filter = st.sidebar.slider('Filter Suhu', min_temp, max_temp, (min_temp, max_temp))

# Filter the data based on temperature
filtered_data = data[(data['temp'] >= temp_filter[0]) & (data['temp'] <= temp_filter[1])]

# Calculate average rentals in the filtered data
average_rentals = filtered_data['cnt'].mean()

# Display the filtered data
st.write(f"Menampilkan data untuk suhu antara {temp_filter[0]} dan {temp_filter[1]}")
st.write(f"Rata-rata peminjaman sepeda: {average_rentals:.2f}")

# Plot total rentals against temperature
st.line_chart(filtered_data.groupby('temp')['cnt'].mean())

# Question 2: Pengaruh Musim terhadap Total Peminjaman Sepeda
st.header('Pengaruh Musim terhadap Total Peminjaman Sepeda')

# Menamai setiap musim
season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
data['season_name'] = data['season'].map(season_mapping)

# Plot the pie chart
season_rentals = data.groupby('season_name')['cnt'].sum()
fig, ax = plt.subplots()
ax.pie(season_rentals, labels=season_rentals.index, autopct='%1.1f%%', startangle=90, colors=['#4D77FF','#FF9999','#66FF66','#FFCC66'])
ax.set_title('Proporsi Peminjaman Sepeda Berdasarkan Musim')
ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
st.pyplot(fig)

# Question 3: Pada tahun berapa peminjaman sepeda tertinggi?
st.header('Distribusi Peminjaman Sepeda Setiap Tahun')

# Convert 'dteday' to datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Add month names to the data for better readability
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
data['months'] = data['mnth'].apply(lambda x: month_names[x - 1])

# Filter data for the years 2011 and 2012
data_2011 = data[data['yr'] == 0]  # 0 represents the year 2011
data_2012 = data[data['yr'] == 1]  # 1 represents the year 2012

# Sidebar filter for months
selected_months = st.sidebar.multiselect('Pilih Bulan', month_names, default=month_names)

# Filter data based on selected months
data_2011_filtered = data_2011[data_2011['month_name'].isin(selected_months)]
data_2012_filtered = data_2012[data_2012['month_name'].isin(selected_months)]

# Group data by month and calculate total rentals for each month
monthly_data_2011 = data_2011_filtered.groupby('mnth')['cnt'].sum().reset_index()
monthly_data_2011['month_name'] = monthly_data_2011['mnth'].apply(lambda x: month_names[x - 1])

monthly_data_2012 = data_2012_filtered.groupby('mnth')['cnt'].sum().reset_index()
monthly_data_2012['months'] = monthly_data_2012['mnth'].apply(lambda x: month_names[x - 1])

# Scatter and line plot for 2011
scatter_chart_2011 = alt.Chart(monthly_data_2011).mark_circle(size=60, color='blue').encode(
    x=alt.X('months', title='Month', sort=month_names),
    y=alt.Y('cnt', title='Total Rentals'),
    tooltip=['month_name', 'cnt']
)

line_chart_2011 = alt.Chart(monthly_data_2011).mark_line(color='blue').encode(
    x=alt.X('months', title='Month', sort=month_names),
    y=alt.Y('cnt', title='Total Rentals')
)

# Scatter and line plot for 2012
scatter_chart_2012 = alt.Chart(monthly_data_2012).mark_circle(size=60, color='blue').encode(
    x=alt.X('months', title='Bulan', sort=month_names),
    y=alt.Y('cnt', title='Total Peminjaman'),
    tooltip=['month_name', 'cnt']
)

line_chart_2012 = alt.Chart(monthly_data_2012).mark_line(color='blue').encode(
    x=alt.X('months', title='Bulan', sort=month_names),
    y=alt.Y('cnt', title='Total Peminjaman')
)

# Combine scatter and line charts
combined_chart_2011 = scatter_chart_2011 + line_chart_2011
combined_chart_2012 = scatter_chart_2012 + line_chart_2012

# Create two charts side by side
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Tahun 2011")
    st.altair_chart(combined_chart_2011, use_container_width=True)

with right_column:
    st.subheader("Tahun 2012")
    st.altair_chart(combined_chart_2012, use_container_width=True)

# Menamai setiap tahun
year_mapping = {0: '2011', 1: '2012'}
data['year_name'] = data['yr'].map(year_mapping)
year_rentals = data.groupby('year_name')['cnt'].sum()

fig, ax = plt.subplots(figsize=(4,4))
ax.pie(year_rentals, labels=year_rentals.index, autopct='%1.1f%%', startangle=90, colors=['#4D77FF','#FF9999','#66FF66','#FFCC66'])
ax.set_title('Distribusi Peminjaman Sepeda Setiap Tahun')
ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
st.pyplot(fig)

st.markdown("""
Peminjaman terbanyak terdapat pada tahun 2012 sebanyak 2049576 pengguna
""")

# Question 4: Pada bulan apa setiap tahunnya peminjaman sepeda tertinggi?
st.header('Distribusi Peminjaman Sepeda Setiap Bulan')

# Pisahkan data berdasarkan tahun
data_2011 = data[data['yr'] == 0]  # 2011
data_2012 = data[data['yr'] == 1]  # 2012

# Agregasi peminjaman sepeda berdasarkan bulan untuk setiap tahun
rentals_2011 = data_2011.groupby('mnth')['cnt'].sum()
rentals_2012 = data_2012.groupby('mnth')['cnt'].sum()

# Labels for months
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Membuat dua pie chart bersebelahan
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Pie chart untuk tahun 2011
ax1.pie(rentals_2011, labels=months, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax1.set_title('Distribusi Peminjaman Sepeda Tahun 2011')
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Pie chart untuk tahun 2012
ax2.pie(rentals_2012, labels=months, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax2.set_title('Distribusi Peminjaman Sepeda Tahun 2012')
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig)
st.markdown("""
Peminjaman terbanyak terdapat pada bulan Juni untuk tahun 2011 dan bulan September untuk tahun 2012
""")

# Membuat kesimpulan
st.header("Conclusion")
st.markdown("""
- Conclution pertanyaan 1: Dapat disimpulkan bahwa suhu memiliki pengaruh terhadap total peminjaman sepeda. Sebagaimana pada grafik yang telah dibuat, total pengguna sepeda meningkat seiring bertambahnya suhu hingga binning ke 8 dan menurun pada binning 9 dan 10. Hal ini menunjukkan pengguna sepeda lebih memilih meminjam sepeda ketika suhunya hangat, tetapi juga tidak terlalu panas.
- Conclution pertanyaan 2: Dapat disimpulkan bahwa sebagian besar pengguna sepeda lebih memilih menggunakan sepeda pada musim gugur, sebagaimana yang ditunjukkan pada grafik distribusi peminjaman sepeda lintas musim, dengan persentase penggunanya sebesar 32.2%.
- Conclution pertanyaan 3: Dapat disimpulkan bahwa peminjaman sepeda pada tahun 2012 jauh meningkat dibanding tahun 2011 dengan total peminjaman pada tahun 2011 sebesar 1243103 dan pada tahun 2012 sebesar 2049576.
- Conclution pertanyaan 4: Dapat disimpulkan bahwa peminjaman tertinggi pada tahun 2011 terjadi pada bulan Juni sebanyak 638 pengguna dan pada bulan September pada tahun 2012 sebanyak 977 pengguna.
""")

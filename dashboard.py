import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk menghitung jumlah pelanggan aktif dan kurang aktif
def get_customers_status(orders, customers):
    active_customer = orders['customer_id'].drop_duplicates().reset_index(drop=True)
    inactive_customer = customers[~customers['customer_id'].isin(active_customer)]['customer_id'].reset_index(drop=True)
    return active_customer, inactive_customer

# Fungsi untuk menghitung jumlah pelanggan aktif dan kurang aktif per kota
def get_cities_status(orders, customers, inactive_customer):
    active_customer_city = orders.groupby('customer_city')['customer_id'].nunique().sort_values(ascending=False)
    inactive_customer_city = customers[customers['customer_id'].isin(inactive_customer)].groupby('customer_city')['customer_id'].nunique().sort_values(ascending=False)
    return active_customer_city, inactive_customer_city

# Fungsi untuk menghitung jumlah pelanggan aktif dan kurang aktif per negara bagian
def get_states_status(orders, customers, inactive_customer):
    active_customer_state = orders.groupby('customer_state')['customer_id'].nunique().sort_values(ascending=False)
    inactive_customer_state = customers[customers['customer_id'].isin(inactive_customer)].groupby('customer_state')['customer_id'].nunique().sort_values(ascending=False)
    return active_customer_state, inactive_customer_state

# Memuat data
df_customers = pd.read_csv('customers_final.csv')
df_order_customer = pd.read_csv('order_customer_2018_final.csv')
df_order_customer['order_purchase_timestamp'] = pd.to_datetime(df_order_customer['order_purchase_timestamp']).dt.date

# Sidebar rentang waktu
min_date = df_order_customer['order_purchase_timestamp'].min()
max_date = df_order_customer['order_purchase_timestamp'].max()

with st.sidebar:
    st.image("k-logo.png")
    start_date, end_date = st.date_input('Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date])

# Filter berdasarkan rentang tanggal
df_order_customer_filtered = df_order_customer[(df_order_customer['order_purchase_timestamp'] >= start_date) &
                                               (df_order_customer['order_purchase_timestamp'] <= end_date)]

# Menghitung jumlah pelanggan aktif dan kurang aktif
active_customer, inactive_customer = get_customers_status(df_order_customer_filtered, df_customers)
active_customer_city, inactive_customer_city = get_cities_status(df_order_customer_filtered, df_customers, inactive_customer)
active_customer_state, inactive_customer_state = get_states_status(df_order_customer_filtered, df_customers, inactive_customer)

# Visualisasi 1: Pie Chart untuk Pelanggan Aktif vs Kurang Aktif
st.subheader('Perbandingan Jumlah Pelanggan Aktif Dan Pelanggan Kurang Aktif Tahun 2018')
st.write(f'Rentang Waktu: {start_date} - {end_date}')

labels = [f'Aktif: \n{len(active_customer)} customer', f'Kurang Aktif: \n{len(inactive_customer)} customer']
sizes = [len(active_customer), len(inactive_customer)]
colors = ['#44AA44', '#FF4444']

fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.pie(sizes, labels=labels, autopct='%.2f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
st.pyplot(fig1)

# Visualisasi 2: Bar Chart untuk 5 Kota Teratas
st.subheader('5 Kota Teratas dengan Pelanggan Aktif dan Kurang Aktif Tahun 2018')
st.write(f'Rentang Waktu: {start_date} - {end_date}')

top_active_customer_city = active_customer_city.head(5)
top_inactive_customer_city = inactive_customer_city.head(5)
max_ytick_city = max(top_active_customer_city.max(), top_inactive_customer_city.max())

fig2, axs2 = plt.subplots(1, 2, figsize=(14, 6))

# Kota Aktif
bars_city_active = axs2[0].bar(top_active_customer_city.index, top_active_customer_city.values, color='#44AA44')
axs2[0].set_title('Kota dengan Pelanggan Aktif Terbanyak')
axs2[0].set_yticks(range(0, max_ytick_city + 1000, 1000))
axs2[0].tick_params(axis='x', rotation=45)
axs2[0].set_xlabel('Kota')
axs2[0].set_ylabel('Jumlah Pelanggan Aktif')

for bar in bars_city_active:
    yval = bar.get_height()
    axs2[0].text(bar.get_x() + bar.get_width()/2, yval, yval, va='bottom')

# Kota Inaktif
bars_city_inactive = axs2[1].bar(top_inactive_customer_city.index, top_inactive_customer_city.values, color='#FF4444')
axs2[1].set_title('Kota dengan Pelanggan Kurang Aktif Terbanyak')
axs2[1].set_yticks(range(0, max_ytick_city + 1000, 1000))
axs2[1].tick_params(axis='x', rotation=45)
axs2[1].set_xlabel('Kota')
axs2[1].set_ylabel('Jumlah Pelanggan Kurang Aktif')

for bar in bars_city_inactive:
    yval = bar.get_height()
    axs2[1].text(bar.get_x() + bar.get_width()/2, yval, yval, va='bottom')

plt.tight_layout()
st.pyplot(fig2)

# Visualisasi 3: Bar Chart untuk 5 Negara Bagian Teratas
st.subheader('5 Negara Bagian Teratas dengan Pelanggan Aktif dan Kurang Aktif Tahun 2018')
st.write(f'Rentang Waktu: {start_date} - {end_date}')

top_active_customer_state = active_customer_state.head(5)
top_inactive_customer_state = inactive_customer_state.head(5)
max_ytick_state = max(top_active_customer_state.max(), top_inactive_customer_state.max())

fig3, axs3 = plt.subplots(1, 2, figsize=(14, 6))

# Negara Bagian Aktif
bars_state_active = axs3[0].bar(top_active_customer_state.index, top_active_customer_state.values, color='#44AA44')
axs3[0].set_title('Negara Bagian dengan Pelanggan Aktif Terbanyak')
axs3[0].set_yticks(range(0, max_ytick_state + 1000, 1000))
axs3[0].tick_params(axis='x', rotation=45)
axs3[0].set_xlabel('Negara Bagian')
axs3[0].set_ylabel('Jumlah Pelanggan Aktif')

for bar in bars_state_active:
    yval = bar.get_height()
    axs3[0].text(bar.get_x() + bar.get_width()/2, yval, yval, va='bottom')

# Negara Bagian Inaktif
bars_state_inactive = axs3[1].bar(top_inactive_customer_state.index, top_inactive_customer_state.values, color='#FF4444')
axs3[1].set_title('Negara Bagian dengan Pelanggan Kurang Aktif Terbanyak')
axs3[1].set_yticks(range(0, max_ytick_state + 1000, 1000))
axs3[1].tick_params(axis='x', rotation=45)
axs3[1].set_xlabel('Negara Bagian')
axs3[1].set_ylabel('Jumlah Pelanggan Kurang Aktif')

for bar in bars_state_inactive:
    yval = bar.get_height()
    axs3[1].text(bar.get_x() + bar.get_width()/2, yval, yval, va='bottom')

plt.tight_layout()
st.pyplot(fig3)

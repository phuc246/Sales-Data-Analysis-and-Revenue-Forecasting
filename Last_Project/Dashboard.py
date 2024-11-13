import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Doanh Số Bán Hàng")

st.sidebar.header("Tùy Chọn")
uploaded_file = st.sidebar.file_uploader("Tải lên tệp CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    filename = 'D:/Cachehotroraquyetdinh/project40%/Last_Project ver 2.1/Last_Project/Sales-Reporting-main/data/'
    frames = []
    for file in os.listdir(filename):
        if file.endswith('.csv'):
            filepath = filename + file
            df1 = pd.read_csv(filepath)
            frames.append(df1)
    df = pd.concat(frames, ignore_index=True)

# Xử lý dữ liệu
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
df['Sales'] = df['Quantity Ordered'] * df['Price Each']

# Tạo cột 'Month' và 'City'
df['Month'] = df['Order Date'].dt.month
df['City'] = df['Purchase Address'].apply(lambda x: x.split(',')[1].strip() if isinstance(x, str) and ',' in x else 'Unknown')
st.subheader("Bảng Dữ Liệu")
st.dataframe(df)

# Tính toán doanh số hàng tháng
monthly_sales = df.groupby('Month')['Sales'].sum()

col1, col2, col3 = st.columns(3)

# Biểu đồ doanh số hàng tháng
with col1:
    fig1, ax1 = plt.subplots()
    ax1.bar(monthly_sales.index, monthly_sales.values)
    ax1.set_xlabel('Tháng')
    ax1.set_ylabel('Doanh Số (USD)')
    ax1.set_title('Doanh Số Hàng Tháng')
    st.pyplot(fig1)

# Biểu đồ doanh số theo thành phố
with col2:
    sales_by_city = df.groupby('City')['Sales'].sum()
    fig2, ax2 = plt.subplots()
    ax2.bar(sales_by_city.index, sales_by_city.values)
    ax2.set_xlabel('Thành Phố')
    ax2.set_ylabel('Doanh Số (USD)')
    ax2.set_title('Doanh Số Theo Thành Phố')
    ax2.tick_params(axis='x', rotation=90)
    st.pyplot(fig2)

# Biểu đồ doanh số theo giờ
with col3:
    df['Hour'] = df['Order Date'].dt.hour
    sales_by_hour = df.groupby('Hour')['Sales'].sum()
    fig3, ax3 = plt.subplots()
    ax3.plot(sales_by_hour.index, sales_by_hour.values)
    ax3.set_xlabel('Giờ')
    ax3.set_ylabel('Doanh Số (USD)')
    ax3.set_title('Doanh Số Hàng Giờ')
    ax3.grid()
    st.pyplot(fig3)

# Tạo heatmap
st.subheader("Heatmap Số Lượng Đặt Hàng theo Thành Phố và Tháng")
heatmap_data = df.pivot_table(values='Quantity Ordered', index='City', columns='Month', aggfunc='sum', fill_value=0)
fig4, ax4 = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='YlGnBu', ax=ax4)
ax4.set_title('Số Lượng Đặt Hàng theo Thành Phố và Tháng')
ax4.set_xlabel('Tháng')
ax4.set_ylabel('Thành Phố')
st.pyplot(fig4)


st.subheader("Bảng Tổng Hợp Dữ Liệu")
st.dataframe(df)


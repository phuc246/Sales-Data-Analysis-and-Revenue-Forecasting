import pandas as pd
import streamlit as st
import os
import math
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

##-----------------------------------------------------

filename = 'D:/Cachehotroraquyetdinh/project40%/Last_Project ver 2.1/Last_Project/Sales-Reporting-main/data/'
df = pd.read_csv(filename + 'sales2019_1.csv')
df = df.reset_index(drop=True)
st.subheader('Bảng Dữ Liệu Với Doanh Số 1 Tháng')
st.dataframe(df)

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

frames = []
all_length = []
for file in os.listdir(filename):
    if file.endswith('.csv'):
        filepath = filename + file
        df1 = pd.read_csv(filepath)
        frames.append(df1)
        result = pd.concat(frames)
        length_1month = len(df1.index)
        all_length.append(length_1month)

result.to_csv('annualSales2020.csv', index=False)

df_annual = pd.read_csv('D:/Cachehotroraquyetdinh/project40%/Last_Project ver 2.1/Last_Project/annualSales2020.csv')
st.subheader('Bảng Dữ Liệu Gộp 12 Tháng')
st.dataframe(df_annual)

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

df_annual['Month'] = df_annual['Order Date'].str[0:2]
df_annual = df_annual.dropna(how='all')
df_annual = df_annual[df_annual['Month'] != 'Or']
st.subheader('Bảng Dữ Liệu Định Dạng Thời Gian')
st.dataframe(df_annual)

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

df_annual['Quantity Ordered'] = pd.to_numeric(df_annual['Quantity Ordered'], downcast='integer')
df_annual['Price Each'] = pd.to_numeric(df_annual['Price Each'], downcast='float')
df_annual['Sales'] = df_annual['Quantity Ordered'] * df_annual['Price Each']
moving_column = df_annual.pop('Sales')
df_annual.insert(4, 'Sales', moving_column)
st.subheader('Thêm cột Sales')
st.dataframe(df_annual)

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.subheader('Bảng Dữ Liệu với Tổng Sales Mỗi Tháng')
df_annual.groupby('Month').sum()['Sales']
sales_value = df_annual.groupby('Month').sum()['Sales']
months = range(1,13)

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

plt.bar(x=months, height=sales_value)
plt.xticks(months)
plt.xlabel('Months')
plt.ylabel('Sales in USD')
plt.title('Doanh Số Hàng Tháng')
st.pyplot(plt)
plt.clf()

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

address_to_city = lambda address:address.split(',')[1]

df_annual['City'] = df_annual['Purchase Address'].apply(address_to_city)
st.subheader('Bảng Dữ Liệu Với Tổng Sales Theo Khu Vực')
df_annual.groupby('City').sum()['Sales']
sales_value_city = df_annual.groupby('City').sum()['Sales']

cities = [city for city, sales in sales_value_city.items()]

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

plt.bar(x=cities, height=sales_value_city)
plt.xticks(cities, rotation=90, size=8)
plt.xlabel('Cities')
plt.ylabel('Sales in USD')
plt.show()
plt.title('Doanh Số Theo Thành Phố')
st.pyplot(plt)
plt.clf()

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

df_annual['Order Date'] = pd.to_datetime(df_annual['Order Date'])
df_annual['Hours'] = df_annual['Order Date'].dt.hour
st.subheader('Bảng Dữ Liệu Với Số Lượng Đặt Hàng Mỗi Khung Giờ')
sales_value_hours = df_annual.groupby('Hours').count()['Sales']
hours = [hour for hour, sales in sales_value_hours.items()]

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

plt.plot(hours, sales_value_hours)
plt.grid()
plt.xticks(hours, rotation=90, size=8)
plt.xlabel('Hours')
plt.ylabel('Sales in USD')
plt.show()
plt.title('Doanh Số Hàng Giờ')
st.pyplot(plt)
plt.clf()

###---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

all_products = df_annual.groupby('Product').sum(numeric_only=True)['Quantity Ordered']
prices = df_annual.groupby('Product').mean(numeric_only=True)['Price Each']
products_ls = [product for product, quant in all_products.items()]

x = products_ls
y1 = all_products
y2 = prices

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(x, y1, color='g')
ax2.plot(x, y2, 'b-')

ax1.set_xticklabels(products_ls, rotation=90, size=8)
ax1.set_xlabel('Products')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price Each', color='b')
plt.title('Mối Quan Hệ giữa Giá và Số Lượng Đặt Hàng')
plt.show()

st.pyplot(plt)
plt.clf()

###---------------------------------------------
# Chuyển đổi cột 'Order Date' sang kiểu datetime
df_annual['Order Date'] = pd.to_datetime(df_annual['Order Date'], errors='coerce')
st.subheader('Bảng Dữ Liệu Sau Khi Chuyển Đổi Cột Order Date')
st.dataframe(df_annual)  
# Lấy Tháng và Năm
df_annual['Month'] = df_annual['Order Date'].dt.month 
df_annual['Year'] = df_annual['Order Date'].dt.year    
st.subheader('Bảng Dữ Liệu Với Thông Tin Tháng và Năm')
st.dataframe(df_annual[['Order Date', 'Month', 'Year', 'Sales']]) 
###---------------------------------------------
# Tạo cột 'City' từ 'Purchase Address's
def extract_city(address):
    # Kiểm tra xem địa chỉ có phải là chuỗi và có chứa dấu phẩy không
    if isinstance(address, str) and ',' in address:
        return address.split(',')[1].strip() 
    return 'Unknown'  

# Áp dụng hàm extract_city để tạo cột 'City'
df_annual['City'] = df_annual['Purchase Address'].apply(extract_city)
st.subheader('Bảng Dữ Liệu Với Thông Tin Thành Phố')
st.dataframe(df_annual[['Order Date', 'Month', 'Year', 'City', 'Sales']]) 

###---------------------------------------------
df_annual['Price Each'] = pd.to_numeric(df_annual['Price Each'], errors='coerce')  # Chuyển đổi giá thành số
df_annual['Quantity Ordered'] = pd.to_numeric(df_annual['Quantity Ordered'], errors='coerce')  # Chuyển đổi số lượng thành số

# Hiển thị bảng với thông tin thành phố
st.subheader('Bảng Dữ Liệu Với Thông Tin Thành Phố và Các Cột Đã Chuyển Đổi')
st.dataframe(df_annual[['Order Date', 'Month', 'Year', 'City', 'Price Each', 'Quantity Ordered', 'Sales']])  
st.dataframe(df_annual)
###---------------------------------------------
# Tạo biểu đồ hình tròn cho doanh số theo thành phố
sales_value_city = df_annual.groupby('City')['Quantity Ordered'].sum().dropna()  

# Vẽ biểu đồ hình tròn
st.markdown("<br>", unsafe_allow_html=True)  
plt.figure(figsize=(10, 6))  
plt.pie(sales_value_city, labels=sales_value_city.index, autopct='%1.1f%%', startangle=140)  
plt.title('Tỷ lệ Doanh Số theo Thành Phố')  
plt.axis('equal')  
st.pyplot(plt)  
plt.clf()  
###---------------------------------------------

# Nhóm theo giá và tính tổng số lượng đặt hàng
price_quantity = df_annual.groupby('Price Each')['Quantity Ordered'].sum().reset_index()
st.subheader('Tổng Số Lượng Đặt Hàng Theo Giá')
st.dataframe(price_quantity)  
###---------------------------------------------
# Vẽ biểu đồ đơn giản
st.markdown("<br>", unsafe_allow_html=True)  
plt.figure(figsize=(10, 6)) 

# Vẽ biểu đồ đơn giản
plt.plot(price_quantity['Price Each'], price_quantity['Quantity Ordered'], marker='o', linestyle='-', color='b', alpha=0.7)

plt.title('Mối Quan Hệ giữa Giá và Số Lượng Đặt Hàng') 
plt.xlabel('Giá Mỗi Sản Phẩm (USD)')  
plt.ylabel('Số Lượng Đặt Hàng') 
plt.grid()  
plt.xticks(rotation=65, size=10)# Thêm nhãn trục x với độ nghiêng và kích thước

# Hiển thị giá trị tại các điểm
for i in range(len(price_quantity)):
    plt.text(price_quantity['Price Each'].iloc[i], price_quantity['Quantity Ordered'].iloc[i], 
             f"{price_quantity['Quantity Ordered'].iloc[i]}", 
             fontsize=12, ha='center', va='bottom')  
st.pyplot(plt) 
plt.clf()  
###---------------------------------------------


# Tạo bảng tổng hợp số lượng theo thành phố và tháng
heatmap_data = df_annual.pivot_table(values='Quantity Ordered', index='City', columns='Month', aggfunc='sum', fill_value=0)
st.dataframe(heatmap_data)

# Vẽ biểu đồ heatmaps
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='YlGnBu') 
plt.title('Số Lượng Đặt Hàng theo Thành Phố và Tháng')
plt.xlabel('Tháng')
plt.ylabel('Thành Phố')
st.pyplot(plt)
plt.clf()

###---------------------------------------------
# Đảm bảo rằng cột 'Order Date' đã được chuyển đổi đúng
df_annual['Order Date'] = pd.to_datetime(df_annual['Order Date'], errors='coerce')
df_annual['Sales'] = df_annual['Quantity Ordered'] * df_annual['Price Each']  # Tính doanh số
daily_sales = df_annual.groupby(df_annual['Order Date'].dt.date)['Sales'].sum()  # Nhóm theo ngày và tính tổng doanh số

# Vẽ biểu đồ cột cho doanh số hàng ngày
plt.figure(figsize=(12, 6))
plt.bar(daily_sales.index, daily_sales.values, color='skyblue')
plt.title('Doanh Số Hàng Ngày')
plt.xlabel('Ngày')
plt.ylabel('Doanh Số (USD)')
plt.xticks(rotation=45)
plt.grid(axis='y')
st.pyplot(plt)
plt.clf()

###---------------------------------------------
df_annual['Sales'] = df_annual['Quantity Ordered'] * df_annual['Price Each']  # Tính doanh số
monthly_sales = df_annual.groupby('Month')['Sales'].sum()  # Nhóm theo tháng và tính tổng doanh số
monthly_change = monthly_sales.pct_change() * 100# Tính tỷ lệ thay đổi doanh số hàng tháng

# Chuyển đổi tỷ lệ thay đổi thành DataFrame
monthly_change_df = monthly_change.reset_index()
monthly_change_df.columns = ['Month', 'Monthly Change (%)']
print(monthly_change_df) 

df_annual = df_annual.merge(monthly_change_df, on='Month', how='left')

# Tính tổng doanh số hàng tháng cho df_annual
monthly_totals = df_annual.groupby('Month')['Sales'].sum().reset_index()
monthly_totals.columns = ['Month', 'Total Monthly Sales']


df_annual = df_annual.merge(monthly_totals, on='Month', how='left')# Gộp tổng doanh số hàng tháng vào df_annual
df_annual['Monthly Change (%)'] = df_annual['Monthly Change (%)'].fillna(0).round(2)# Định dạng lại để hiển thị phần trăm tăng/giảm
df_annual['Change Color'] = df_annual['Monthly Change (%)'].apply(lambda x: 'green' if x > 0 else ('red' if x < 0 else 'black'))
columns_to_display = ['Month', 'Monthly Change (%)', 'Total Monthly Sales']
st.dataframe(df_annual[columns_to_display])

###---------------------------------------------
df_annual['Sales'] = df_annual['Quantity Ordered'] * df_annual['Price Each']  # Tính doanh số
monthly_sales = df_annual.groupby('Month')['Sales'].sum().reset_index(name='Total Monthly Sales')  # Tính tổng doanh số
monthly_change = monthly_sales['Total Monthly Sales'].pct_change() * 100  # Tính tỷ lệ thay đổi
monthly_sales['Monthly Change (%)'] = monthly_change.fillna(0).round(2)  
# Định dạng màu sắc cho phần trăm thay đổi
monthly_sales['Change Color'] = monthly_sales['Monthly Change (%)'].apply(lambda x: 'green' if x > 0 else ('red' if x < 0 else 'black'))
st.subheader('Doanh Số Hàng Tháng và Tỷ Lệ Thay Đổi')
st.dataframe(monthly_sales)

###---------------------------------------------
# Tạo danh sách màu sắc cho các cột
colors = ['green' if change > 0 else 'red' for change in monthly_change]

# Vẽ biểu đồ tỷ lệ thay đổi
plt.figure(figsize=(10, 6))
plt.bar(monthly_change.index, monthly_change, color=colors)
plt.title('Tỷ Lệ Thay Đổi Doanh Số Hàng Tháng')
plt.xlabel('Tháng')
plt.ylabel('Tỷ Lệ Thay Đổi (%)')
plt.axhline(0, color='black', lw=1)  
plt.xticks(monthly_change.index)  
plt.grid(axis='y')  
st.pyplot(plt)
plt.clf()
###---------------------------------------------
# Bảng tổng hợp
st.subheader("Bảng tổng hợp")
st.dataframe(df_annual)

# Lưu DataFrame thành tệp CSV
csv = df_annual.to_csv(index=False).encode('utf-8')

# Tạo nút tải xuống
st.download_button(
    label="Tải xuống bảng tổng hợp",
    data=csv,
    file_name='summary_data.csv',
    mime='text/csv',
)

###---------------------------------------------
df_annual['Order Date'] = pd.to_datetime(df_annual['Order Date'], errors='coerce') 
df_annual['Month'] = df_annual['Order Date'].dt.month

# Xóa các hàng có tất cả các giá trị NaN
df_annual = df_annual.dropna(how='all')

# Chuyển đổi Số lượng đặt hàng và Giá mỗi loại sang dạng số
df_annual['Quantity Ordered'] = pd.to_numeric(df_annual['Quantity Ordered'], downcast='integer')
df_annual['Price Each'] = pd.to_numeric(df_annual['Price Each'], downcast='float')

# Tính toán doanh số
df_annual['Sales'] = df_annual['Quantity Ordered'] * df_annual['Price Each']
monthly_sales = df_annual.groupby('Month')['Sales'].sum()  # Tổng doanh số được nhóm theo tháng
# Kiểm tra thay đổi hàng tháng
monthly_change = monthly_sales.pct_change() * 100 # Tính toán phần trăm thay đổi
monthly_change = monthly_change.fillna(0)  # Thay thế NaN bằng 0


# fig1: Doanh số hàng tháng
fig1, ax1 = plt.subplots()
ax1.bar(x=monthly_sales.index, height=monthly_sales)  
ax1.set_xlabel('Months')
ax1.set_ylabel('Sales in USD')
ax1.set_title('Monthly Sales')

# fig2: Bán theo Thành phố
sales_value_city = df_annual.groupby('City')['Sales'].sum()  # Nhóm theo Thành phố và tổng Doanh số
cities = sales_value_city.index
fig2, ax2 = plt.subplots()
ax2.bar(x=cities, height=sales_value_city)
ax2.set_xlabel('Cities')
ax2.set_ylabel('Sales in USD')
ax2.set_title('Sales by City')
ax2.tick_params(axis='x', rotation=90)

# fig3: Bán hàng theo giờ
df_annual['Hours'] = df_annual['Order Date'].dt.hour  
sales_value_hours = df_annual.groupby('Hours')['Sales'].sum() 
hours = sales_value_hours.index
fig3, ax3 = plt.subplots()
ax3.plot(hours, sales_value_hours)
ax3.set_xlabel('Hours')
ax3.set_ylabel('Sales in USD')
ax3.set_title('Hourly Sales')
ax3.grid()

# fig4: Mối quan hệ giữa giá và số lượng
all_products = df_annual.groupby('Product')['Quantity Ordered'].sum()
prices = df_annual.groupby('Product')['Price Each'].mean()
products_ls = all_products.index
fig4, ax4 = plt.subplots()
ax4.bar(products_ls, all_products, color='g')
ax4.set_xlabel('Products')
ax4.set_ylabel('Quantity Ordered')
ax4.tick_params(axis='x', rotation=90)
ax4_twin = ax4.twinx()
ax4_twin.plot(products_ls, prices, 'b-')
ax4_twin.set_ylabel('Price Each', color='b')
ax4.set_title('Relationship between Price and Quantity Ordered')

# fig5: Biểu đồ tròn cho doanh số theo thành phố
fig5, ax5 = plt.subplots()
sales_value_city = df_annual.groupby('City')['Quantity Ordered'].sum().dropna()
ax5.pie(sales_value_city, labels=sales_value_city.index, autopct='%1.1f%%', startangle=140)
ax5.set_title('Tỷ lệ Doanh Số theo Thành Phố')
ax5.axis('equal')

# fig6: Biểu đồ đường giá so với số lượng đặt hàng
price_quantity = df_annual.groupby('Price Each')['Quantity Ordered'].sum().reset_index()
fig6, ax6 = plt.subplots()
ax6.plot(price_quantity['Price Each'], price_quantity['Quantity Ordered'], marker='o', linestyle='-', color='b', alpha=0.7)
ax6.set_title('Mối Quan Hệ giữa Giá và Số Lượng Đặt Hàng')
ax6.set_xlabel('Giá Mỗi Sản Phẩm (USD)')
ax6.set_ylabel('Số Lượng Đặt Hàng')
ax6.grid()
plt.xticks(rotation=65, size=10)
for i in range(len(price_quantity)):
    ax6.text(price_quantity['Price Each'].iloc[i], price_quantity['Quantity Ordered'].iloc[i],
             f"{price_quantity['Quantity Ordered'].iloc[i]}",
             fontsize=12, ha='center', va='bottom')

# fig7: Heatmap
heatmap_data = df_annual.pivot_table(values='Quantity Ordered', index='City', columns='Month', aggfunc='sum', fill_value=0)
fig7, ax7 = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='YlGnBu', ax=ax7)
ax7.set_title('Số Lượng Đặt Hàng theo Thành Phố và Tháng')
ax7.set_xlabel('Tháng')
ax7.set_ylabel('Thành Phố')

# fig8: Bán hàng hằng ngày
daily_sales = df_annual.groupby(df_annual['Order Date'].dt.date)['Sales'].sum()
fig8, ax8 = plt.subplots(figsize=(12, 6))
ax8.bar(daily_sales.index, daily_sales.values, color='skyblue')
ax8.set_title('Doanh Số Hàng Ngày')
ax8.set_xlabel('Ngày')
ax8.set_ylabel('Doanh Số (USD)')
plt.xticks(rotation=45)
ax8.grid(axis='y')

# fig9: Thay đổi hàng tháng
colors = ['green' if change > 0 else 'red' for change in monthly_change]
fig9, ax9 = plt.subplots(figsize=(10, 6))
ax9.bar(monthly_change.index, monthly_change, color=colors)
ax9.set_title('Tỷ Lệ Thay Đổi Doanh Số Hàng Tháng')
ax9.set_xlabel('Tháng')
ax9.set_ylabel('Tỷ Lệ Thay Đổi (%)')
ax9.axhline(0, color='black', lw=1)  
ax9.set_xticks(monthly_change.index) 
ax9.grid(axis='y') 


col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)

with col2:
    st.pyplot(fig4)
    st.pyplot(fig5)
    st.pyplot(fig6)

with col3:
    st.pyplot(fig7)
    st.pyplot(fig8)
    st.pyplot(fig9)
plt.clf()

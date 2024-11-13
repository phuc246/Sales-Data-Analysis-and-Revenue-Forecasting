import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns  
import math  

filename = 'D:/Cachehotroraquyetdinh/project40%/Last_Project ver 2.1/Last_Project/'
df_annual = pd.read_csv(filename + 'summary_data.csv')

# Tiền xử lý dữ liệu
df_annual['Quantity Ordered'] = pd.to_numeric(df_annual['Quantity Ordered'], errors='coerce')
df_annual['Price Each'] = pd.to_numeric(df_annual['Price Each'], errors='coerce')
df_annual['Sales'] = df_annual['Quantity Ordered'] * df_annual['Price Each']
features = df_annual[['Quantity Ordered', 'Price Each', 'Month']] 
target = df_annual['Sales']

# huấn luyện 
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Xây dựng mô hình hồi quy tuyến tính
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Đánh giá mô hình
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# Trực quan hóa kết quả đánh giá mô hình
st.subheader('Hiển Thị Kế Quả Đánh Giá Mô Hình')

# Trực quan hóa 2 biểu đồ trong cùng 1 hàng (2 cột)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

#Biểu đồ so sánh giá trị thực và giá trị dự đoán
ax1.scatter(y_test, y_pred, color='blue', alpha=0.6)
ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
ax1.set_xlabel('Giá trị thực tế')
ax1.set_ylabel('Giá trị dự đoán')
ax1.set_title('So sánh Giá trị Thực và Dự đoán')

# Biểu đồ residual plot (Lỗi dự đoán)
residuals = y_test - y_pred
sns.scatterplot(x=y_pred, y=residuals, color='purple', alpha=0.6, ax=ax2)
ax2.axhline(y=0, color='red', linestyle='--')
ax2.set_xlabel('Giá trị dự đoán')
ax2.set_ylabel('Lỗi (Residuals)')
ax2.set_title('Residual Plot')
# Hiển thị biểu đồ trong Streamlit
st.pyplot(fig)

# Trực quan hóa RMSE, R², và MAE
metrics = {
    'Root Mean Squared Error (RMSE)': rmse,
    'R² (Hệ số xác định)': r2,
    'Mean Absolute Error (MAE)': mae
}
fig3, ax3 = plt.subplots(figsize=(8, 5))
ax3.bar(metrics.keys(), metrics.values(), color=['skyblue', 'lightcoral', 'lightgreen'])
ax3.set_ylabel('Giá trị')
ax3.set_title('Các Chỉ Số Đánh Giá Mô Hình')
st.pyplot(fig3)

# Hiển thị kết quả đánh giá mô hình
st.subheader('Kết quả Dự đoán')
st.write(f'Root Mean Squared Error (RMSE): {rmse:.2f}')
st.write(f'R² (Hệ số xác định): {r2:.2f}')
st.write(f'Mean Absolute Error (MAE): {mae:.2f}')

# Chọn tháng
st.subheader('Dự đoán Doanh Thu theo Tháng')
month = st.selectbox('Chọn tháng (1-12)', options=list(range(1, 13)))

# Lọc dữ liệu theo tháng đã chọn
df_month = df_annual[df_annual['Month'] == month]
product_list = df_month['Product'].unique()  

# Dự đoán doanh thu cho từng sản phẩm trong tháng
st.subheader(f"Doanh thu dự đoán cho các sản phẩm trong tháng {month}")

total_revenue = 0  
predicted_revenues = []  
products = []  
predicted_quantities = []  

for product in product_list:
    # Lọc dữ liệu sản phẩm và lấy giá mỗi sản phẩm
    selected_product_data = df_month[df_month['Product'] == product]
    price_each = selected_product_data['Price Each'].iloc[0]
    quantity_ordered = selected_product_data['Quantity Ordered'].sum()  # Lấy tổng số lượng đặt hàng trong tháng đó
    
    # Dự đoán doanh thu cho sản phẩm
    month_data = pd.DataFrame([[quantity_ordered, price_each, month]], columns=['Quantity Ordered', 'Price Each', 'Month'])
    prediction = model.predict(month_data)
    predicted_revenue = prediction[0]
    total_revenue += predicted_revenue
    
    # Tính số lượng cần nhập cho sản phẩm (Doanh thu dự đoán / Giá mỗi sản phẩm)
    predicted_quantity = predicted_revenue / price_each
    
    # Làm tròn số lượng cần nhập lên
    predicted_quantity_ceil = math.ceil(predicted_quantity)
   
    predicted_revenues.append(predicted_revenue)
    products.append(product)
    predicted_quantities.append(predicted_quantity_ceil)

    # Hiển thị kết quả dự đoán cho từng sản phẩm
    #st.write(f'Dự đoán doanh thu cho sản phẩm "{product}": ${predicted_revenue:.2f}')
    #st.write(f'Số lượng cần nhập cho sản phẩm "{product}": {predicted_quantity_ceil} sản phẩm')

# Hiển thị tổng doanh thu cho tất cả các sản phẩm trong tháng
st.write(f'Tổng doanh thu dự đoán cho tháng {month}: ${total_revenue:.2f}')

# Trực quan hóa kết quả Doanh Thu Dự Đoán: Biểu đồ cột
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(products, predicted_revenues, color='skyblue')

# Thêm số vào các cột
for bar in bars:
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2, f'${bar.get_width():.2f}', 
            va='center', ha='left', fontsize=10, color='black')

ax.set_xlabel('Doanh Thu Dự Đoán (USD)')
ax.set_title(f'Dự Đoán Doanh Thu cho Các Sản Phẩm trong Tháng {month}')
ax.set_xlim(0, max(predicted_revenues) * 1.1)  # Đặt giới hạn trục X phù hợp

st.pyplot(fig)

fig2, ax2 = plt.subplots(figsize=(10, 6))
bars2 = ax2.barh(products, predicted_quantities, color='lightgreen')

# Thêm số vào các cột
for bar in bars2:
    ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.0f}', 
             va='center', ha='left', fontsize=10, color='black')

ax2.set_xlabel('Số Lượng Cần Nhập')
ax2.set_title(f'Dự Đoán Số Lượng Cần Nhập Cho Mỗi Sản Phẩm trong Tháng {month}')
ax2.set_xlim(0, max(predicted_quantities) * 1.1)  # Đặt giới hạn trục X phù hợp

st.pyplot(fig2)

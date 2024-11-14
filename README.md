# Sales-Data-Analysis-and-Revenue-Forecasting
### Phân Tích Dữ Liệu Doanh Số và Dự Đoán Doanh Thu
Dự án này thực hiện phân tích dữ liệu doanh số và cung cấp các biểu đồ trực quan sử dụng **Streamlit**, **Pandas**, **Matplotlib**, và **Seaborn**. Mục tiêu là rút ra các thông tin quan trọng từ dữ liệu doanh số, hiển thị xu hướng và cho phép người dùng tương tác với kết quả thông qua giao diện web.

## Tổng Quan Dự Án

Repo này chứa một tập lệnh Python thực hiện các công việc sau:

- Tải và xử lý dữ liệu doanh số từ các tệp CSV.
- Làm sạch và chuẩn bị dữ liệu cho phân tích.
- Hiển thị các xu hướng doanh số theo tháng, thành phố, sản phẩm, giờ trong ngày và nhiều yếu tố khác.
- Cung cấp các biểu đồ và đồ thị trực quan thông qua giao diện web của Streamlit.
- Cho phép người dùng tải xuống bộ dữ liệu đã xử lý dưới dạng tệp CSV.
- Xây dựng mô hình hồi quy tuyến tính để dự đoán doanh thu và số lượng sản phẩm cần nhập.

## Các Tính Năng

### 1. **Tải Dữ Liệu và Tiền Xử Lý**
- Kết hợp nhiều tệp CSV thành một DataFrame duy nhất cho dữ liệu doanh số hàng năm.
- Chuyển đổi các cột ngày tháng sang định dạng datetime và trích xuất thông tin tháng và năm.
- Chuyển đổi các cột số lượng sản phẩm và giá thành sang kiểu số để tính toán chính xác.
- Tính toán tổng doanh số cho mỗi dòng dữ liệu và thêm cột này vào DataFrame.

### 2. **Biểu Đồ và Trực Quan Hóa**
- **Doanh Số Theo Tháng**: Hiển thị biểu đồ cột cho doanh số theo từng tháng.
- **Doanh Số Theo Thành Phố**: Cung cấp biểu đồ tròn và cột cho tổng doanh số theo thành phố.
- **Doanh Số Theo Giờ**: Hiển thị doanh số theo từng giờ trong ngày bằng biểu đồ đường.
- **Phân Tích Sản Phẩm**: Kết hợp biểu đồ cột và đường để khảo sát mối quan hệ giữa giá sản phẩm và số lượng đặt hàng.
- **Thay Đổi Doanh Số**: Phân tích và hiển thị phần trăm thay đổi doanh số hàng tháng.
- **Heatmap**: Hiển thị heatmap cho số lượng đơn hàng theo thành phố và tháng.
- **Doanh Số Hàng Ngày**: Hiển thị doanh số hàng ngày bằng biểu đồ cột.
- **Doanh Số Theo Sản Phẩm**: Hiển thị mối quan hệ giữa giá sản phẩm và số lượng đặt hàng.

### 3. **Tính Năng Tương Tác**
- Cho phép người dùng tải xuống bộ dữ liệu đã xử lý dưới dạng tệp CSV để phân tích thêm.
- Sử dụng Streamlit để tạo giao diện web động cho phép người dùng tương tác và khám phá dữ liệu doanh số.

### 4. **Tính Năng Nâng Cao**
- **Mô Hình Hồi Quy Tuyến Tính**: Huấn luyện mô hình hồi quy tuyến tính để dự đoán doanh thu cho các sản phẩm dựa trên số lượng đặt hàng, giá thành và tháng.
- **Dự Đoán Doanh Thu Theo Tháng**: Cho phép người dùng chọn tháng và dự đoán doanh thu cho các sản phẩm trong tháng đó.
- **Dự Đoán Số Lượng Cần Nhập**: Tính toán số lượng sản phẩm cần nhập dựa trên doanh thu dự đoán.

## Cài Đặt

Để chạy dự án này trên máy tính cá nhân, bạn có thể làm theo các bước sau:

### 1. Clone Repository:
Clone repository về máy của bạn:
```bash
git clone https://github.com/your-username/sales-data-analysis.git
cd sales-data-analysis
```
### 2. Cài Đặt Các Thư Viện:
Bạn cần cài đặt Python 3.7+ và các thư viện cần thiết.

Cài đặt thông qua pip với tệp requirements.txt:

```bash
pip install -r requirements.txt
Nếu không có tệp requirements.txt, bạn có thể cài đặt thủ công các thư viện:
```
```bash
pip install pandas matplotlib seaborn streamlit scikit-learn
```
### 3. Chạy Ứng Dụng Streamlit:
Sau khi cài đặt xong các thư viện, bạn có thể chạy ứng dụng Streamlit bằng lệnh sau:
```bash
streamlit run app.py
```
## Cấu Trúc Dự Án
```css
/Last_Project
│
├── Dashboard.py                         # Hệ thống tự động phân tích
├── last_project.txt                     # Phân tích và trực quan hoá
├── last_project_linear_regression.py    # Dự đoán dữ liệu có sẵn
├── annualSales2020.csv                  # Bảng tổng hợp 12 tháng
├── summary_data.csv                     # Bảng tổng hợp phân tích  
└── Sales-Reporting-main/
        └── data/                        # Thư mục chứa các tệp CSV dữ liệu doanh số 12 tháng
            └── sales2019_1-12 
```
## Tệp summary_data.csv
Tệp dữ liệu CSV này chứa thông tin về các đơn hàng, bao gồm các cột:

- Order Date: Ngày và giờ của đơn hàng.
- Product: Tên sản phẩm.
- Quantity Ordered: Số lượng sản phẩm được đặt.
- Price Each: Giá mỗi sản phẩm.
- Month: Tháng của đơn hàng.
  
## Ví Dụ Tệp CSV (summary_data.csv)
```csv
Order Date,Product,Quantity Ordered,Price Each,Purchase Address,Month
01/01/2019 10:01 AM,Product A,3,20.00,1234 Elm St, New York, NY,1
01/01/2019 11:25 AM,Product B,2,15.00,5678 Oak Rd, Los Angeles, CA,1
01/02/2019 09:15 AM,Product C,5,30.00,2345 Pine Ave, Chicago, IL,2
```
## Kết Quả
Sau khi chạy ứng dụng, bạn sẽ thấy một dashboard Streamlit với các phần sau:
- Một bảng hiển thị dữ liệu doanh số.
- Các biểu đồ như biểu đồ cột, đường, tròn, và heatmap.
- Biểu đồ so sánh giá trị thực tế và giá trị dự đoán từ mô hình hồi quy tuyến tính.
- Biểu đồ residual plot (Lỗi dự đoán).
- Biểu đồ các chỉ số đánh giá mô hình như RMSE, R², MAE.
- Dự đoán doanh thu cho các sản phẩm trong tháng đã chọn và số lượng cần nhập cho mỗi sản phẩm.

## Hướng Dẫn Sử Dụng
Người dùng có thể lọc và tương tác với dữ liệu thông qua các widget của Streamlit và khám phá các biểu đồ khác nhau như:
- Doanh số theo thành phố.
- Xu hướng doanh số theo tháng.
- Doanh số theo giờ.
- Dự đoán doanh thu theo tháng và số lượng cần nhập cho sản phẩm.
- Bộ dữ liệu đã xử lý có thể được tải xuống dưới dạng tệp CSV để phân tích thêm.

## Cộng Tác
Chào đón các đóng góp và cải tiến cho dự án! Bạn có thể fork repo này, báo cáo vấn đề, hoặc tạo pull request.

## Giấy Phép
Dự án này được cấp phép theo Giấy Phép MIT - xem chi tiết tại LICENSE.

'''
template
+ mô tả thí nghiệm ( nội dung - text)
+ thiết lập thí nghiệm (hình ảnh - đường dẫn)
+ bảng số liệu
    - cần thu thập bao nhiêu dữ liệu (list)
    - dữ liệu cột nào sẽ được thu thập từ thiết bị đo (list index) 
    - dữ liệu cột nào sẽ được thu thập thông qua nhập tay (list index) 
+ đồ thị
   - cột nào từ bảng số liệu sẽ được vẽ thành đồ thị (list - 2 ptu)

'''


exp_temp = {
        "name": "Định luật 2 newton",
        "desc": '''Tiến hành:
Bước 1: Lực kéo F có độ lớn tăng dần 1 N, 2 N và 3 N (bằng cách móc thêm các quả nặng vào đầu dây vắt qua ròng rọc). 
Bước 2: Ghi vào Bảng 15.1 độ lớn lực kéo F và tổng khối lượng của hệ (gồm xe trượt và các quả nặng đặt vào xe), ứng với mỗi lần thí nghiệm.
Bước 3: Do thời gian chuyển động của xe; đồng hồ bắt đầu đếm từ lúc tám chân sáng đi qua cổng quang điện 1 và kết thúc đêm khi tấm chắn vượt qua cổng quang điện 2.
Bước 4: Gia tốc a được tính từ công thức: a = v0*t + 1/2*a*t^2 (đặt xe trượt có gắn tấm chấn sáng sao cho tấm chắn này sát với cổng quang điện 1 để v = 0; s= 0,5 m là khoảng cách giữa hai cổng quang điện trong thí nghiệm). Đo thời gian túng với mỗi làn thí nghiệm.

Thảo luận:
a) Dựa vào số liệu trong Bảng 15.1, hãy vẽ đồ thị chỉ sự phụ thuộc của gia tốc a:
- Vào F (ứng với m + M = 0,5 kg), (Hình 15.3a). Đô thị có phải là đường tháng không? Tại sao?
- Vào 1 m+M (ứng với F - 1 N), đồ thị có phải là đường thẳng không? Tại sao?
b) Nếu kết luận về sự phụ thuộc của gia tốc vào độ lớn của lực tác dụng và khối lượng
của vật.''',
        "img": "assets//img1.png",
        "table_data": {
            "headers": ["Lần thử", "Lực kéo (lt)", "Khối lượng", "Thời gian", "Quãng đường", "Gia tốc"],
            "measuring_data": 3,
            "input_data": [1, 2, 4],
            "calucating_data": {"5": {
                    "formula": "(2*{})/({}*{})",
                    "attrs": [4, 3, 3]
                }
            },
        },
        "plot": {
            "name": "Đồ thị F-a",
            "x_name": "Lực kéo F (N)",
            "y_name": "Gia tốc a (m/s)",
            "x_data": 1,
            "y_data": 5,
        }
    }
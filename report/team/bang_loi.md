# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: ... · Người gắn nhãn 2: ... (gắn trong 8 phút, không trao đổi)

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Do người dùng | Có | Do người dùng |
| 2 | Hệ thống | Hệ thống | Có | Hệ thống |
| 3 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 4 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 5 | Ngầm | Ngầm | Có | Ngầm |
| 6 | Do người dùng | Hệ thống | Không | Do người dùng |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Hệ thống | Ngầm | Không | Hệ thống |
| 9 | Do người dùng | Do người dùng | Có | Do người dùng |
| 10 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 11 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 12 | Ngầm | Ngầm | Có | Ngầm |
| 13 | Giới hạn hệ thống | Hệ thống | Không | Giới hạn hệ thống |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Hệ thống | Không | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Hệ thống | Hệ thống | Có | Hệ thống |

**Tỉ lệ đồng thuận:** 16 / 20 = 80%

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- **Ca 6 (Do người dùng):** Gốc lỗi là khách chọn sai mục ngay từ đầu; việc trợ lý chưa đối chiếu nội dung mô tả là cải tiến nằm ở cột khắc phục.
- **Ca 8 (Hệ thống):** Trợ lý bịa điều khoản vi phạm chính sách và đã lộ ra ở nội dung gửi đi, không phải lỗi ngầm.
- **Ca 13 (Giới hạn hệ thống):** Yêu cầu thuộc sản phẩm bảo hiểm đối tác nằm ngoài phạm vi trợ lý; gắn theo nguyên nhân gốc là ngoài phạm vi dù cách từ chối chưa rõ.
- **Ca 18 (Ngữ cảnh):** Số tiền tính đúng chính sách, chỉ thiếu giải thích công thức khiến khách hiểu nhầm là hoàn thiếu.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 9 | Do người dùng | Event `input_validation_failed`; cảnh báo khi vượt 2% tổng yêu cầu/ngày | Tự nhận diện mã sàn TMĐT và tra sang mã vận đơn; nếu không tra được thì gợi ý định dạng kèm ảnh minh hoạ | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ giữa `agent_run_completed` và `refund_ledger_write` theo `trace_id`; ngưỡng cảnh báo > 0 ca lệch | Chỉ gửi thông báo "đã hoàn" khi sổ cái trả `ok`; nếu lỗi 503 sau 3 lần thì báo "đang xử lý" và chuyển nhân viên | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Tỉ lệ `ticket_reopened` có lý do khiếu nại số tiền nhưng kiểm tra sổ cái đúng; theo dõi theo tuần, ngưỡng > 1% | Cập nhật mẫu tin nhắn luôn hiển thị công thức tính chi tiết (ví dụ: `30.000 đ × 50% = 15.000 đ`) | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | Event `handoff_to_staff` với `reason = thieu_du_lieu` theo loại yêu cầu; cảnh báo khi vượt 5%/ngày | Giữ cơ chế từ chối rõ ràng và chuyển nhân viên kèm tóm tắt; loại nhóm `quoc_te` khỏi phạm vi pilot | PM trợ lý hoàn phí |
| 17 | Ngầm | Event `audit_sample_checked`: kiểm tra mẫu 100 đơn/tuần so với bảng giá hiện hành; ngưỡng cảnh báo > 1% đơn lệch | Xoá bộ nhớ đệm (cache) ngay khi cập nhật bảng giá mới và ghi `price_table_version` vào mọi trace | Kế toán trưởng |

# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: NST · Lớp: L3A

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | Toàn mẫu: **4.472 đ** (gấp 16,3× hoá đơn 275 đ; giờ NV chiếm 92,5%). Phạm vi `noi_dia`: **2.696 đ** (0,22×); `hang_nang`: **8.221 đ** (0,69×); cộng định phí 40 tr/tháng: **4.599 đ** (0,38×) [simulated] | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | 1. Số ca làm lại gấp đôi: **6.787 đ (+51,8%)** · 2. Xem lại gấp đôi: **6.292 đ (+40,7%)** · 3. Lương NV +25%: **5.506 đ (+23,1%)** [simulated] | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Chi phí cả hệ thống (gồm ca chuyển NV 12.000 đ): **5.865 đ/yêu cầu = 0,49×** so với 12.000 đ; giới hạn tối đa 2 lần chạy rẻ nhất toàn hệ thống (**6.901.220 đ**) [simulated] | Giả lập | Giám đốc vận hành LogiX-VN |
| 4 · Chỉ số chính, dùng, an toàn | Đợt chạy thử (chưa có đối chứng): Chính (đóng 24h, không mở lại 7 ngày) = **82,83%**; Dùng (bỏ qua gợi ý) = **27,12%**; An toàn (mở lại 7 ngày) = **4,25%**; đủ 10 event gắn `trace_id` | Xong, có bằng chứng | PM trợ lý hoàn phí |
| 5 · Bảng lỗi và cách khắc phục | Phân loại 20 ca theo 5 nhóm Google PAIR (đồng thuận ≥ 80%); thiết lập phát hiện đo được và khắc phục cho từng nhóm (khoá chống trùng, đối soát sổ cái, hậu kiểm mẫu 100 đơn/tuần) | Xong, có bằng chứng | Kỹ sư trưởng agent |
| 6 · Pilot plan | Chia ngẫu nhiên 20 NV can thiệp + 20 NV đối chứng (`noi_dia` + `hang_nang`), rollout 10% → 25% → 50%; chấp nhận MDE **6 điểm** (n = 859/nhóm, m ≥ 299 yc/NV, power ~0,64 ở mức 5 điểm); 3 luật dừng đủ 4 vế | Xong, có bằng chứng | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | Xem lại 100% đẩy chi phí lên **11.743 đ (0,98×)** hoặc **12.414 đ (1,03×)** nếu làm lại 15,3 phút [simulated]; giảm khối lượng 50% tăng định phí lên **2.370 đ/việc** [simulated] | Giả lập | PM trợ lý hoàn phí |

## Đề xuất quyết định Gate 2a: **Go có điều kiện**

Cho phép triển khai pilot có đối chứng trong phạm vi **chỉ gồm `noi_dia` và `hang_nang`** (loại bỏ `quoc_te` giá 22.515 đ và `doi_tac` giá 10.215 đ) với 4 điều kiện bắt buộc sau:

1. **Khắc phục lỗi hệ thống nghiêm trọng trước khi mở pilot:** Bổ sung khoá chống trùng (`idempotency_key`) và cơ chế đối soát sổ cái `refund_ledger_write` trước khi báo hoàn tiền (xử lý ca 7, 20) — *Người phụ trách: Kỹ sư trưởng agent · Ngày kiểm tra: trước ngày bắt đầu pilot*.
2. **Phê duyệt đánh đổi cỡ mẫu:** Ký xác nhận chấp nhận mức chênh phát hiện tối thiểu MDE = 6 điểm phần trăm (859 yêu cầu/nhóm, mỗi NV xử lý ≥ 299 yêu cầu; lưu ý power chỉ đạt ~0,64 nếu tác động thực tế là 5 điểm) — *Người phụ trách: Giám đốc vận hành LogiX-VN · Ngày kiểm tra: trước ngày bắt đầu pilot*.
3. **Thay thế dữ liệu giả lập bằng số đo thật:** Kích hoạt đủ 10 event có `trace_id` để ghi nhận `phut_xem_lai_thuc_te` và `phut_lam_lai_thuc_te`, cập nhật lại bảng chi phí thực tế sau tuần đầu tiên — *Người phụ trách: Kỹ sư trưởng agent · Ngày kiểm tra: cuối tuần 1 (bước rollout 0.10)*.
4. **Lộ trình giảm tỉ lệ xem lại an toàn:** Áp dụng xem lại 100% ở bước 0.10 để kiểm soát tỉ lệ mở lại (đang ở mức 4,25%), sau đó giảm dần tỉ lệ xem lại ở bước 0.25–0.50 khi tỉ lệ `sua + bo` < 15% và thời gian xem lại < 5,1 phút để đảm bảo hiệu quả chi phí — *Người phụ trách: Trưởng nhóm CSKH · Ngày kiểm tra: 2027-01-05*.

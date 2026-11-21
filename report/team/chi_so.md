# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h == 1` và `mo_lai_trong_7_ngay == 0`, chia tổng số yêu cầu | 82,83% (994 / 1.200) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | 27,12% (48 / 177) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay == 1`, chia tổng số yêu cầu | 4,25% (51 / 1.200) |
| Dùng | Tỉ lệ kích hoạt và sử dụng trợ lý (độ sâu) | Số yêu cầu nhóm can thiệp có ghi nhận `agent_suggestion_shown` chia tổng số yêu cầu nhóm can thiệp nhận | Không cần tính |
| An toàn | Tỉ lệ hoàn sai tiền phát hiện qua kiểm tra mẫu | Số đơn lệch số tiền hoàn trong `audit_sample_checked` chia tổng số đơn kiểm tra mẫu hằng tuần (100 đơn/tuần) | Không cần tính |

*Lưu ý:* Chỉ số chính trong đợt chạy thử là **82,83%** (không kết luận trợ lý "đã nâng" chỉ số từ 70% vì đợt chạy thử không có nhóm đối chứng).

## Danh sách event

Ít nhất sáu event, mỗi event có `trace_id` để nối với trace của agent.

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | Hệ thống tiếp nhận | `request_id`, `depot`, `loai`, `so_tien_vnd`, `arm`, `trace_id` | Khi khách gửi yêu cầu hoàn phí |
| `agent_run_completed` | Dịch vụ Agent | `request_id`, `attempt`, `tokens_in`, `tokens_out`, `tool_calls`, `status`, `trace_id` | Sau mỗi lần agent chạy (kể cả khi lỗi) |
| `agent_suggestion_shown` | Giao diện CSKH | `request_id`, `staff_id`, `so_tien_de_xuat`, `trace_id` | Khi gợi ý của trợ lý hiển thị cho nhân viên |
| `staff_review_decision` | Nhân viên CSKH | `request_id`, `staff_id`, `quyet_dinh` (`giu`/`sua`/`bo`), `phut_xem_lai_thuc_te`, `trace_id` | Khi nhân viên duyệt, sửa hoặc bỏ gợi ý |
| `staff_rework_completed` | Nhân viên CSKH | `request_id`, `staff_id`, `phut_lam_lai_thuc_te`, `ly_do`, `trace_id` | Khi nhân viên hoàn tất xử lý lại ca sai |
| `refund_ledger_write` | Dịch vụ sổ cái | `request_id`, `idempotency_key`, `so_tien_hoan`, `status`, `trace_id` | Khi hệ thống ghi lệnh hoàn tiền vào sổ cái |
| `handoff_to_staff` | Dịch vụ Agent | `request_id`, `reason`, `tom_tat`, `trace_id` | Khi trợ lý chuyển ca sang nhân viên xử lý |
| `ticket_closed` | Hệ thống ticket | `request_id`, `closed_at`, `dong_trong_24h`, `trace_id` | Khi yêu cầu chuyển sang trạng thái đã đóng |
| `ticket_reopened` | Khách hàng / Hệ thống | `request_id`, `reopened_at`, `so_ngay_sau_dong`, `ly_do`, `trace_id` | Khi khách mở lại yêu cầu trong vòng 7 ngày |
| `audit_sample_checked` | Bộ phận Kế toán | `request_id`, `so_tien_da_hoan`, `so_tien_dung`, `is_error`, `trace_id` | Hằng tuần khi hậu kiểm mẫu 100 đơn |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, ghi event dùng để tính. Chỉ số nào không tính được từ danh sách event thì chưa đo được.

- **Chỉ số chính (`dong_trong_24h_khong_mo_lai_7_ngay`):** tính từ `refund_request_created`, `ticket_closed` và `ticket_reopened` (nối qua `request_id` và `trace_id`).
- **Tỉ lệ bỏ qua gợi ý:** tính từ `staff_review_decision` (`sua` + `bo`) chia cho tổng `agent_suggestion_shown`.
- **Tỉ lệ lỗi lọt đến khách:** tính từ `ticket_reopened` (trong 7 ngày) chia cho `refund_request_created`.
- **Tỉ lệ độ sâu sử dụng (đề xuất):** tính từ `agent_suggestion_shown` chia cho `refund_request_created` thuộc nhánh can thiệp.
- **Tỉ lệ hoàn sai tiền ngầm (đề xuất):** tính từ `audit_sample_checked`. Tất cả 5 chỉ số đều đo được đầy đủ từ 10 event trên.

## E2 · Rủi ro kinh tế

Ít nhất hai dòng, số lấy từ bảng độ nhạy (`bang_chi_phi.md`).

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | Chi phí mỗi việc thành công tăng **+51,8%**, từ 4.472 đ lên **6.787 đ** (simulated) | Tỉ lệ ca `lam_lai` theo tuần vượt 7% (mức chạy thử trong phạm vi là 4,9%) | Thu hẹp phạm vi về chỉ `noi_dia`, kiểm tra 20 trace lỗi làm lại để sửa prompt/tool | PM trợ lý hoàn phí |
| Phải duy trì xem lại 100% kéo dài | Chi phí đạt **11.743 đ = 0,98×** (9 phút làm lại) hoặc **12.414 đ = 1,03×** (15,3 phút làm lại) so với 12.000 đ (simulated) | Tỉ lệ yêu cầu bị xem lại vẫn > 50% khi kết thúc bước rollout 0.25 | Áp dụng cơ chế giảm tỉ lệ xem lại theo bậc đối với các đơn `noi_dia` có độ tin cậy cao khi tỉ lệ `sua + bo` < 15% | Trưởng nhóm CSKH |
| Khối lượng yêu cầu thực tế thấp hơn dự kiến | Chi phí cố định 40 triệu đ/tháng làm tăng thêm **+1.185 đ/việc** ở 45.000 yc/tháng và **+2.370 đ/việc** nếu khối lượng giảm một nửa (simulated) | Số việc thành công hằng tuần thấp hơn 50% kế hoạch rollout | Tạm dừng mở rộng bước tiếp theo và đàm phán lại gói hạ tầng/vận hành cố định | PM trợ lý hoàn phí |

"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
from statistics import NormalDist
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
# TODO CP1: viết ba hàm dưới đây cho tới khi kiem_tra_dap_an_biet_truoc() in ĐẠT.
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# TODO CP1: viết mo_hinh; CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công)."""
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())
    return dict(
        token=tien_token.sum(),
        tool=tien_tool.sum(),
        chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
        xem_lai=xem_lai,
        lam_lai=lam_lai,
        tong=tong,
        thanh_cong=thanh_cong,
        cps=tong / thanh_cong,
        hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs),
    )


def co_mau(p1, p2, alpha=0.05, power=0.8):
    za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()

    print('\n--- A2 · Mô hình chi phí ---')
    ket_qua = mo_hinh(runs, reqs)
    for ten, gia_tri in ket_qua.items():
        print(f'{ten:16s} {gia_tri:>14,.1f}')

    # TODO CP1 · Nhiệm vụ A3: tính lại theo từng giá trị của cột loai.
    print('\n--- A3 · Tách theo loại yêu cầu ---')
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        sub = reqs[reqs['loai'] == loai]
        r = mo_hinh(runs, sub)
        print(f"{loai:10s} | yc={len(sub):3d} | tc={r['thanh_cong']/len(sub)*100:5.1f}% | "
              f"chay/yc={sub['so_lan_chay'].mean():.2f} | cps={r['cps']:7,.0f} | so_12k={r['cps']/BASELINE:.2f}x")

    # A4 · Chi phí cố định 40 triệu/tháng cho noi_dia + hang_nang
    pv = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    r_pv = mo_hinh(runs, pv)
    tc_thang = 45000 * (r_pv['thanh_cong'] / len(reqs))
    cp_cd_1 = 40_000_000 / tc_thang
    cp_cd_2 = 40_000_000 / (tc_thang / 2)
    print(f"\n--- A4 · Chi phí cố định (noi_dia + hang_nang) ---")
    print(f"45.000 yc/tháng: tc={tc_thang:,.0f} | cd={cp_cd_1:,.0f} | cps+cd={r_pv['cps']+cp_cd_1:,.0f} ({(r_pv['cps']+cp_cd_1)/BASELINE:.2f}x)")
    print(f"22.500 yc/tháng: tc={tc_thang/2:,.0f} | cd={cp_cd_2:,.0f} | cps+cd={r_pv['cps']+cp_cd_2:,.0f} ({(r_pv['cps']+cp_cd_2)/BASELINE:.2f}x)")

    # TODO CP2 · Nhiệm vụ B: đổi từng yếu tố, ghi vào bảng độ nhạy.
    print('\n--- B1 & B2 · Bảng độ nhạy ---')
    kich_ban = {
        'Giá token gấp đôi': dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa': dict(gia_vao=13, gia_ra=65),
        'Tỉ lệ xem lại gấp đôi': dict(he_so_xem_lai=2),
        'Tỉ lệ xem lại giảm một nửa': dict(he_so_xem_lai=0.5),
        'Số ca làm lại gấp đôi': dict(he_so_lam_lai=2),
        'Số ca làm lại giảm một nửa': dict(he_so_lam_lai=0.5),
        'Lương nhân viên tăng 25%': dict(luong_phut=2500),
        'Chỉ cho chạy tối đa 2 lần': dict(max_lan_chay=2),
        'Chỉ cho chạy 1 lần': dict(max_lan_chay=1),
    }
    goc = ket_qua['cps']
    for ten, kw in kich_ban.items():
        r = mo_hinh(runs, reqs, **kw)
        print(f"{ten:28s} | cps={r['cps']:7,.0f} | {(r['cps']/goc - 1)*100:+6.1f}%")
    r_pair = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)
    print(f"{'Cặp: Token x2 + Xem lại x2':28s} | cps={r_pair['cps']:7,.0f} | {(r_pair['cps']/goc - 1)*100:+6.1f}%")

    print('\n--- B3 · Chi phí cả hệ thống ---')
    for k in [1, 2, 3]:
        r = mo_hinh(runs, reqs, max_lan_chay=k)
        khong_tc = len(reqs) - r['thanh_cong']
        he_thong = r['tong'] + khong_tc * BASELINE
        print(f"Giới hạn {k} lần: tro_ly={r['tong']:10,.0f} | khong_tc={khong_tc:3d} | he_thong={he_thong:10,.0f} | cps={r['cps']:7,.0f}")

    # B4 · Xem lại 100% trên noi_dia + hang_nang
    runs_pv = runs[runs['request_id'].isin(pv['request_id'])]
    ok_reqs = runs_pv[runs_pv['status'] == 'ok']['request_id'].nunique()
    lam_lai_cnt = (pv['ket_qua'] == 'lam_lai').sum()
    tok_tool_pv = (runs_pv['tokens_in'] / 1000 * GIA_VAO + runs_pv['tokens_out'] / 1000 * GIA_RA + runs_pv['tool_calls'] * GIA_TOOL).sum()
    cps_b4_9 = (tok_tool_pv + ok_reqs * 5 * LUONG_PHUT + lam_lai_cnt * 9 * LUONG_PHUT) / r_pv['thanh_cong']
    cps_b4_153 = (tok_tool_pv + ok_reqs * 5 * LUONG_PHUT + lam_lai_cnt * 15.3 * LUONG_PHUT) / r_pv['thanh_cong']
    print(f"\n--- B4 · Xem lại 100% (noi_dia + hang_nang) ---")
    print(f"Làm lại 9 phút: {cps_b4_9:,.0f} đ ({cps_b4_9/BASELINE:.2f}x) | Làm lại 15,3 phút: {cps_b4_153:,.0f} đ ({cps_b4_153/BASELINE:.2f}x)")

    # TODO CP4 · Nhiệm vụ D: cỡ mẫu.
    print('\n--- D1 · Cỡ mẫu ---')
    from statsmodels.stats.proportion import proportion_effectsize
    from statsmodels.stats.power import NormalIndPower

    n_5pt = co_mau(0.70, 0.75)
    n_stats = math.ceil(NormalIndPower().solve_power(effect_size=proportion_effectsize(0.75, 0.70), alpha=0.05, power=0.80, ratio=1))
    de_75 = 1 + 74 * 0.02
    n_b = math.ceil(n_5pt * de_75)
    n_6pt = co_mau(0.70, 0.76)
    m_e = math.ceil((0.98 * n_6pt) / (20 - 0.02 * n_6pt))
    print(f"D1.a Theo yêu cầu (5 điểm): {n_5pt} (statsmodels: {n_stats})")
    print(f"D1.b Theo nhân viên m=75: DE={de_75:.2f}, n={n_b}/nhóm -> {math.ceil(n_b/75)} NV/nhóm (tổng {math.ceil(n_b/75)*2} > 40)")
    print(f"D1.c 20 NV/nhóm: tối đa {int(20/0.02)} < {n_5pt}")
    print(f"D1.d 6 depot/nhóm: tối đa {int(6/0.02)}")
    print(f"D1.e Chấp nhận 6 điểm (n={n_6pt}/nhóm), 20 NV/nhóm: m >= {m_e} yêu cầu/NV (DE={1+(m_e-1)*0.02:.2f})")
    print(f"Tỉ lệ mo_lai_trong_7_ngay: {reqs['mo_lai_trong_7_ngay'].mean()*100:.2f}% ({reqs['mo_lai_trong_7_ngay'].sum()}/{len(reqs)})")
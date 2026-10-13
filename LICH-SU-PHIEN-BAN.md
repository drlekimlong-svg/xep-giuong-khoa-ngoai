# Lịch sử phiên bản – App xếp giường khoa Ngoại

Mỗi phiên bản phát hành được lưu ở ba nơi:

- **Bản sao nguyên vẹn** trong thư mục `phien-ban/<số phiên bản>/` – đây là file đem đi dùng.
- **Nhãn git** cùng tên (ví dụ `v1.0`) – xem lại hoặc lấy lại mã nguồn đúng thời điểm đó.
- **Một mục trong file này** – ghi phiên bản có gì, dùng ở đâu, còn hạn chế gì.

Số phiên bản hiện ở góc dưới màn hình app và trong file sao lưu. Phiên bản `1.x` là bản một máy, không cần mạng. Phiên bản `2.x` là bản dùng chung nhiều máy qua Supabase.

File `XepGiuong_KhoaNgoai.html` ở thư mục gốc là bản đang phát triển, có thể mới hơn mọi bản đã phát hành.

---

## 1.0 — 13/10/2026 — Bản triển khai đầu tại khoa

- **File:** `phien-ban/v1.0/XepGiuong_KhoaNgoai.html` · nhãn git `v1.0`
- **Dùng ở đâu:** một máy tính tại quầy điều dưỡng khoa Ngoại, giai đoạn đầu triển khai.
- **Dữ liệu:** lưu trong trình duyệt của máy đó, không gửi lên mạng, không cần internet.

**Có gì**

- Sơ đồ 17 phòng, 65 giường đúng vị trí thực tế; phân khu Tiêu hóa 33 giường, Niệu 32 giường.
- Khu Niệu luôn có phòng Nam và phòng Nữ cho cả bốn loại phòng 2, 3, 4, 6 giường; phòng Tiêu hóa tự tách Nam/Nữ theo người vào trước.
- Phòng 2–3 giường là phòng dịch vụ, chỉ gợi ý khi người bệnh yêu cầu.
- Gợi ý giường khi nhận bệnh; cho nằm nhờ khu kia khi hết giường và tự đề xuất chuyển về khi có giường.
- Ghi nơi nhận bệnh (cấp cứu, phòng khám, khoa khác/phòng mổ) và hình thức ra khoa (xuất viện, chuyển khoa, đi mổ, xin về, chuyển viện, tử vong).
- Đi mổ có giữ giường; mổ về trả lại giường cũ nếu còn.
- Danh sách người bệnh trong ngày: theo chuyên khoa, theo bác sĩ, theo phòng, hoặc riêng một bác sĩ; in, lưu PDF, xuất Excel; có dòng tổng hợp vào/ra/đi mổ trong ngày.
- Danh sách chờ giường, tìm kiếm, lịch sử ra khoa có hoàn tác, nhật ký thao tác.
- Tự lưu sau mỗi thao tác; mỗi ngày tự giữ một bản đầu ngày trong máy và tự tải một file sao lưu về thư mục Downloads.

**Cách cài ở máy khoa**

1. Chép file `XepGiuong_KhoaNgoai.html` vào một thư mục cố định trên máy (ví dụ `D:\XepGiuong\`).
2. Bấm đúp để mở bằng Chrome hoặc Edge; nên tạo lối tắt ra màn hình.
3. Vào Cài đặt → mục 3 để nhập danh sách bác sĩ của khoa.

**Khi nâng cấp lên bản mới:** bấm "Sao lưu ra file ngay" trước, rồi chép đè file mới vào **đúng thư mục và tên file cũ**. Dữ liệu nằm trong trình duyệt nên vẫn còn; file sao lưu là phương án dự phòng.

**Hạn chế đã biết**

- Chỉ dùng trên một máy; máy khác mở file sẽ thấy dữ liệu riêng của máy đó.
- Không chạy được khi chép file vào iPad/iPhone (chỉ xem trước được).
- Nếu trình duyệt bị xóa dữ liệu duyệt web thì mất dữ liệu trong máy; khi đó khôi phục từ file sao lưu.
- Chưa thử in ra giấy thật và chưa thử trên máy của khoa.
- Danh sách bác sĩ chưa được nhập sẵn.

---

## Trước 1.0 — 12–13/10/2026 — Các bản nháp (không phát hành)

Các bước dựng dẫn đến bản 1.0, không có bản sao riêng:

- 12/10: bản đầu tiên – sơ đồ, gợi ý giường, nằm nhờ, đề xuất chuyển, danh sách ngày.
- 12/10: đổi phân khu để Niệu có cả phòng 6 giường Nam và Nữ (616, 617).
- 12/10: thêm phòng dịch vụ, sao lưu tự động, in danh sách riêng một bác sĩ.
- 12/10: thêm nơi nhận bệnh, hình thức ra khoa, đi mổ có giữ giường, tổng hợp trong ngày.
- 13/10: đưa bản xem thử giao diện lên GitHub (https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/), tự nạp dữ liệu mẫu.

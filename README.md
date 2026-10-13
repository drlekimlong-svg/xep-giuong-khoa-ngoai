# Sơ đồ xếp giường – Khoa Ngoại

Công cụ giúp điều dưỡng xếp giường cho người bệnh Tiêu hóa và Niệu theo khu, theo giới và theo loại phòng, tự nhắc chuyển phòng khi có giường phù hợp, và in danh sách người bệnh mỗi ngày.

**Xem thử giao diện:** https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/

Bản xem thử mở sẵn với dữ liệu mẫu; mọi tên người bệnh và bác sĩ trong đó đều là tên giả.

**Bản dùng chung nhiều máy (cần tài khoản do khoa cấp):** https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/chung.html

**Bản cũ 1.0 (một máy, không đăng nhập, không nối máy chủ):** https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/v1/

Lịch sử các phiên bản: [LICH-SU-PHIEN-BAN.md](LICH-SU-PHIEN-BAN.md).

## Dữ liệu nằm ở đâu

Toàn bộ chương trình là một file `XepGiuong_KhoaNgoai.html`. Kho này chỉ chứa chương trình, không chứa dữ liệu người bệnh.

- **Bản một máy và bản xem thử:** những gì nhập vào chỉ được lưu trong trình duyệt của chính máy đang dùng và không gửi đi đâu.
- **Bản dùng chung:** dữ liệu nằm trong một dự án Supabase của khoa và chỉ đọc, ghi được sau khi đăng nhập bằng tài khoản được cấp quyền. Địa chỉ dự án và khóa trong mã nguồn là khóa công khai; quyền truy cập do quy tắc trong `supabase/thiet-lap.sql` quyết định.

## Dùng tại khoa

Chép file `XepGiuong_KhoaNgoai.html` vào máy tính và bấm đúp để mở bằng Chrome hoặc Edge. Không cần internet.

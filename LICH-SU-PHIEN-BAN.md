# Lịch sử phiên bản – App xếp giường khoa Ngoại

Mỗi phiên bản phát hành được lưu ở ba nơi:

- **Bản sao nguyên vẹn** trong thư mục `phien-ban/<số phiên bản>/` – đây là file đem đi dùng.
- **Nhãn git** cùng tên (ví dụ `v1.0`) – xem lại hoặc lấy lại mã nguồn đúng thời điểm đó.
- **Một mục trong file này** – ghi phiên bản có gì, dùng ở đâu, còn hạn chế gì.

Số phiên bản hiện ở góc dưới màn hình app và trong file sao lưu. Phiên bản `1.x` là bản một máy, không cần mạng. Phiên bản `2.x` là bản dùng chung nhiều máy qua Supabase.

File `XepGiuong_KhoaNgoai.html` ở thư mục gốc là bản đang phát triển, có thể mới hơn mọi bản đã phát hành.

---

## 2.0-thu2 — 13/10/2026 — Nối với dự án Supabase thật của khoa

- **File:** `phien-ban/v2.0-thu2/` (app, `chung.html`, `thiet-lap.sql`) · nhãn git `v2.0-thu2`
- **Dùng ở đâu:** để bác sĩ đăng nhập thử với dự án Supabase thật, bằng dữ liệu mẫu. Chưa dùng tại khoa.
- **Dự án Supabase:** `xep-giuong-khoa-ngoai` (mã `wcnxauujoraohokntryt`, vùng Singapore, gói miễn phí), tạo ngày 13/10/2026.

**Mới so với 2.0-thu1**

- Địa chỉ dự án và khóa công khai của khoa được đặt sẵn trong app.
- Một file chạy ba kiểu theo cách mở: mở thường là bản một máy; `chung.html` (đuôi `#chung`) là bản dùng chung có đăng nhập; `index.html` (đuôi `#mau`) là bản xem thử.
- Cài đặt có nút "Chuyển máy này sang dùng chung", không phải gõ địa chỉ và khóa.
- Hàm `my_role()` trong cơ sở dữ liệu chuyển sang chạy với quyền của người gọi, theo cảnh báo bảo mật của Supabase.

**Đã thử và chưa thử**

- Đã cài `thiet-lap.sql` vào dự án thật; công cụ rà bảo mật của Supabase không còn cảnh báo nào.
- Đã thử quy tắc bảo mật ngay trên cơ sở dữ liệu thật với ba loại người dùng giả lập (dữ liệu thử được hủy sau khi chạy): người chưa đăng nhập và người không thuộc khoa không đọc, không ghi được gì; quyền `view` đọc được, không ghi được; quyền `edit` lưu được, không xóa được sơ đồ, không tự thêm người; lưu với số version cũ bị từ chối; bản lưu đầu ngày được tạo.
- Đã gọi địa chỉ thật từ bên ngoài bằng khóa công khai: bị từ chối đúng như mong muốn; trình duyệt gọi được.
- Lúc phát hành chưa có lần đăng nhập thật nào từ app. Tài khoản đầu tiên (BS.KimLong, quyền `edit`) được cấp quyền cùng ngày; việc đăng nhập thử do bác sĩ tự làm.
- Bản web trên GitHub được cập nhật lên bản này ngày 13/10/2026; link đăng nhập: https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/chung.html
- Chưa thử trên iPad và điện thoại.

**Hạn chế đã biết:** như bản 2.0-thu1.

---

## 2.0-thu1 — 13/10/2026 — Bản thử dùng chung nhiều máy qua Supabase

- **File:** `phien-ban/v2.0-thu1/XepGiuong_KhoaNgoai.html` và `thiet-lap.sql` · nhãn git `v2.0-thu1`
- **Dùng ở đâu:** chưa dùng tại khoa. Để bác sĩ xem thử cách đăng nhập và dùng chung dữ liệu, với dữ liệu mẫu.
- **Dữ liệu:** khi chưa kết nối thì y như bản 1.0 (trong trình duyệt). Khi kết nối Supabase thì lưu trên máy chủ Supabase, không để lại trong trình duyệt.

**Mới so với 1.0**

- Màn hình đăng nhập bằng email và mật khẩu; tài khoản do người quản trị tạo trên Supabase.
- Hai loại quyền: `edit` được sửa, `view` chỉ xem và in. Quyền được kiểm tra ở cả giao diện lẫn máy chủ.
- Cả sơ đồ lưu chung một chỗ; máy khác thấy thay đổi sau khoảng 6 giây.
- Chống ghi đè: hai máy sửa cùng lúc thì máy lưu sau bị từ chối, sơ đồ tự tải lại và báo làm lại.
- Báo đỏ khi mất kết nối và tự thử lại; tự gia hạn phiên đăng nhập.
- Nhật ký ghi tên người thao tác.
- Máy chủ tự giữ một bản mỗi ngày trong 60 ngày.
- Cài đặt có mục kết nối/ngắt kết nối cho riêng từng máy; "Khôi phục từ file" dùng để đưa dữ liệu bản một máy lên.
- Chưa kết nối thì mọi thứ chạy như bản 1.0.

**Cách bật:** xem `supabase/HUONG-DAN.md`.

**Đã thử và chưa thử**

- Đã thử với một máy chủ giả lập chạy trên máy tính: đăng nhập sai/đúng, lưu, máy khác sửa, hai máy sửa cùng lúc, hết hạn phiên, máy chủ ngừng nhận, đăng xuất, tài khoản chỉ xem, tài khoản chưa được cấp quyền, ngắt kết nối. Tất cả đúng.
- **Chưa thử với Supabase thật** vì chưa có dự án. File `thiet-lap.sql` chưa được chạy lần nào.
- Chưa thử trên iPad và điện thoại.

**Hạn chế đã biết**

- Cần mạng để lưu. Thay đổi làm lúc mất mạng có thể bị bỏ nếu máy khác đã sửa trong lúc đó.
- Mỗi thao tác gửi cả sơ đồ lên máy chủ; với một khoa 65 giường thì nhẹ, nhưng không hợp để mở rộng ra nhiều khoa trong cùng một dòng dữ liệu.
- Tên người bệnh nằm trên máy chủ ở nước ngoài dưới dạng đọc được; chưa có mã hóa tại máy. Cần bệnh viện đồng ý trước khi nhập dữ liệu thật.
- Đổi mật khẩu và tạo tài khoản phải làm trong trang Supabase, chưa có trong app.

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

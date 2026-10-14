# Bản dùng chung nhiều máy (Supabase) – hướng dẫn

Cập nhật cho bản 2.0-thu3 (14/10/2026).

## Địa chỉ

| Địa chỉ | Là gì |
|---|---|
| https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/chung.html | Bản dùng chung: đăng nhập, dữ liệu chung của khoa |
| https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/ | Bản xem thử với dữ liệu mẫu, không cần đăng nhập |
| https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/v1/ | Bản cũ 1.0, một máy |

Trên iPhone, iPad: mở địa chỉ bằng Safari → nút Chia sẻ → **Thêm vào Màn hình chính**. Từ đó app mở toàn màn hình như một ứng dụng.

## Đăng nhập

- **Quản trị viên** (một người: dr.lekimlong@gmail.com) đăng nhập bằng email.
- **Bác sĩ, điều dưỡng** đăng nhập bằng **tên đăng nhập** do quản trị viên cấp, không cần email. Tên đăng nhập lấy từ họ tên: chữ cái đầu của họ và tên đệm, cộng tên không dấu. Ví dụ TS. BS. Lê Nguyên Khôi → `LNKhoi`. Gõ chữ hoa hay thường đều được.
- **Mật khẩu ban đầu** theo quy ước của khoa: tên không dấu + `@1234` (ví dụ `Khoi@1234`). Lần đăng nhập đầu, app **bắt buộc** đặt mật khẩu riêng.
- **Quên mật khẩu:** không có thư đặt lại mật khẩu, vì tài khoản không gắn email. Quản trị viên đặt lại trong app (nút Tài khoản → Đặt lại mật khẩu); người đó sẽ phải đổi lại ở lần đăng nhập tới.

Phía sau, tên đăng nhập được đổi thành một địa chỉ nội bộ dạng `lnkhoi@khoangoai.invalid`. Đuôi `.invalid` là tên miền dành riêng, không bao giờ nhận thư, nên không có thư nào bị gửi đi.

## Vai trò

| Việc | Quản trị | Điều dưỡng | Bác sĩ | Chỉ xem |
|---|:-:|:-:|:-:|:-:|
| Xem sơ đồ, danh sách, in, xuất Excel, lịch sử | ✓ | ✓ | ✓ | ✓ |
| Sửa, bổ sung thông tin người bệnh | ✓ | ✓ | ✓ | |
| Nhận bệnh, xếp và chuyển giường, đi mổ, ra khoa, hoàn tác | ✓ | ✓ | | |
| Tải file sao lưu | ✓ | ✓ | | |
| Cài đặt (phân khu, giới phòng, phòng dịch vụ, tên khoa) | ✓ | | | |
| Quản lý tài khoản | ✓ | | | |

Quyền được kiểm hai lớp. Giao diện ẩn những nút không được dùng; máy chủ cũng từ chối lưu nếu thay đổi vượt quyền. Ví dụ bác sĩ đổi giường hay nhận bệnh sẽ bị máy chủ chặn dù giao diện có bị sửa.

## Tạo tài khoản (quản trị viên)

1. Đăng nhập bản dùng chung bằng tài khoản quản trị → nút **Tài khoản** ở góc trên.
2. Ở ô **Thêm tài khoản**, dán danh sách, mỗi dòng một người: `họ tên kèm học hàm; vai trò`.
   - Vai trò: `dd` = điều dưỡng · `bs` = bác sĩ · `xem` = chỉ xem.
   - `qt` = chỉ đưa tên vào danh sách bác sĩ phụ trách mà không tạo tài khoản; dùng cho chính quản trị viên.
   - Không ghi vai trò thì app đoán theo chức danh (ĐD → điều dưỡng, BS/ThS/TS → bác sĩ); đoán không được thì bắt chọn.
3. Bấm **Xem trước**. Kiểm tra tên đăng nhập và mật khẩu ban đầu, sửa được trực tiếp. Nếu hai người trùng tên viết tắt, người sau được thêm số (LNKhoi2).
4. Bấm **Tạo … tài khoản**. Bác sĩ vừa tạo được tự thêm vào danh sách bác sĩ phụ trách.
5. Bấm **In phiếu tài khoản** để in phiếu cho từng người (tên đăng nhập + mật khẩu ban đầu). Mật khẩu ban đầu chỉ xem được lúc này, đóng bảng là mất.

Trong danh sách tài khoản: đổi vai trò bằng ô chọn; **Khóa** để chặn người đã nghỉ (không xóa lịch sử); **Đặt lại mật khẩu** khi có người quên.

Mật khẩu theo quy ước `Tên@1234` dễ đoán. Vì vậy app bắt đổi ở lần đăng nhập đầu; nên phát phiếu và nhắc mọi người đăng nhập sớm để đổi.

## Cấu hình máy tối thiểu

**Máy tính bàn hoặc xách tay**

- Windows 10 hoặc 11 (hoặc macOS), trình duyệt Chrome hoặc Edge bản mới, để tự cập nhật.
- Bộ xử lý 2 nhân bất kỳ đời từ khoảng 2015 trở lại đây; RAM 4 GB (8 GB nếu chạy song song phần mềm quản lý bệnh viện); ổ cứng trống 1 GB.
- Màn hình tối thiểu 1366×768; nên dùng 1920×1080 để thấy trọn hai dãy phòng.
- Bản dùng chung cần internet ổn định; lưu lượng nhỏ, khoảng vài chục MB mỗi ngày mỗi máy. Bản một máy không cần mạng.
- Máy in A4 nếu cần in danh sách.
- Windows 7, 8.1: Chrome và Edge đã ngừng cập nhật từ đầu năm 2023. App có thể vẫn chạy nhưng không an toàn, không khuyên dùng.

**iPhone, iPad, điện thoại Android**

- iPhone hoặc iPad chạy iOS/iPadOS 15 trở lên, dùng Safari. Android dùng Chrome bản mới.
- Trên điện thoại, các phòng xếp thành thẻ hai cột để không phải kéo ngang. iPad xoay ngang thấy đủ sơ đồ hành lang.

## Thông tin dự án (để quản trị)

- Dự án `xep-giuong-khoa-ngoai` · mã `wcnxauujoraohokntryt` · vùng Singapore · gói miễn phí.
- Trang quản trị: https://supabase.com/dashboard/project/wcnxauujoraohokntryt
- Cơ sở dữ liệu: `thiet-lap.sql`. Quản lý tài khoản: `functions/quan-ly-tai-khoan/index.ts`.
- Gói miễn phí: tự tạm dừng nếu cả tuần không ai dùng (vào trang quản trị bấm khôi phục); không có sao lưu tự động. Máy chủ tự giữ một bản sơ đồ mỗi ngày trong 60 ngày, cách lấy lại ghi cuối file `thiet-lap.sql`.
- Chỉ nhập tên người bệnh thật sau khi bệnh viện đồng ý cho lưu dữ liệu trên Supabase.

# Lịch sử phiên bản – App xếp giường khoa Ngoại

Mỗi phiên bản phát hành được lưu ở ba nơi:

- **Bản sao nguyên vẹn** trong thư mục `phien-ban/<số phiên bản>/` – đây là file đem đi dùng.
- **Nhãn git** cùng tên (ví dụ `v1.0`) – xem lại hoặc lấy lại mã nguồn đúng thời điểm đó.
- **Một mục trong file này** – ghi phiên bản có gì, dùng ở đâu, còn hạn chế gì.

Số phiên bản hiện ở góc dưới màn hình app và trong file sao lưu. Phiên bản `1.x` là bản một máy, không cần mạng. Phiên bản `2.x` là bản dùng chung nhiều máy qua Supabase.

File `XepGiuong_KhoaNgoai.html` ở thư mục gốc là bản đang phát triển, có thể mới hơn mọi bản đã phát hành.

**Địa chỉ trên web** (cập nhật 13/10/2026):

| Địa chỉ | Là gì |
|---|---|
| https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/ | Bản mới nhất, chạy kiểu xem thử với dữ liệu mẫu |
| https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/chung.html | Bản mới nhất, dùng chung nhiều máy: đăng nhập, nối Supabase |
| https://drlekimlong-svg.github.io/xep-giuong-khoa-ngoai/v1/ | Bản cũ 1.0: một máy, không đăng nhập, không nối Supabase |

Mọi bản đã phát hành đều mở được trên web theo dạng `…/phien-ban/<số phiên bản>/XepGiuong_KhoaNgoai.html`.
Các địa chỉ này cùng một trang web nên trên cùng một máy, bản một máy và bản 1.0 dùng chung dữ liệu lưu trong trình duyệt.

---

## 2.0-thu4 — 14/10/2026 — Sửa cách tạo tên đăng nhập và mật khẩu ban đầu

- **File:** `phien-ban/v2.0-thu4/XepGiuong_KhoaNgoai.html` · nhãn git `v2.0-thu4`. Máy chủ (cơ sở dữ liệu, Edge Function) không đổi so với 2.0-thu3.

**Sửa so với 2.0-thu3**

- Chức danh `CKI`, `CKII`, `CK1`, `CK2` viết không có dấu chấm (vd "BS. CKII Phạm Ngọc Tảo") trước đây bị tính là một phần của tên, cho ra tên đăng nhập sai. Nay được bỏ đúng: `PNTao`.
- Người tên hai chữ cái (Vũ, Mỹ, My) có mật khẩu ban đầu `Vu@1234` chỉ 7 ký tự, bị từ chối vì dưới 8 ký tự. Nay thêm một số: `Vu@12345`.

**Đã thử:** dán danh sách 30 người của khoa (lấy từ sơ đồ tổ chức) vào mục Tài khoản trên máy chủ giả lập. Tên đăng nhập không trùng, mật khẩu đều đủ 8 ký tự, vai trò đúng; tạo đủ 29 tài khoản (một dòng `qt` chỉ thêm vào danh sách bác sĩ); 15 bác sĩ được đưa vào danh sách bác sĩ phụ trách. Chưa tạo trên máy chủ thật.

---

## 2.0-thu3 — 14/10/2026 — Đăng nhập bằng mã, phân quyền theo vai trò, dùng được trên iPhone/iPad

- **File:** `phien-ban/v2.0-thu3/` (app, `chung.html`, `icon-180.png`, `thiet-lap.sql`, `quan-ly-tai-khoan/index.ts`) · nhãn git `v2.0-thu3`
- **Dùng ở đâu:** bản dùng chung trên web (`…/chung.html`), dùng thử với dữ liệu mẫu.

**Mới so với 2.0-thu2**

- **Đăng nhập bằng mã** do quản trị viên cấp (vd `LNKhoi`), không cần email; quản trị viên vẫn dùng email.
- **Bốn vai trò:**
  - Quản trị: một người, dr.lekimlong@gmail.com.
  - Điều dưỡng: nhận bệnh, xếp và chuyển giường, đi mổ, ra khoa, sửa thông tin.
  - Bác sĩ: xem và bổ sung thông tin, không xếp giường.
  - Chỉ xem.
- **Máy chủ kiểm quyền theo nội dung thay đổi:** bác sĩ đổi giường, nhận bệnh hay cho ra khoa bị từ chối; chỉ quản trị viên đổi được phân khu và tên khoa.
- **Mục "Tài khoản" cho quản trị viên:**
  - Dán danh sách để tạo hàng loạt; app gợi ý tên đăng nhập và mật khẩu ban đầu theo quy ước `Tên@1234`.
  - In phiếu tài khoản; đổi vai trò, khóa/mở khóa, đặt lại mật khẩu.
  - Tạo bằng Edge Function `quan-ly-tai-khoan` trên máy chủ; khóa quản trị của Supabase không tới trình duyệt.
- **Bắt buộc đổi mật khẩu ở lần đăng nhập đầu** và sau mỗi lần được đặt lại; có nút "Đổi mật khẩu" cho mọi người.
- **Nếu vai trò bị đổi trong lúc đang mở app:** máy chủ từ chối, app báo, tự tải lại sơ đồ và cập nhật vai trò.
- **Giao diện màn hình hẹp:**
  - Điện thoại và iPad dọc: phòng xếp thành thẻ, không phải kéo ngang; nút và ô giường to hơn khi dùng tay chạm; chữ ô nhập 16px để iPhone không tự phóng to.
  - iPad ngang: thấy đủ sơ đồ hành lang.
  - Biểu tượng riêng khi "Thêm vào Màn hình chính".
- **Cơ sở dữ liệu:** bảng `staff` có thêm `login_id`, `must_change`, `active`; vai trò đổi từ `edit/view` sang `admin/nurse/doctor/view`; hàm kiểm quyền chuyển vào schema `private` (không gọi được qua API).

**Đã thử và chưa thử**

- **Trên cơ sở dữ liệu thật** (người dùng giả lập, hủy sau khi chạy):
  - Từng vai trò đọc và ghi đúng quyền; bác sĩ bị chặn khi đổi giường, nhận bệnh, cho ra khoa.
  - Điều dưỡng bị chặn khi đổi phân khu; không thêm được quản trị viên thứ hai; tài khoản bị khóa không đọc được gì.
  - Công cụ rà bảo mật của Supabase chỉ còn một nhắc về tính năng chặn mật khẩu đã lộ; tôi chưa bật tính năng này.
- **Phần quản lý tài khoản trên máy chủ thật:** đã thử người chưa đăng nhập và mã giả đều bị từ chối, và Supabase nhận địa chỉ nội bộ `…@khoangoai.invalid` (kiểm bằng lệnh không tạo tài khoản). **Chưa tạo tài khoản thật nào**; lần tạo đầu do quản trị viên làm.
- **Với máy chủ giả lập:**
  - Quản trị tạo hàng loạt, in phiếu, đổi vai trò, khóa, đặt lại mật khẩu.
  - Điều dưỡng đăng nhập lần đầu bị bắt đổi mật khẩu, rồi nhận bệnh được.
  - Bác sĩ chỉ thấy nút "Sửa thông tin"; tài khoản chỉ xem không sửa được gì; tài khoản bị khóa không vào được.
- **Giao diện:** đã thử bằng cách giả lập khổ màn hình iPhone (375 px), iPad dọc (768 px), iPad ngang (1180 px) trên máy tính. **Chưa thử trên iPhone, iPad thật.**

**Hạn chế đã biết**

- Mật khẩu ban đầu theo quy ước dễ đoán cho tới khi người dùng đổi.
- Không có "quên mật khẩu" tự phục vụ; phải nhờ quản trị viên.
- Các hạn chế của 2.0-thu1 vẫn còn: cần mạng; tên người bệnh trên máy chủ ở nước ngoài, chưa mã hóa.

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

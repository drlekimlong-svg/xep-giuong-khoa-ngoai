# Bản dùng chung nhiều máy (Supabase) – hướng dẫn

Cập nhật cho bản 2.2-thu2 (15/10/2026).

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
| Xem sơ đồ, danh sách, báo cáo, in, xuất Excel, lịch sử | ✓ | ✓ | ✓ | ✓ |
| Sửa, bổ sung thông tin người bệnh | ✓ | ✓ | ✓ | |
| Ghi báo cáo bệnh trong ngày (giao ca) | ✓ | ✓ | | |
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

## Cập nhật bệnh mới từ phần mềm bệnh viện (máy bàn)

Dùng cho máy tính bàn. Điện thoại, iPad dùng "+ Nhận bệnh" để nhập tay như cũ; nút này ẩn trên màn hình nhỏ.

1. Trong phần mềm bệnh viện, xuất **Danh sách bệnh nhân hiện diện** của khoa ra file Excel, đặt tên **a**, lưu vào thư mục **Downloads (Tải xuống)**. Nếu đã có file a cũ thì **lưu đè**, đừng để thành "a (1)".
2. Trong app, bấm **Cập nhật bệnh mới** (cạnh nút "+ Nhận bệnh").
   - Lần đầu: chọn file `a.xls` trong thư mục Tải xuống. Chrome, Edge sẽ nhớ file này cho những lần sau; mỗi lần mở lại trình duyệt có thể hỏi "Cho phép xem tệp?" một lần, bấm Cho phép.
3. App so danh sách trong file với sơ đồ:
   - **Không có bệnh mới:** app báo "Không có bệnh mới".
   - **Có bệnh mới (tối đa 10 người):** mở lần lượt bảng nhận bệnh cho từng người, đã điền sẵn họ tên, năm sinh, giới, mã bệnh nhân, ngày vào, mã ICD, nơi chuyển đến; chuyên khoa được **gợi ý theo mã ICD** (N… → Niệu; S06, I60–I62… → Thần kinh; còn lại → Tiêu hóa). Kiểm tra, chọn giường theo gợi ý hoặc tự chọn, rồi bấm **Lưu & xếp giường**. "Bỏ qua người này" để nhận sau; "Dừng lại" để xem bảng đối chiếu.
   - **Nhiều hơn 10 người** (ví dụ lần đầu đưa cả khoa vào): app hiện danh sách trước. Có thể xếp giường lần lượt, hoặc **đưa tất cả vào danh sách chờ giường** rồi xếp dần.
4. Bảng **Cần đối chiếu** liệt kê:
   - Ca **nhập tay** trùng họ tên và năm sinh với danh sách bệnh viện → **Gắn mã** (từ đó tự đối chiếu được).
   - Họ tên, năm sinh, giới **khác với** danh sách bệnh viện → **Sửa theo bệnh viện**.
   - Có trên sơ đồ nhưng **không còn** trong danh sách bệnh viện → có thể đã ra viện/chuyển khoa → **Ra khoa…**.
   - Nhập tay chưa có mã và không tìm thấy trong danh sách → kiểm tra lại.
   - Đã cho ra khoa trên sơ đồ nhưng **vẫn còn** trong danh sách bệnh viện → kiểm tra phần mềm bệnh viện.
   - Nếu file không phải vừa xuất (cũ hơn 2 giờ hoặc khác ngày), app nhắc xuất lại.

File chỉ được đọc trong trình duyệt của máy đó. Chỉ những người được bấm Lưu mới được đưa lên sơ đồ chung. Bộ đọc file Excel (SheetJS) được tải từ internet ở lần dùng đầu tiên.

**Danh sách khoa:** "Khoa chuyển đến" khi nhận bệnh và "Chuyển đến khoa" khi chuyển khoa chọn từ danh sách khoa trong Cài đặt (mục 4). Khoa mới xuất hiện trong file a được tự thêm vào; quản trị viên bổ sung các khoa còn thiếu.

## Báo cáo bệnh trong ngày (giao ca 7 giờ)

Bấm **Báo cáo** → **Báo cáo bệnh trong ngày**.

- **Kỳ báo cáo** từ 7:00 hôm trước đến 7:00 ngày báo cáo. Mở buổi sáng là báo cáo vừa chốt lúc 7 giờ; từ trưa trở đi là báo cáo của ca đang chạy, để trực đêm ghi dần. "Ngày trước / Ngày sau" để xem lại, tối đa 45 ngày.
- **Phần app tự tính**, từ giờ vào khoa và giờ ra khoa đã ghi trên sơ đồ:
  - Bảng tổng hợp: cũ đầu kỳ, nhập mới, khoa khác chuyển đến, từng hình thức ra khoa, còn cuối kỳ, kèm dòng đối chiếu.
  - Danh sách người bệnh mới; danh sách xuất viện, chuyển khoa, chuyển viện, tử vong, ra khoa khác.
- **Phần điều dưỡng ghi** (ô nền vàng, tự lưu sau khi gõ):
  - Người giao, người nhận.
  - Tình trạng và việc cần theo dõi của người bệnh mới; tình trạng, hồ sơ đã bàn giao của người ra viện.
  - Sự việc trong ca trực: bấm "+ Thêm" ở đúng nhóm; nhóm không có gì sẽ in "Không ghi nhận trong ca trực".
  - Công việc cần tiếp tục.
- **In / Lưu PDF** ra khổ A4, có chỗ ký của hai bên.
- **Để số liệu đúng:**
  - Khi nhận bệnh, ghi đúng giờ vào khoa. Mặc định là lúc nhận; bấm "Cập nhật bệnh mới" thì lấy giờ từ phần mềm bệnh viện.
  - Khi cho ra khoa, đi mổ mà ghi muộn, sửa lại ô "Thời điểm" cho đúng giờ thật.
  - Trước khi in báo cáo, nên bấm "Cập nhật bệnh mới" để biết người nào đã ra viện trên phần mềm bệnh viện mà chưa ra khoa trên sơ đồ.
- **Đi mổ** tính như chuyển khoa: lúc đi tính vào "Chuyển khoa khác" (chuyển mổ), lúc về tính vào "Khoa khác chuyển đến" (mổ về). Người đang ở phòng mổ lúc 7 giờ không tính vào "Còn cuối kỳ". Khi bấm "Mổ về", ghi đúng giờ về rồi bấm Xác nhận (giường cũ đã chọn sẵn).
- **Ra khoa khác** gồm xin về và trốn viện; tử vong là cột riêng.
- **Danh sách điều dưỡng** để chọn người giao, người nhận nằm ở Cài đặt mục 3, cạnh danh sách bác sĩ.

## Cấu hình máy tối thiểu

**Máy tính bàn hoặc xách tay**

- Windows 10 hoặc 11 (hoặc macOS), trình duyệt Chrome hoặc Edge bản mới, để tự cập nhật.
- Bộ xử lý 2 nhân bất kỳ đời từ khoảng 2015 trở lại đây; RAM 4 GB (8 GB nếu chạy song song phần mềm quản lý bệnh viện); ổ cứng trống 1 GB.
- Màn hình tối thiểu 1366×768; nên dùng 1920×1080 để thấy trọn hai dãy phòng.
- Bản dùng chung cần internet ổn định; lưu lượng nhỏ, khoảng vài chục MB mỗi ngày mỗi máy. Bản một máy không cần mạng.
- Máy in A4 nếu cần in danh sách.
- Windows 7, 8.1: Chrome và Edge đã ngừng cập nhật từ đầu năm 2023. App có thể vẫn chạy nhưng không an toàn, không khuyên dùng.
- **Máy ở quầy khoa hiện tại** (15/10/2026): Windows 7 Ultimate SP1, Pentium Dual-Core E5200 2,5 GHz, RAM 3 GB. Bác sĩ đã mở được link và chạy thử. Chrome cao nhất trên Windows 7 là bản 109, vẫn đủ cho app, kể cả nút "Cập nhật bệnh mới". Nhưng trình duyệt này không còn được vá lỗi bảo mật, nên khi bệnh viện thay máy, ưu tiên Windows 10/11.

**iPhone, iPad, điện thoại Android**

- iPhone hoặc iPad chạy iOS/iPadOS 15 trở lên, dùng Safari. Android dùng Chrome bản mới.
- Trên điện thoại, các phòng xếp thành thẻ hai cột để không phải kéo ngang. iPad xoay ngang thấy đủ sơ đồ hành lang.

## Thông tin dự án (để quản trị)

- Dự án `xep-giuong-khoa-ngoai` · mã `wcnxauujoraohokntryt` · vùng Singapore · gói miễn phí.
- Trang quản trị: https://supabase.com/dashboard/project/wcnxauujoraohokntryt
- Cơ sở dữ liệu: `thiet-lap.sql`. Quản lý tài khoản: `functions/quan-ly-tai-khoan/index.ts`.
- Gói miễn phí: tự tạm dừng nếu cả tuần không ai dùng (vào trang quản trị bấm khôi phục); không có sao lưu tự động. Máy chủ tự giữ một bản sơ đồ mỗi ngày trong 60 ngày, cách lấy lại ghi cuối file `thiet-lap.sql`.
- Chỉ nhập tên người bệnh thật sau khi bệnh viện đồng ý cho lưu dữ liệu trên Supabase.

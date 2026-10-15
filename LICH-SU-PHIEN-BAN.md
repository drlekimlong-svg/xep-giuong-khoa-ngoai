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

## 2.3-thu1 — 15/10/2026 — Nhận ra ca nhập tay sai/thiếu tên, bản xem thử để tập huấn

- **File:** `phien-ban/v2.3-thu1/XepGiuong_KhoaNgoai.html` · nhãn git `v2.3-thu1`. Máy chủ không đổi.
- **Bộ tập huấn** (ngoài kho, vì có file .xls): thư mục `tap-huan-xep-giuong` cạnh thư mục `xep-giuong`, gồm 5 file `a_TH1…TH5.xls` tên giả, mã giả 99…, và `KICH-BAN-TAP-HUAN.md`.

**Mới so với 2.2-thu2**

- **Đối chiếu ca nhập tay lúc gấp.** Trước đây app chỉ nhận ra khi trùng đúng họ tên (không kể dấu). Nay có thêm mục **"Có thể là người đã nhập tay lúc gấp"** cho các trường hợp:
  - Họ tên nhập thiếu, kể cả có cách gọi ở đầu như "Bà Lụa" ↔ Phạm Thị Lụa. Chỉ xét ca nhận trong 3 ngày nếu chỉ có một chữ tên.
  - Gõ sai 1–2 chữ, ví dụ Khanh ↔ Khang.
  - Cùng họ tên nhưng khác năm sinh.
  - Luôn phải cùng giới; năm sinh lệch quá 2 năm thì không xét.
  - Người nhận bệnh bấm **Đúng người – gắn mã** (có hỏi xác nhận) hoặc **Không phải**.
  - Có ca cần xác nhận thì app hiện bảng đối chiếu trước, không mở ngay bảng nhận bệnh, để tránh nhận trùng.
- **Khi gắn mã:** sửa họ tên, năm sinh, giới theo bệnh viện; điền thêm nơi chuyển đến và mã ICD nếu lúc nhập còn trống; nhật ký ghi lại tên cũ đã nhập.
- **Bản xem thử (`#mau`):**
  - Lưu riêng (khóa `xepgiuong.khoangoai.mau`), không bao giờ nối máy chủ. Nhờ vậy mở bản xem thử trên máy đang dùng bản một máy thật không đụng tới dữ liệu thật.
  - Tự nạp lại dữ liệu mẫu mới khi đổi phiên bản dữ liệu mẫu (`SAMPLE_VER`).
  - Dữ liệu mẫu có mã bệnh nhân giả, để tập "Cập nhật bệnh mới". Dải vàng có nút **Nạp lại dữ liệu mẫu**.
  - Nhớ file a riêng với bản thật; không cảnh báo file cũ.
- **Chặn lẫn file:**
  - File mẫu tập huấn có dòng "FILE MẪU TẬP HUẤN": bản thật từ chối đọc.
  - Bản xem thử chỉ đọc file mẫu, không đọc danh sách thật của bệnh viện.

**Đã thử** (trình duyệt, bản xem thử với 5 file mẫu)

- **TH1:** 3 bệnh mới mở lần lượt, lưu đủ; đọc lại thì báo không có bệnh mới.
- **TH2:** nhập tay "Nguyen Van Hai", "Bà Lụa", "Võ Minh Khanh". App nhận ra đủ 3 người; gắn mã thì sửa đúng họ tên, năm sinh, điền nơi chuyển đến và ICD, giường giữ nguyên. "Không phải" đưa người đó sang bệnh mới.
- **TH3:** 3 người không còn trong danh sách; người đang đi mổ có ghi chú.
- **TH4:** sai năm sinh, sai dấu, người đã cho ra viện mà bệnh viện vẫn còn.
- **TH5:** 26 người, hiện danh sách trước; đưa tất cả vào danh sách chờ đúng; gợi ý 16 Tiêu hóa, 8 Niệu, 2 Thần kinh.
- **Chặn lẫn file:** bản thật từ chối file mẫu; bản xem thử từ chối file không phải file mẫu. Dữ liệu bản xem thử không ghi vào chỗ lưu của bản thật.

**Chưa thử**

- Chưa thử trên máy Windows 7 ở khoa.

---

## 2.2-thu2 — 15/10/2026 — Đi mổ tính như chuyển khoa, thêm "Trốn viện"

- **File:** `phien-ban/v2.2-thu2/XepGiuong_KhoaNgoai.html` · nhãn git `v2.2-thu2`. Máy chủ không đổi.

**Mới so với 2.2-thu1** (theo quyết định của bác sĩ ngày 15/10/2026)

- **Đi mổ trong báo cáo giao ca:**
  - Đi mổ tính là "Chuyển khoa khác" (ghi chú "Chuyển mổ"); mổ về tính là "Khoa khác chuyển đến" (nơi chuyển đến "Phòng mổ (mổ về)"). Đi rồi về trong cùng kỳ thì có cả hai dòng.
  - Người đang ở phòng mổ lúc 7 giờ không tính vào "Còn cuối kỳ".
  - Đi mổ rồi không về khoa (chuyển hồi sức, tử vong…) chỉ tính một lần là chuyển mổ; ghi chú nêu kết cục.
- **Ghi từng lần đi mổ** (`p.ops`): giờ đi và giờ về. Bấm "Mổ về" nay luôn mở bảng xếp giường có ô **thời điểm mổ về**; giường cũ còn dùng được thì đã chọn sẵn, chỉ cần bấm Xác nhận.
- **Hình thức ra khoa "Trốn viện"**, tính vào "Ra khoa khác" cùng "Xin về". "Tử vong" vẫn là cột riêng như mẫu.
- **Đối chiếu file bệnh viện:** người đang đi mổ mà không có trong file được ghi chú là có thể đang ở khoa gây mê, nút đổi thành "Không về…".

**Đã thử** (bản một máy, dữ liệu mẫu)

- Báo cáo có dòng chuyển mổ và mổ về; người đang ở phòng mổ không tính vào "Còn cuối kỳ"; đối chiếu khớp. Số còn cuối kỳ của ngày trước vẫn bằng số cũ đầu kỳ của ngày sau.
- Mổ về: giường cũ được chọn sẵn; giờ về sớm hơn giờ đi bị chặn; lưu đúng giờ về.
- Đi mổ rồi "Không về" (chuyển khoa hồi sức): chỉ tăng một ở "Chuyển khoa khác".
- Trốn viện: vào cột "Ra khoa khác".

**Chưa thử**

- Như 2.2-thu1: chưa thử trên máy ở khoa, chưa in giấy thật, chưa thử với tài khoản điều dưỡng thật.

**Hạn chế**

- Những lần đi mổ ghi ở bản 2.2-thu1 mà đã về thì không có giờ về, nên không vào báo cáo. Hiện máy chủ chưa có người bệnh nào nên không ảnh hưởng.

---

## 2.2-thu1 — 15/10/2026 — Báo cáo bệnh trong ngày (giao ca 7 giờ), bấm chọn bác sĩ, giờ vào/ra khoa

- **File:** `phien-ban/v2.2-thu1/XepGiuong_KhoaNgoai.html` · nhãn git `v2.2-thu1`.
- **Máy chủ:**
  - Quy tắc `private.ward_state_check` thêm một điều: bác sĩ không sửa được báo cáo giao ca (`thiet-lap.sql` đã cập nhật).
  - Sơ đồ chung được thêm danh sách 13 điều dưỡng lấy từ bảng tài khoản.

**Mới so với 2.1-thu1**

- **Nút "Báo cáo"** (thay nút "Danh sách ngày") mở ra hai mục: *Báo cáo bệnh trong ngày* và *Danh sách người bệnh* (như cũ).
- **Báo cáo bệnh trong ngày** theo mẫu giao ca của bác sĩ. Kỳ báo cáo từ 7:00 hôm trước đến 7:00 ngày báo cáo; mở buổi sáng là báo cáo vừa chốt, từ trưa trở đi là báo cáo của ca đang chạy. Xem lại được 45 ngày.
  1. **Tổng hợp số lượng:** Cũ đầu kỳ · Nhập mới (cấp cứu, phòng khám) · Khoa khác chuyển đến · Xuất viện · Chuyển khoa · Chuyển viện · Tử vong · Ra khoa khác (xin về) · Còn cuối kỳ. App tự tính, có dòng đối chiếu Cũ + Vào − Ra = Còn, số còn theo chuyên khoa, số lượt đi mổ.
  2. **Nhập mới/chuyển đến:** họ tên – mã, tuổi/giới, giờ vào, nơi chuyển đến, chẩn đoán, buồng/giường; điều dưỡng ghi "tình trạng và việc cần theo dõi".
  3. **Xuất viện**, rồi từng nhóm chuyển khoa, chuyển viện, tử vong, ra khoa khác; điều dưỡng ghi tình trạng, hồ sơ/hướng dẫn đã bàn giao, ghi chú.
  4. **Đêm trực và sự việc phát sinh** theo 5 nhóm (người bệnh nặng, sự cố chăm sóc, an ninh trật tự, thiết bị/điện nước, khác); nhóm không có ghi "Không ghi nhận trong ca trực".
  - **Cuối trang:** công việc cần tiếp tục, người tiếp nhận, thời điểm bàn giao, chỗ ký hai bên.
  - **Lưu, in, quyền:** ô điều dưỡng ghi tự lưu sau khi gõ, lưu theo từng ô; nếu máy khác vừa lưu thì ô vẫn được ghi lại, không phải gõ lại. In hoặc lưu PDF khổ A4. Chỉ điều dưỡng và quản trị viên ghi được; bác sĩ và tài khoản chỉ xem thì xem và in.
- **Giờ vào khoa** (bắt buộc khi nhận bệnh mới, mặc định là lúc nhận; lấy từ file a khi cập nhật bệnh mới).
- **Thời điểm ra khoa, đi mổ:** mặc định là lúc bấm, sửa được khi ghi muộn. Không cho ghi giờ ở tương lai hay sớm hơn lúc vào khoa.
- **Bác sĩ phụ trách: bấm chọn** từ danh sách của khoa; tên chưa có thì chọn "Khác (gõ tên)…".
- **Danh sách điều dưỡng** trong Cài đặt mục 3, cạnh danh sách bác sĩ; điều dưỡng tạo tài khoản mới được tự thêm vào.

**Đã thử**

- **Bản một máy, dữ liệu mẫu:**
  - Số liệu báo cáo khớp đối chiếu; số còn cuối kỳ của ngày trước bằng số cũ đầu kỳ của ngày sau.
  - Ghi tay, thêm sự việc, ghi việc cần tiếp tục: đều lưu đúng.
  - Bản in có đủ các mục và chỗ ký.
  - Nhận bệnh mới có chọn bác sĩ "Khác", giờ "7g15": lưu đúng; giờ sai (25:00) bị chặn.
  - Ra khoa ghi lùi giờ: lưu đúng; giờ sớm hơn lúc vào, giờ ở tương lai: bị chặn.
- **Bản dùng chung trên máy chủ giả lập:**
  - Máy khác lưu đúng lúc đang ghi báo cáo: phần báo cáo được ghi lại, phần của máy kia vẫn còn, không hiện cảnh báo.
  - Thao tác thường bị máy khác lưu trước: vẫn cảnh báo như cũ.
  - Tài khoản bác sĩ: báo cáo chỉ xem.
- **Cơ sở dữ liệu thật** (thử rồi hủy, không để lại dữ liệu): bác sĩ sửa báo cáo bị từ chối, bác sĩ sửa phần khác vẫn được, điều dưỡng sửa báo cáo được.

**Chưa thử**

- Chưa thử trên máy Windows 7 ở khoa, chưa in ra giấy thật, chưa thử với tài khoản điều dưỡng thật.

**Hạn chế**

- **Số liệu tính theo giờ đã ghi trên app:** nếu ra viện trên phần mềm bệnh viện mà chưa bấm ra khoa trên app thì báo cáo sẽ thiếu. Nên bấm "Cập nhật bệnh mới" trước khi in để đối chiếu.
- **Người nhận trước bản này chưa có giờ vào khoa:** tạm tính là 7:00 ngày vào, có ghi "(chưa ghi giờ)".
- **Đi mổ không tính là ra khoa:** người đang ở phòng mổ vẫn tính trong "Còn cuối kỳ", số lượt đi mổ ghi riêng.
- **Buồng/giường trong báo cáo** là vị trí hiện tại, không phải vị trí lúc 7 giờ.
- **Lịch sử ra khoa giữ 300 người gần nhất**, nên báo cáo của những ngày quá xa có thể thiếu.

---

## 2.1-thu1 — 15/10/2026 — Lấy bệnh mới từ phần mềm bệnh viện, phân khu mới, phòng dự phòng, danh sách khoa

- **File:** `phien-ban/v2.1-thu1/XepGiuong_KhoaNgoai.html` · nhãn git `v2.1-thu1`. Máy chủ: cơ sở dữ liệu và Edge Function không đổi; sơ đồ chung trên máy chủ được cập nhật phân khu mới (lúc đó chưa có người bệnh nào).

**Mới so với 2.0-thu4**

- **Phân khu mới** (bác sĩ quyết định 15/10/2026):
  - Niệu: 612 (Nam), 614 (Nữ), 610 (linh hoạt), 609 (Nam), 608 (Nữ), 607 (linh hoạt), tổng 23 giường.
  - Tiêu hóa và Thần kinh: các phòng còn lại, giới như cũ, 618 thành Nam; tổng 42 giường, kể cả 619.
  - Tạm bỏ chuyên khoa Lồng ngực – Mạch máu (ẩn khỏi lựa chọn, hồ sơ cũ vẫn giữ).
  - Kiểm tra "Niệu đủ phòng Nam/Nữ" nay chỉ xét phòng 3, 4, 6 giường.
- **Phòng dự phòng** (619): chỉ được gợi ý khi các phòng khác đã hết giường đúng giới. Có thẻ "Dự phòng" trên sơ đồ, cảnh báo khi tự chọn, nhắc chuyển ra khi có giường thường. Bật/tắt trong Cài đặt.
- **Nút "Cập nhật bệnh mới"** (máy bàn), đọc file `a.xls` (Danh sách bệnh nhân hiện diện) xuất từ phần mềm bệnh viện:
  - Nhận ra các cột theo nội dung, vì file không có dòng tiêu đề.
  - Bệnh mới mở lần lượt bảng nhận bệnh điền sẵn, gợi ý chuyên khoa theo ICD, gợi ý giường; nhiều hơn 10 người thì hiện danh sách trước, có nút đưa tất cả vào danh sách chờ.
  - Bảng đối chiếu: ca nhập tay trùng tên (gắn mã), thông tin sai khác (sửa theo bệnh viện), người không còn trong danh sách (ra khoa), người đã ra khoa nhưng vẫn còn trong danh sách.
  - Nhắc khi file cũ; Chrome/Edge nhớ file đã chọn.
- **Mã bệnh nhân** của phần mềm bệnh viện: lưu cho từng người, nhập tay được, chặn trùng mã, có trong file Excel xuất ra và tìm kiếm được.
- **Danh sách khoa:** "Khoa chuyển đến" khi nhận bệnh, "Chuyển đến khoa" (bắt buộc) khi chuyển khoa; hiện trong hồ sơ, lịch sử, file Excel. Sửa trong Cài đặt mục 4; khoa mới trong file a được tự thêm.

**Đã thử**

- **Với file thử cùng cấu trúc, tên giả** (8 người), ở bản một máy trên khổ màn hình máy bàn:
  - Bệnh mới mở lần lượt và điền sẵn đúng; lưu, bỏ qua, dừng giữa chừng đều đúng.
  - Ca nhập tay được nhận ra và gắn mã; sai năm sinh được báo và sửa; người không còn trong danh sách được báo.
  - "Đưa tất cả vào danh sách chờ" chạy đúng; khoa mới "Nội Thận" được tự thêm.
- **Phòng 619:** không nằm trong 6 gợi ý đầu khi còn giường khác; tự chọn có cảnh báo; có đề xuất "rời phòng dự phòng".
- **Chuyển khoa:** bắt buộc ghi khoa; hiện trong lịch sử.
- **Với file `a.xls` thật của khoa** (đọc trên máy này, không lưu, không gửi đi): nhận đủ 50 người; mã, năm sinh, giới, giờ vào, khoa chuyển đến khớp với file; gợi ý 31 Tiêu hóa, 17 Niệu, 2 Thần kinh.

**Chưa thử**

- Chưa thử trên máy ở khoa (Windows 7, Chrome 109), nhất là bước Chrome nhớ file a.
- Chưa thử ở bản dùng chung với tài khoản điều dưỡng thật.
- Chưa thử với file có người bệnh mới thật xen giữa người cũ.

**Hạn chế đã biết**

- Phần mềm bệnh viện không xuất chẩn đoán bằng chữ và bác sĩ phụ trách, nên chỉ có mã ICD; cần gõ thêm nếu muốn.
- Gợi ý chuyên khoa theo ICD có thể sai, ví dụ chấn thương cột sống thắt lưng S32; người nhận bệnh phải kiểm tra.
- Bộ đọc Excel tải từ internet (cdn.sheetjs.com) ở lần dùng đầu; mất mạng thì không đọc được file, vẫn nhập tay được.
- Khi đã nhập tên người bệnh thật lên bản dùng chung, dữ liệu nằm trên máy chủ Supabase ở Singapore; cần bệnh viện đồng ý.

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

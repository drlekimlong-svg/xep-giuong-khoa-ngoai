# Bật dùng chung nhiều máy qua Supabase

Làm một lần, khoảng 15 phút. Tên các mục trong trang Supabase có thể khác đôi chút theo thời gian.

> Trong giai đoạn thử, chỉ dùng dữ liệu mẫu hoặc tên giả. Chỉ nhập tên người bệnh thật sau khi bệnh viện đồng ý cho lưu dữ liệu trên Supabase.

## 1. Tạo dự án

1. Vào https://supabase.com, đăng nhập (hoặc tạo tài khoản miễn phí).
2. Bấm **New project**. Đặt tên, ví dụ `xep-giuong-khoa-ngoai`.
3. **Region:** chọn Southeast Asia (Singapore) – gần Việt Nam nhất.
4. **Database password:** để Supabase tự tạo rồi cất vào nơi an toàn. App không cần mật khẩu này.

## 2. Tạo bảng và quy tắc bảo mật

1. Mở **SQL Editor** → **New query**.
2. Mở file `thiet-lap.sql` (cùng thư mục với file này), chép toàn bộ, dán vào, bấm **Run**.
3. Kết quả đúng là dòng "Success. No rows returned".

## 3. Tắt tự đăng ký

**Authentication** → **Sign In / Providers** → tắt **Allow new users to sign up**.
Từ đó chỉ người quản trị tạo được tài khoản.

## 4. Tạo tài khoản cho từng người

1. **Authentication** → **Users** → **Add user** → **Create new user**.
2. Nhập email, mật khẩu, bật **Auto Confirm User**.
3. Vào **SQL Editor**, chạy lệnh sau (sửa email, tên, quyền):

```sql
insert into public.staff (user_id, full_name, role)
select id, 'ĐD Nguyễn Thị A', 'edit' from auth.users where email = 'email-cua-nguoi-do@vi-du.vn'
on conflict (user_id) do update set full_name = excluded.full_name, role = excluded.role;
```

Quyền `edit` là được sửa (điều dưỡng xếp giường). Quyền `view` là chỉ xem và in (bác sĩ đi buồng).
Tài khoản đã tạo ở bước 1–2 mà chưa chạy lệnh này thì đăng nhập sẽ bị báo "chưa được cấp quyền vào khoa".

## 5. Lấy địa chỉ dự án và khóa công khai

**Project Settings** → **API Keys** (hoặc **API**):

- **Project URL**, dạng `https://abcdefgh.supabase.co`
- **Publishable key** (dự án cũ ghi là `anon` `public`)

Hai giá trị này được phép công khai. **Không** dùng và không gửi cho ai khóa `secret` / `service_role`.

## 6. Kết nối app

**Thử trên một máy:** mở app → **Cài đặt** → mục **Dùng chung nhiều máy** → dán hai giá trị → **Kết nối** → đăng nhập.
Dữ liệu một máy đang có trong trình duyệt vẫn giữ nguyên; bấm "Ngắt kết nối" là quay lại như cũ.

**Cho mọi máy tự kết nối:** điền hai giá trị vào dòng `CLOUD_DEFAULT` ở đầu phần chương trình trong file `XepGiuong_KhoaNgoai.html`, rồi phát hành bản mới.

## 7. Đưa dữ liệu từ bản một máy lên

Ở máy đang dùng bản một máy: **Sao lưu ra file ngay**. Ở bản dùng chung (tài khoản quyền `edit`): **Cài đặt** → **Khôi phục từ file** → chọn file vừa tải.

## Điều cần biết

- **Hai máy sửa cùng lúc:** máy lưu sau sẽ bị từ chối, sơ đồ tự tải lại và app báo để làm lại. Không có chuyện ghi đè lên nhau.
- **Mất mạng:** app báo đỏ ở góc trên và tự thử lại. Nếu trong lúc đó máy khác đã sửa thì thay đổi chưa lưu của máy này bị bỏ.
- **Sao lưu:** máy chủ giữ một bản mỗi ngày trong 60 ngày (bảng `ward_state_daily`); cách lấy lại ghi ở cuối file `thiet-lap.sql`.
- **Gói miễn phí:** dự án tự tạm dừng nếu cả tuần không ai dùng; vào trang Supabase bấm khôi phục là chạy lại.
- **Dữ liệu trên máy:** bản dùng chung không để lại dữ liệu người bệnh trong trình duyệt sau khi đăng xuất.

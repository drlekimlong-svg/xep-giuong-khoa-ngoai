-- ============================================================================
-- App xếp giường khoa Ngoại – thiết lập Supabase
-- Chạy MỘT LẦN: Supabase → SQL Editor → dán toàn bộ file này → Run.
-- Chạy lại nhiều lần cũng không sao, không làm mất dữ liệu.
-- ============================================================================

-- 1. Danh sách người được vào khoa. Tài khoản đăng nhập mà không có dòng ở đây
--    thì không đọc, không ghi được gì.
create table if not exists public.staff (
  user_id   uuid primary key references auth.users (id) on delete cascade,
  full_name text not null,
  role      text not null default 'edit' check (role in ('edit', 'view'))   -- edit: được sửa · view: chỉ xem
);

-- 2. Sơ đồ giường: mỗi khoa một dòng, cả sơ đồ nằm trong cột data.
--    Cột version tăng 1 sau mỗi lần lưu; app chỉ lưu được khi version còn khớp,
--    nhờ đó hai máy không ghi đè lên nhau.
create table if not exists public.ward_state (
  id         text primary key,
  data       jsonb not null,
  version    bigint not null default 1,
  updated_at timestamptz not null default now(),
  updated_by text
);

-- 3. Bản lưu mỗi ngày: sơ đồ trước lần sửa đầu tiên của ngày, giữ 60 ngày.
--    Gói miễn phí của Supabase không có sao lưu tự động nên tự giữ ở đây.
create table if not exists public.ward_state_daily (
  id       text not null,
  day      date not null,
  data     jsonb not null,
  saved_at timestamptz not null default now(),
  primary key (id, day)
);

-- Mỗi lần sơ đồ được sửa: giữ bản đầu ngày, tăng version, ghi giờ sửa.
create or replace function public.ward_state_touch() returns trigger
language plpgsql security definer set search_path = public as $$
declare
  today date := (now() at time zone 'Asia/Ho_Chi_Minh')::date;
begin
  insert into public.ward_state_daily (id, day, data)
  values (old.id, today, old.data)
  on conflict (id, day) do nothing;
  delete from public.ward_state_daily where id = old.id and day < today - 60;
  new.id := old.id;
  new.version := old.version + 1;
  new.updated_at := now();
  return new;
end $$;

drop trigger if exists ward_state_touch on public.ward_state;
create trigger ward_state_touch before update on public.ward_state
  for each row execute function public.ward_state_touch();

-- Quyền của người đang đăng nhập: 'edit', 'view', hoặc null nếu không thuộc khoa.
-- Chỉ đọc dòng staff của chính người gọi (quy tắc RLS của bảng staff cho phép), nên không cần security definer.
create or replace function public.my_role() returns text
language sql stable security invoker set search_path = public as $$
  select role from public.staff where user_id = (select auth.uid())
$$;

revoke all on function public.my_role() from public, anon;
grant execute on function public.my_role() to authenticated;
revoke all on function public.ward_state_touch() from public, anon, authenticated;

-- 4. Bật kiểm soát theo dòng (RLS): không có quy tắc cho phép thì bị từ chối.
alter table public.staff            enable row level security;
alter table public.ward_state       enable row level security;
alter table public.ward_state_daily enable row level security;

drop policy if exists "nhan vien xem dong cua minh"   on public.staff;
drop policy if exists "nhan vien doc so do"           on public.ward_state;
drop policy if exists "nguoi duoc sua tao so do"      on public.ward_state;
drop policy if exists "nguoi duoc sua cap nhat so do" on public.ward_state;
drop policy if exists "nhan vien doc ban luu ngay"    on public.ward_state_daily;

create policy "nhan vien xem dong cua minh" on public.staff
  for select to authenticated using (user_id = (select auth.uid()));

create policy "nhan vien doc so do" on public.ward_state
  for select to authenticated using (public.my_role() is not null);

create policy "nguoi duoc sua tao so do" on public.ward_state
  for insert to authenticated with check (public.my_role() = 'edit');

create policy "nguoi duoc sua cap nhat so do" on public.ward_state
  for update to authenticated using (public.my_role() = 'edit') with check (public.my_role() = 'edit');

create policy "nhan vien doc ban luu ngay" on public.ward_state_daily
  for select to authenticated using (public.my_role() is not null);

-- Không có quy tắc nào cho xóa: không ai xóa được sơ đồ qua app.
-- Người chưa đăng nhập (anon) không có quyền gì trên ba bảng này.
revoke all on public.staff, public.ward_state, public.ward_state_daily from anon;
revoke all on public.staff, public.ward_state, public.ward_state_daily from authenticated;
grant select                 on public.staff            to authenticated;
grant select, insert, update on public.ward_state       to authenticated;
grant select                 on public.ward_state_daily to authenticated;

-- ============================================================================
-- CẤP QUYỀN CHO MỘT TÀI KHOẢN
-- Bước 1: Authentication → Users → Add user → nhập email, mật khẩu, bật "Auto Confirm User".
-- Bước 2: chạy lệnh dưới đây (bỏ hai dấu gạch đầu dòng), sửa email, tên và quyền:
--
--   insert into public.staff (user_id, full_name, role)
--   select id, 'ĐD Nguyễn Thị A', 'edit' from auth.users where email = 'email-cua-nguoi-do@vi-du.vn'
--   on conflict (user_id) do update set full_name = excluded.full_name, role = excluded.role;
--
-- Thu hồi quyền:   delete from public.staff where user_id = (select id from auth.users where email = '...');
-- Xem ai có quyền: select u.email, s.full_name, s.role from public.staff s join auth.users u on u.id = s.user_id;
--
-- LẤY LẠI SƠ ĐỒ CỦA MỘT NGÀY TRƯỚC (khi lỡ xóa nhầm), ví dụ ngày 20/10/2026:
--   update public.ward_state w set data = d.data
--   from public.ward_state_daily d where d.id = w.id and w.id = 'khoa-ngoai' and d.day = '2026-10-20';
-- ============================================================================

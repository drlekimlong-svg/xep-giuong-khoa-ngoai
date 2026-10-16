-- ============================================================================
-- App xếp giường khoa Ngoại – thiết lập Supabase (trạng thái từ bản 2.0-thu3, 14/10/2026)
-- Dùng khi cần dựng lại dự án: Supabase → SQL Editor → dán toàn bộ file → Run.
-- Chạy lại nhiều lần cũng không sao, không làm mất dữ liệu.
-- Kèm theo: Edge Function supabase/functions/quan-ly-tai-khoan (tạo và quản lý tài khoản).
-- ============================================================================

-- Schema riêng: không mở qua API (/rest/v1/rpc không gọi được), chỉ dùng trong quy tắc RLS và trigger.
create schema if not exists private;
grant usage on schema private to authenticated;

-- 1. Người được vào khoa. Tài khoản đăng nhập mà không có dòng ở đây (hoặc active = false) thì không làm được gì.
--    Vai trò: admin = quản trị viên (chỉ một người) · nurse = điều dưỡng · doctor = bác sĩ · view = chỉ xem.
create table if not exists public.staff (
  user_id     uuid primary key references auth.users (id) on delete cascade,
  full_name   text not null,
  role        text not null default 'view',
  login_id    text,                                   -- mã đăng nhập, vd LNKhoi (quản trị viên dùng email nên để trống)
  must_change boolean not null default false,         -- phải đổi mật khẩu ở lần đăng nhập tới
  active      boolean not null default true,          -- false = đã khóa
  created_at  timestamptz not null default now()
);
alter table public.staff add column if not exists login_id    text;
alter table public.staff add column if not exists must_change boolean not null default false;
alter table public.staff add column if not exists active      boolean not null default true;
alter table public.staff add column if not exists created_at  timestamptz not null default now();
alter table public.staff drop constraint if exists staff_role_check;
-- headnurse = điều dưỡng trưởng: như điều dưỡng, thêm quyền xóa/khôi phục hồ sơ nhập trùng, nhập nhầm (từ bản 2.4)
alter table public.staff add constraint staff_role_check check (role in ('admin', 'nurse', 'headnurse', 'doctor', 'view'));
create unique index if not exists staff_one_admin on public.staff ((true)) where role = 'admin';
create unique index if not exists staff_login_id_key on public.staff (lower(login_id)) where login_id is not null;

-- 2. Sơ đồ giường: mỗi khoa một dòng, cả sơ đồ nằm trong cột data.
--    version tăng 1 sau mỗi lần lưu; app chỉ lưu được khi version còn khớp, nhờ đó hai máy không ghi đè nhau.
create table if not exists public.ward_state (
  id         text primary key,
  data       jsonb not null,
  version    bigint not null default 1,
  updated_at timestamptz not null default now(),
  updated_by text
);

-- 3. Bản lưu mỗi ngày: sơ đồ trước lần sửa đầu tiên của ngày, giữ 60 ngày (gói miễn phí không có sao lưu tự động).
create table if not exists public.ward_state_daily (
  id       text not null,
  day      date not null,
  data     jsonb not null,
  saved_at timestamptz not null default now(),
  primary key (id, day)
);

-- Vai trò của người đang đăng nhập (null nếu không thuộc khoa hoặc đã bị khóa).
create or replace function private.my_role() returns text
language sql stable security definer set search_path = public as $$
  select role from public.staff where user_id = (select auth.uid()) and active
$$;
revoke all on function private.my_role() from public, anon;
grant execute on function private.my_role() to authenticated;
drop function if exists public.my_role();

-- Vị trí giường của từng người bệnh, để so sánh trước/sau một lần lưu.
create or replace function private.bed_map(d jsonb) returns jsonb
language sql immutable set search_path = public as $$
  select coalesce(jsonb_object_agg(p->>'id', jsonb_build_object(
           'room', p->'room', 'bed', p->'bed', 'away', coalesce(p->'away', 'false'::jsonb),
           'keepRoom', p->'keepRoom', 'keepBed', p->'keepBed')), '{}'::jsonb)
  from jsonb_array_elements(coalesce(d->'patients', '[]'::jsonb)) p
$$;
revoke all on function private.bed_map(jsonb) from public, anon;

-- Kiểm quyền theo nội dung thay đổi (RLS chỉ biết ai được ghi, không biết ghi phần nào):
--   chỉ quản trị viên đổi được phân khu, chuyên khoa, tên khoa;
--   bác sĩ chỉ bổ sung thông tin, không đổi vị trí giường, không nhận bệnh, không cho ra khoa.
create or replace function private.ward_state_check() returns trigger
language plpgsql security definer set search_path = public, private as $$
declare
  r text := private.my_role();
begin
  if (select auth.uid()) is null then return new; end if;   -- thao tác từ trang quản trị Supabase
  if r is distinct from 'admin' and (new.data->'rooms' is distinct from old.data->'rooms'
       or new.data->'specs' is distinct from old.data->'specs' or new.data->'ward' is distinct from old.data->'ward') then
    raise exception 'Chỉ quản trị viên được đổi phân khu, chuyên khoa và tên khoa.' using errcode = '42501';
  end if;
  if r = 'doctor' and (private.bed_map(new.data) is distinct from private.bed_map(old.data)
       or new.data->'discharged' is distinct from old.data->'discharged') then
    raise exception 'Bác sĩ chỉ được bổ sung thông tin, không được nhận bệnh, xếp giường hay cho ra khoa.' using errcode = '42501';
  end if;
  -- báo cáo bệnh trong ngày (giao ca) do điều dưỡng ghi; bác sĩ chỉ xem và in (từ bản 2.2; thiếu mục = rỗng)
  if r = 'doctor' and coalesce(new.data->'reports', '{}'::jsonb) is distinct from coalesce(old.data->'reports', '{}'::jsonb) then
    raise exception 'Báo cáo giao ca do điều dưỡng ghi; bác sĩ chỉ xem và in.' using errcode = '42501';
  end if;
  -- hồ sơ đã xóa (nhập trùng, nhập nhầm): chỉ quản trị viên và điều dưỡng trưởng được xóa hoặc khôi phục (từ bản 2.4)
  if (r is null or r not in ('admin', 'headnurse'))
     and coalesce(new.data->'deleted', '[]'::jsonb) is distinct from coalesce(old.data->'deleted', '[]'::jsonb) then
    raise exception 'Chỉ quản trị viên và điều dưỡng trưởng được xóa hoặc khôi phục hồ sơ.' using errcode = '42501';
  end if;
  return new;
end $$;
revoke all on function private.ward_state_check() from public, anon, authenticated;

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
revoke all on function public.ward_state_touch() from public, anon, authenticated;

-- Hai trigger chạy theo thứ tự tên: kiểm quyền trước (a_check), rồi mới ghi bản lưu và tăng version (touch).
drop trigger if exists ward_state_a_check on public.ward_state;
create trigger ward_state_a_check before update on public.ward_state
  for each row execute function private.ward_state_check();
drop trigger if exists ward_state_touch on public.ward_state;
create trigger ward_state_touch before update on public.ward_state
  for each row execute function public.ward_state_touch();

-- 4. Quy tắc RLS: không có quy tắc cho phép thì bị từ chối.
alter table public.staff            enable row level security;
alter table public.ward_state       enable row level security;
alter table public.ward_state_daily enable row level security;

drop policy if exists "nhan vien xem dong cua minh"                on public.staff;
drop policy if exists "xem dong cua minh, quan tri xem tat ca"     on public.staff;
drop policy if exists "nhan vien doc so do"                        on public.ward_state;
drop policy if exists "nguoi duoc sua tao so do"                   on public.ward_state;
drop policy if exists "nguoi duoc sua cap nhat so do"              on public.ward_state;
drop policy if exists "quan tri va dieu duong tao so do"           on public.ward_state;
drop policy if exists "quan tri dieu duong bac si cap nhat so do"  on public.ward_state;
drop policy if exists "nhan vien doc ban luu ngay"                 on public.ward_state_daily;

create policy "xem dong cua minh, quan tri xem tat ca" on public.staff
  for select to authenticated using (user_id = (select auth.uid()) or private.my_role() = 'admin');

create policy "nhan vien doc so do" on public.ward_state
  for select to authenticated using (private.my_role() is not null);

create policy "quan tri va dieu duong tao so do" on public.ward_state
  for insert to authenticated with check (private.my_role() in ('admin', 'nurse', 'headnurse'));

create policy "quan tri dieu duong bac si cap nhat so do" on public.ward_state
  for update to authenticated using (private.my_role() in ('admin', 'nurse', 'headnurse', 'doctor'))
  with check (private.my_role() in ('admin', 'nurse', 'headnurse', 'doctor'));

create policy "nhan vien doc ban luu ngay" on public.ward_state_daily
  for select to authenticated using (private.my_role() is not null);

-- Không có quy tắc xóa: không ai xóa được sơ đồ qua app. Thêm, sửa, khóa tài khoản chỉ qua Edge Function
-- quan-ly-tai-khoan (chạy bằng khóa service_role ở máy chủ, chỉ nhận lệnh của quản trị viên).
revoke all on public.staff, public.ward_state, public.ward_state_daily from anon;
revoke all on public.staff, public.ward_state, public.ward_state_daily from authenticated;
grant select                 on public.staff            to authenticated;
grant select, insert, update on public.ward_state       to authenticated;
grant select                 on public.ward_state_daily to authenticated;

-- ============================================================================
-- QUẢN TRỊ VIÊN (làm một lần khi dựng lại dự án)
-- Tạo tài khoản của quản trị viên ở Authentication → Users → Add user (email thật, bật Auto Confirm), rồi:
--
--   insert into public.staff (user_id, full_name, role)
--   select id, 'BS.KimLong', 'admin' from auth.users where email = 'dr.lekimlong@gmail.com'
--   on conflict (user_id) do update set role = 'admin';
--
-- Mọi tài khoản khác tạo trong app: đăng nhập bằng tài khoản quản trị → nút "Tài khoản".
--
-- LẤY LẠI SƠ ĐỒ CỦA MỘT NGÀY TRƯỚC (khi lỡ xóa nhầm), ví dụ ngày 20/10/2026:
--   update public.ward_state w set data = d.data
--   from public.ward_state_daily d where d.id = w.id and w.id = 'khoa-ngoai' and d.day = '2026-10-20';
-- ============================================================================

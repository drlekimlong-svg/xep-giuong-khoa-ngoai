// Edge Function "quan-ly-tai-khoan": tạo và quản lý tài khoản đăng nhập của khoa.
//
// Chỉ quản trị viên (staff.role = 'admin') được tạo, sửa, khóa tài khoản và đặt lại mật khẩu.
// Mọi người đã đăng nhập đều được tự đổi mật khẩu của mình (bắt buộc ở lần đăng nhập đầu).
// Khóa service_role chỉ nằm ở máy chủ Supabase (biến môi trường), không bao giờ tới trình duyệt.
//
// Đăng nhập bằng mã (vd LNKhoi): mã được đổi thành địa chỉ nội bộ lnkhoi@khoangoai.invalid.
// Đuôi ".invalid" là tên miền dành riêng, không bao giờ nhận thư, nên không có thư nào bị gửi đi.
import { createClient } from "npm:@supabase/supabase-js@2";

const DOMAIN = "khoangoai.invalid";
const ROLES = ["nurse", "doctor", "view"]; // quản trị viên chỉ có một, không tạo thêm qua đây

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function reply(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json; charset=utf-8" },
  });
}

function weakPassword(pw: string): string | null {
  if (pw.length < 8) return "Mật khẩu phải có ít nhất 8 ký tự.";
  if (!/[A-Za-z]/.test(pw) || !/[0-9]/.test(pw)) return "Mật khẩu phải có cả chữ và số.";
  return null;
}

function cleanText(v: unknown, max: number): string {
  return String(v ?? "").replace(/\s+/g, " ").trim().slice(0, max);
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });
  if (req.method !== "POST") return reply(405, { error: "Chỉ nhận yêu cầu POST." });

  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return reply(400, { error: "Dữ liệu gửi lên không hợp lệ." });
  }
  const action = String(body.action ?? "");

  // Xác thực người gọi bằng chính máy chủ đăng nhập của Supabase.
  const token = (req.headers.get("Authorization") ?? "").replace(/^Bearer\s+/i, "");
  if (!token) return reply(401, { error: "Chưa đăng nhập." });
  const { data: who, error: whoErr } = await admin.auth.getUser(token);
  if (whoErr || !who?.user) return reply(401, { error: "Phiên đăng nhập không hợp lệ hoặc đã hết hạn." });
  const me = who.user;

  const { data: mine } = await admin.from("staff").select("role, active").eq("user_id", me.id).maybeSingle();
  if (!mine || !mine.active) return reply(403, { error: "Tài khoản không thuộc khoa hoặc đã bị khóa." });

  // ---- ai cũng được: tự đổi mật khẩu ----
  if (action === "doi-mat-khau") {
    const pw = String(body.password ?? "");
    const bad = weakPassword(pw);
    if (bad) return reply(400, { error: bad });
    const { error } = await admin.auth.admin.updateUserById(me.id, { password: pw });
    if (error) return reply(400, { error: "Không đổi được mật khẩu: " + error.message });
    await admin.from("staff").update({ must_change: false }).eq("user_id", me.id);
    return reply(200, { ok: true });
  }

  if (mine.role !== "admin") return reply(403, { error: "Chỉ quản trị viên được quản lý tài khoản." });

  // ---- quản trị viên ----
  if (action === "danh-sach") {
    const { data: rows, error } = await admin.from("staff")
      .select("user_id, full_name, login_id, role, active, must_change, created_at").order("created_at");
    if (error) return reply(500, { error: error.message });
    const users = new Map<string, { email?: string; last_sign_in_at?: string }>();
    for (let page = 1; page <= 20; page++) {
      const { data, error: e } = await admin.auth.admin.listUsers({ page, perPage: 200 });
      if (e || !data) break;
      for (const u of data.users) users.set(u.id, u);
      if (data.users.length < 200) break;
    }
    return reply(200, {
      staff: (rows ?? []).map((r) => ({
        ...r,
        email: users.get(r.user_id)?.email ?? null,
        last_sign_in_at: users.get(r.user_id)?.last_sign_in_at ?? null,
      })),
    });
  }

  if (action === "tao") {
    const fullName = cleanText(body.full_name, 120);
    const loginId = cleanText(body.login_id, 40);
    const role = String(body.role ?? "");
    const pw = String(body.password ?? "");
    if (!fullName) return reply(400, { error: "Thiếu họ tên." });
    if (!/^[A-Za-z0-9._-]{2,40}$/.test(loginId)) return reply(400, { error: "Tên đăng nhập chỉ gồm chữ không dấu, số, dấu chấm, gạch (2–40 ký tự)." });
    if (!ROLES.includes(role)) return reply(400, { error: "Vai trò không hợp lệ." });
    const bad = weakPassword(pw);
    if (bad) return reply(400, { error: bad });

    const { data: taken } = await admin.from("staff").select("user_id").ilike("login_id", loginId).maybeSingle();
    if (taken) return reply(409, { error: "Tên đăng nhập " + loginId + " đã có." });

    const { data: created, error } = await admin.auth.admin.createUser({
      email: loginId.toLowerCase() + "@" + DOMAIN,
      password: pw,
      email_confirm: true,
      user_metadata: { login_id: loginId, full_name: fullName },
    });
    if (error || !created?.user) {
      const msg = error?.message ?? "";
      return reply(400, { error: /already|registered|exists/i.test(msg) ? "Tên đăng nhập " + loginId + " đã có." : "Không tạo được tài khoản: " + msg });
    }
    const { error: e2 } = await admin.from("staff").insert({
      user_id: created.user.id, full_name: fullName, login_id: loginId, role, must_change: true,
    });
    if (e2) {
      await admin.auth.admin.deleteUser(created.user.id); // không để lại tài khoản lửng
      return reply(400, { error: "Không lưu được vào danh sách khoa: " + e2.message });
    }
    return reply(200, { ok: true, user_id: created.user.id });
  }

  if (action === "sua") {
    const userId = String(body.user_id ?? "");
    if (!userId) return reply(400, { error: "Thiếu tài khoản cần sửa." });
    if (userId === me.id) return reply(400, { error: "Quản trị viên không tự đổi vai trò hay tự khóa mình." });
    const patch: Record<string, unknown> = {};
    if (body.full_name !== undefined) {
      const fullName = cleanText(body.full_name, 120);
      if (!fullName) return reply(400, { error: "Thiếu họ tên." });
      patch.full_name = fullName;
    }
    if (body.role !== undefined) {
      if (!ROLES.includes(String(body.role))) return reply(400, { error: "Vai trò không hợp lệ." });
      patch.role = String(body.role);
    }
    if (body.active !== undefined) patch.active = !!body.active;
    const { data, error } = await admin.from("staff").update(patch).eq("user_id", userId).neq("role", "admin").select("user_id");
    if (error) return reply(400, { error: error.message });
    if (!data?.length) return reply(404, { error: "Không tìm thấy tài khoản." });
    return reply(200, { ok: true });
  }

  if (action === "dat-lai-mat-khau") {
    const userId = String(body.user_id ?? "");
    const pw = String(body.password ?? "");
    if (!userId) return reply(400, { error: "Thiếu tài khoản cần đặt lại mật khẩu." });
    if (userId === me.id) return reply(400, { error: "Muốn đổi mật khẩu của mình, dùng nút Đổi mật khẩu." });
    const bad = weakPassword(pw);
    if (bad) return reply(400, { error: bad });
    const { data: row } = await admin.from("staff").select("role").eq("user_id", userId).maybeSingle();
    if (!row) return reply(404, { error: "Không tìm thấy tài khoản." });
    const { error } = await admin.auth.admin.updateUserById(userId, { password: pw });
    if (error) return reply(400, { error: "Không đặt lại được mật khẩu: " + error.message });
    await admin.from("staff").update({ must_change: true }).eq("user_id", userId);
    return reply(200, { ok: true });
  }

  return reply(400, { error: "Không rõ thao tác." });
});

# -*- coding: utf-8 -*-
"""Tạo danh mục ICD-10 gợi ý cho ô Chẩn đoán của app xếp giường (từ bản 2.7).

Nguồn tên bệnh: danh mục ICD-10 ban hành kèm TT 06/2026/TT-BYT (áp dụng từ 01/07/2026),
bản điện tử FHIR của HL7 Việt Nam:
  https://downloads.fhir.hl7.org.vn/core/0.10.0/terminology/clinical/CodeSystem-vn-icd10-cs.full.json
Chỉ giữ các nhóm bệnh khoa Ngoại hay gặp (khoảng 2.200 mã), thêm từ khóa thường gõ (VRT, CTSN, sỏi OMC…)
và đánh dấu * các mã hay dùng để xếp lên đầu danh sách gợi ý.

Cách chạy (tải file JSON về một thư mục riêng trước):
  python -I tao-icd.py <CodeSystem-vn-icd10-cs.full.json> ../XepGiuong_KhoaNgoai.html
Script thay phần giữa <script id="icdData" type="text/plain"> và </script> trong file HTML.
"""
import json
import re
import sys
import unicodedata

SRC, HTML = sys.argv[1], sys.argv[2]

# Phạm vi lấy theo 3 ký tự đầu của mã
RANGES = """A01 A01;A04 A04;A06 A06;A09 A09;A18 A18;A41 A41;A46 A46;A48 A48;B15 B19;B66 B67;B76 B83;
C15 C26;C33 C34;C37 C38;C45 C45;C48 C49;C50 C50;C60 C68;C70 C72;C73 C73;C75 C75;C76 C80;
D00 D01;D09 D09;D12 D13;D17 D21;D24 D24;D29 D30;D32 D35;D37 D37;D40 D43;D48 D48;D50 D50;D62 D62;D64 D64;D73 D73;
E04 E05;E10 E11;E14 E14;E86 E87;
G06 G06;G40 G41;G56 G56;G91 G91;G93 G93;G95 G97;
I10 I10;I20 I21;I25 I26;I48 I48;I50 I50;I60 I64;I67 I67;I70 I89;
J18 J18;J44 J44;J85 J86;J90 J94;J96 J96;
K20 K93;
L00 L08;L72 L72;L89 L89;L97 L98;
M43 M43;M47 M48;M50 M51;M54 M54;M72 M72;
N10 N13;N15 N15;N17 N53;N60 N64;N83 N83;N99 N99;
Q01 Q07;Q39 Q45;Q53 Q55;Q60 Q64;
R10 R19;R22 R22;R30 R41;R50 R60;R64 R65;R68 R68;
S00 S39;S45 S45;S55 S55;S65 S65;S75 S75;S85 S85;S95 S95;
T00 T19;T79 T88;
Z08 Z09;Z43 Z43;Z46 Z46;Z48 Z48;Z93 Z93;Z96 Z96"""

# Mã không liên quan dù nằm trong phạm vi trên
DROP = set("""Z46.0 Z46.1 Z46.2 Z46.3 Z46.4 Z46.7 Z43.0 Z43.7 T83.3 T83.4 T83.6 T85.2 T85.3 T85.4
S02.2 S02.3 S02.4 S02.5 S02.6 S01.1 S01.2 S01.3 S01.4 S01.5 T18.0 T19.2 T19.3""".split())

# Mã hay dùng ở khoa: xếp đầu danh sách gợi ý
COMMON = """K35.2 K35.3 K35.8 K36 K37 K38.1 K40.0 K40.2 K40.3 K40.4 K40.9 K41.3 K41.9 K42.0 K42.9 K43.0 K43.2 K43.6 K43.9
K56.0 K56.1 K56.2 K56.5 K56.6 K56.7 K91.3 K25.0 K25.1 K25.4 K25.5 K26.0 K26.1 K26.4 K26.5 K27.1 K27.5 K92.0 K92.1 K92.2
K29.7 K29.9 K31.1 K80.0 K80.1 K80.2 K80.3 K80.4 K80.5 K81.0 K81.1 K82.2 K83.0 K83.1 K85.1 K85.2 K85.9 K86.1 K86.3
K75.0 A06.4 K74.6 K76.6 K65.0 K66.0 K66.1 K63.1 K57.2 K57.3 K59.0 K60.3 K60.1 K61.0 K61.2 K62.1 K62.3 K63.5
K64.0 K64.1 K64.2 K64.3 K64.5 K64.8 K64.9 K22.3 B77.8 B66.3
C15.9 C16.0 C16.3 C16.9 C18.0 C18.2 C18.4 C18.6 C18.7 C18.9 C19 C20 C21.0 C22.0 C22.1 C22.9 C23 C24.0 C24.1 C25.0 C25.9
C78.6 C78.7 C80.9 D12.6 D13.1 D37.4 D37.7
N20.0 N20.1 N20.2 N20.9 N21.0 N21.1 N13.0 N13.2 N13.3 N13.6 N23 N10 N11.9 N15.1 N28.1 N17.9 N18.9 N39.0 N30.0
N40 N41.0 N41.2 N43.3 N44 N45.0 N45.9 N47 N35.9 N32.0 N31.9 N48.1 I86.1 Q53.9
C61 C64 C65 C66 C67.9 C62.9 D41.4 D30.0 D30.3 R31 R33 Z96.0 Z46.6 T83.0 T83.1 T83.5
S06.0 S06.1 S06.2 S06.3 S06.4 S06.5 S06.6 S06.8 S06.9 S02.0 S02.1 S01.0 S12.9 S22.0 S32.0 S14.1 S24.1 S34.1
I60.9 I61.9 I62.0 I62.9 I63.9 I64 G91.9 G93.6 C71.9 C79.3 D32.0 D33.2 D43.2 T85.0
M51.1 M51.2 M50.1 M50.2 M48.0 M43.1 M54.4 M54.5
S36.0 S36.1 S36.4 S36.5 S36.7 S36.9 S37.0 S37.2 S37.3 S27.0 S27.1 S27.2 S22.3 S22.4 S31.1 S21.1 S39.9 T07
R10.0 R10.4 R57.1 R57.2 A41.9 E11.9 I10 R18 R17.0 R19.0 R50.9
I83.9 I87.2 I80.2 I70.2 I74.3 I71.4 J93.0 J93.1 J94.2 J90 J86.9
L02.2 L02.3 L02.4 L03.1 L03.3 L05.0 L05.9 L72.1 D17.1 D17.9 T81.0 T81.3 T81.4 Z43.3 Z93.3 Z93.2 Z09.0 Z48.0 Z08.0""".split()

# Từ khóa thêm (từ thường gõ ở khoa, chữ viết tắt). Khóa có thể là mã (K35.2) hoặc tiền tố (S06, K40).
KW = {
    'K35': 'VRT viêm ruột thừa cấp',
    'K35.2': 'viêm phúc mạc ruột thừa, vỡ ruột thừa, thủng ruột thừa, VPM',
    'K35.3': 'áp xe ruột thừa, đám quánh ruột thừa, VPM khu trú',
    'K36': 'VRT', 'K37': 'VRT',
    'K40': 'TVB', 'K42': 'TV rốn', 'K43': 'thoát vị thành bụng, thoát vị vết mổ',
    'K56.0': 'liệt ruột cơ năng',
    'K56.5': 'tắc ruột do dính, dây chằng',
    'K56.6': 'bán tắc ruột, tắc ruột do u, tắc ruột do bã thức ăn',
    'K56.7': 'bán tắc ruột',
    'K91.3': 'tắc ruột sau mổ, dính ruột sau mổ',
    'K25.1': 'thủng dạ dày, thủng ổ loét', 'K25.5': 'thủng dạ dày, thủng ổ loét',
    'K26.1': 'thủng tá tràng, thủng ổ loét', 'K26.5': 'thủng tá tràng, thủng ổ loét',
    'K27.1': 'thủng ổ loét', 'K27.5': 'thủng ổ loét',
    'K25': 'loét bao tử, LDD', 'K26': 'LTT', 'K27': 'LDDTT',
    'K92.2': 'XHTH, xuất huyết tiêu hóa trên, xuất huyết tiêu hóa dưới',
    'K92.0': 'XHTH', 'K92.1': 'XHTH, tiêu phân đen',
    'K80.3': 'sỏi ống mật chủ, sỏi OMC, sỏi đường mật, sỏi gan',
    'K80.4': 'sỏi ống mật chủ, sỏi OMC',
    'K80.5': 'sỏi ống mật chủ, sỏi OMC, sỏi đường mật, sỏi gan, sỏi trong gan',
    'K80.0': 'VTM', 'K80.1': 'VTM', 'K81': 'VTM',
    'K82.2': 'thủng túi mật, viêm phúc mạc mật',
    'K83.0': 'nhiễm trùng đường mật, viêm đường mật cấp',
    'K83.1': 'tắc mật, vàng da tắc mật, hẹp đường mật',
    'K85': 'VTC', 'K86.3': 'nang giả tụy',
    'K74.6': 'xơ gan', 'K76.6': 'TALTMC',
    'K65.0': 'VPM', 'K65.8': 'VPM', 'K65.9': 'VPM',
    'K66.0': 'dính ruột, dính phúc mạc', 'K66.1': 'máu trong ổ bụng',
    'K63.1': 'thủng ruột non, thủng đại tràng',
    'K57': 'viêm túi thừa',
    'K61.0': 'áp xe cạnh hậu môn, áp xe quanh hậu môn',
    'K64.5': 'trĩ tắc mạch, trĩ huyết khối', 'K64.8': 'trĩ hỗn hợp, trĩ nội, trĩ ngoại',
    'K62.3': 'sa trực tràng',
    'A06.4': 'áp xe gan amip', 'B66.3': 'sán lá gan lớn', 'B77.8': 'giun chui ống mật, giun đũa',
    'B77.0': 'tắc ruột do giun',
    'N13': 'ứ nước thận, thận ứ nước',
    'N13.6': 'ứ mủ thận',
    'N20': 'sỏi niệu', 'N20.1': 'sỏi NQ', 'N20.2': 'sỏi NQ',
    'N21.0': 'sỏi BQ',
    'N23': 'cơn đau quặn thận',
    'N10': 'viêm thận bể thận cấp', 'N11': 'viêm thận bể thận mạn',
    'N39.0': 'nhiễm khuẩn tiết niệu, NTT, nhiễm trùng tiểu',
    'N40': 'u xơ tuyến tiền liệt, bướu tuyến tiền liệt, tăng sản lành tính, BPH',
    'N43.3': 'tràn dịch tinh mạc, TDTM', 'N43': 'tràn dịch tinh mạc',
    'N44': 'xoắn thừng tinh', 'N45': 'viêm mào tinh',
    'N47': 'hẹp bao quy đầu, dài bao quy đầu',
    'N35': 'hẹp niệu đạo', 'N32.0': 'hẹp cổ bàng quang',
    'I86.1': 'giãn tĩnh mạch thừng tinh, varicocele',
    'Q53': 'tinh hoàn ẩn',
    'R31': 'đái máu, tiểu ra máu',
    'R33': 'bí đái',
    'Z96.0': 'sonde JJ, ống thông JJ, double J, thông niệu quản',
    'Z46.6': 'rút sonde JJ, thay sonde JJ, rút JJ, thay JJ, thay sonde dẫn lưu',
    'T83.0': 'tắc sonde tiểu, sonde Foley',
    'T83.1': 'biến chứng sonde JJ, tắc JJ',
    'T83.5': 'nhiễm trùng sonde JJ',
    'S06': 'CTSN, chấn thương sọ não',
    'S06.0': 'chấn động não',
    'S06.3': 'dập não, máu tụ trong não',
    'S06.4': 'máu tụ ngoài màng cứng, MTNMC',
    'S06.5': 'máu tụ dưới màng cứng, MTDMC',
    'S06.6': 'XHDN',
    'S02.0': 'CTSN, chấn thương sọ não, lún sọ, vỡ sọ',
    'S02.1': 'CTSN, chấn thương sọ não, vỡ nền sọ',
    'S01.0': 'vết thương da đầu, VTDĐ',
    'S12': 'CTCS, chấn thương cột sống cổ', 'S13': 'CTCS cổ', 'S14': 'CTCS, chấn thương tủy cổ',
    'S22.0': 'CTCS, chấn thương cột sống ngực', 'S22.1': 'CTCS', 'S24': 'CTCS, chấn thương tủy ngực',
    'S32.0': 'CTCS, chấn thương cột sống thắt lưng', 'S32.7': 'CTCS', 'S34': 'CTCS, chấn thương tủy thắt lưng',
    'S27': 'chấn thương ngực, CTN',
    'S27.0': 'TKMP', 'S27.1': 'TMMP', 'S27.2': 'TMMP, TKMP',
    'S22.3': 'chấn thương ngực', 'S22.4': 'chấn thương ngực',
    'S21': 'vết thương ngực, VTN',
    'S36': 'chấn thương bụng, CTB, vết thương thấu bụng',
    'S36.0': 'vỡ lách, dập lách', 'S36.1': 'vỡ gan, dập gan, rách gan', 'S36.2': 'vỡ tụy, dập tụy',
    'S36.3': 'thủng dạ dày do chấn thương', 'S36.4': 'thủng ruột non, vỡ ruột non', 'S36.5': 'thủng đại tràng, vỡ đại tràng',
    'S37': 'chấn thương bụng, chấn thương tiết niệu',
    'S37.0': 'chấn thương thận, vỡ thận, dập thận', 'S37.2': 'vỡ bàng quang', 'S37.3': 'đứt niệu đạo, chấn thương niệu đạo',
    'S31.1': 'vết thương bụng, VTB', 'S31.8': 'vết thương bụng',
    'S39.9': 'chấn thương bụng',
    'T07': 'đa chấn thương',
    'I60': 'XHDN, vỡ phình mạch não', 'I61': 'xuất huyết não, XHN, máu tụ trong não, đột quỵ', 'I62.0': 'máu tụ dưới màng cứng mạn tính',
    'I62.9': 'xuất huyết nội sọ', 'I63': 'nhồi máu não, đột quỵ', 'I67.1': 'phình mạch não',
    'G91': 'não úng thủy, giãn não thất', 'G93.6': 'phù não', 'G93.5': 'chèn ép não',
    'G06.0': 'áp xe não',
    'C71': 'u não', 'D33': 'u não', 'D43': 'u não', 'D32.0': 'u màng não', 'C79.3': 'u não di căn',
    'M51.1': 'thoát vị đĩa đệm thắt lưng, TVĐĐ, TVDD',
    'M51.2': 'thoát vị đĩa đệm, TVĐĐ, TVDD',
    'M50.1': 'thoát vị đĩa đệm cổ, TVĐĐ, TVDD', 'M50.2': 'TVĐĐ, TVDD',
    'M48.0': 'hẹp ống sống thắt lưng, hẹp ống sống cổ',
    'M43.1': 'trượt đốt sống, trượt cột sống thắt lưng',
    'M54.4': 'đau thần kinh tọa, đau thắt lưng hông', 'M54.5': 'đau lưng',
    'G56.0': 'hội chứng ống cổ tay',
    'C': 'u ác, ung thư, K',
    'C78': 'di căn', 'C79': 'di căn', 'C77': 'di căn hạch',
    'C80.9': 'ung thư không rõ nguyên phát',
    'C18': 'ung thư đại tràng, K đại tràng', 'C20': 'ung thư trực tràng', 'C16': 'ung thư dạ dày, ung thư bao tử',
    'C22.0': 'HCC, ung thư gan', 'C22.1': 'ung thư đường mật trong gan', 'C24.0': 'ung thư đường mật, u Klatskin',
    'C25': 'ung thư tụy', 'C61': 'ung thư tuyến tiền liệt', 'C67': 'ung thư bàng quang',
    'C64': 'ung thư thận', 'C15': 'ung thư thực quản',
    'D12': 'polyp đại tràng, polyp trực tràng', 'D13.1': 'polyp dạ dày, GIST',
    'D37': 'GIST, u mô đệm', 'D41.4': 'u bàng quang',
    'D30.0': 'u thận lành', 'D30.3': 'u bàng quang lành',
    'R10.0': 'bụng ngoại khoa, bụng cấp', 'R10.4': 'đau bụng',
    'R57.1': 'sốc mất máu', 'R57.2': 'sốc nhiễm khuẩn',
    'A41': 'nhiễm khuẩn huyết, nhiễm trùng huyết, NKH, sepsis',
    'R65': 'SIRS, đáp ứng viêm hệ thống',
    'R18': 'cổ trướng, báng bụng', 'R17.0': 'vàng da', 'R19.0': 'khối u bụng, u bụng',
    'R50.9': 'sốt',
    'E11.9': 'ĐTĐ, tiểu đường', 'E11': 'ĐTĐ, tiểu đường', 'E10': 'ĐTĐ, tiểu đường', 'E14': 'ĐTĐ, tiểu đường',
    'I10': 'THA, cao huyết áp',
    'J44': 'COPD, BPTNMT', 'N18': 'suy thận mạn, STM, bệnh thận mạn',
    'E86': 'mất nước',
    'I83': 'suy giãn tĩnh mạch, giãn tĩnh mạch chân', 'I87.2': 'suy giãn tĩnh mạch, suy tĩnh mạch chi dưới',
    'I80': 'huyết khối tĩnh mạch sâu, HKTMS, DVT',
    'I70.2': 'thiếu máu chi, tắc động mạch chi', 'I74': 'tắc động mạch, thuyên tắc',
    'I71': 'phình động mạch chủ',
    'J93': 'TKMP', 'J94.2': 'TMMP', 'J90': 'TDMP', 'J91': 'TDMP', 'J86': 'mủ màng phổi', 'J85': 'áp xe phổi',
    'L02': 'áp xe, nhọt', 'L03': 'viêm tấy, viêm mô tế bào',
    'L05': 'nang lông cùng cụt, xoang lông',
    'L72': 'u bã đậu, nang bã', 'D17': 'u mỡ, lipoma',
    'M72.6': 'viêm cân hoại tử', 'A48.0': 'hoại thư sinh hơi',
    'L89': 'loét tì đè, loét tỳ đè, loét cùng cụt',
    'T81.0': 'chảy máu sau mổ, tụ máu sau mổ',
    'T81.3': 'bục vết mổ, toác vết mổ, bục thành bụng',
    'T81.4': 'nhiễm trùng vết mổ, nhiễm khuẩn vết mổ, NKVM, áp xe tồn lưu',
    'T85.0': 'tắc dẫn lưu não thất, VP shunt, dẫn lưu não thất ổ bụng',
    'Z43.3': 'đóng hậu môn nhân tạo, HMNT', 'Z93.3': 'HMNT', 'Z43.2': 'đóng hậu môn nhân tạo, HMNT', 'Z93.2': 'HMNT',
    'Z09.0': 'tái khám sau mổ', 'Z48.0': 'thay băng, cắt chỉ', 'Z48.8': 'chăm sóc sau mổ',
    'Z08.0': 'theo dõi sau mổ ung thư',
    'E04': 'bướu giáp, bướu cổ', 'C73': 'ung thư tuyến giáp',
    'N60': 'u vú lành', 'N61': 'áp xe vú, viêm vú', 'C50': 'ung thư vú', 'D24': 'u vú lành, u xơ vú',
    'N83.5': 'xoắn nang buồng trứng',
    'T18': 'dị vật đường tiêu hóa, hóc xương',
}

TYPO = [('tụỵ', 'tuỵ'), ('huyêt ', 'huyết ')]


def nfc(s):
    return unicodedata.normalize('NFC', s)


def walk(cs, out):
    for x in cs:
        out.append(x)
        walk(x.get('concept', []), out)
    return out


def prop(x, k):
    for p in x.get('property', []):
        if p['code'] == k:
            return p.get('valueBoolean', p.get('valueString', p.get('valueInteger')))
    return None


rng = [x.split() for x in re.split(r'[;\n]+', RANGES) if x.strip()]


def in_range(code):
    c3 = code[:3]
    return any(a[0] == c3[0] and a <= c3 <= b for a, b in rng)


d = json.load(open(SRC, encoding='utf-8'))
rows = []
for x in walk(d['concept'], []):
    c = x['code']
    if not re.match(r'^[A-Z]\d\d(\.\d)?$', c):      # bỏ mã 5 ký tự (vd S06.00), dùng mã 4 ký tự
        continue
    if prop(x, 'inactive') or not prop(x, 'leaf') or not in_range(c) or c in DROP:
        continue
    n = nfc(x['display'].strip())
    n = re.sub(r'\s*\(([A-Z]\d\d(\.[\d-]+)?[*†]?[-–, ]*)+\)', '', n)   # bỏ mã tham chiếu kiểu (G99.2*)
    n = n.replace('†', '').replace('*', '').replace('|', '/').strip()
    for a, b in TYPO:
        n = n.replace(a, b)
    rows.append((c, n))

# mã 4 ký tự có trong danh mục nhưng không có mã 3 ký tự cha là lá: giữ nguyên thứ tự của danh mục
codes = set(c for c, _ in rows)
missing = [c for c in COMMON if c not in codes]
if missing:
    print('Mã hay dùng không có trong danh mục:', missing)
for k in KW:
    if k != 'C' and not any(c == k or c.startswith(k) for c in codes):
        print('Từ khóa không khớp mã nào:', k)


def kw_of(c):
    ks = [KW[k] for k in sorted(KW, key=len) if c == k or (len(k) < len(c) and c.startswith(k) and (len(k) == 1 or len(k) == 3))]
    if c[:3] in ('K40', 'K41', 'K42', 'K43', 'K44', 'K45', 'K46'):
        n = names[c]
        if re.search(r'(kèm|có) (tắc nghẽn|hoại thư)', n):
            ks.append('thoát vị nghẹt, thoát vị kẹt')
    return ', '.join(nfc(k) for k in ks)


names = dict(rows)


lines = []
common = set(COMMON)
for c, n in rows:
    k = kw_of(c)
    lines.append(('*' if c in common else '') + c + '|' + n + ('|' + k if k else ''))
data = '\n'.join(lines)

h = open(HTML, encoding='utf-8').read()
m = re.search(r'(<script id="icdData" type="text/plain">)(.*?)(</script>)', h, re.S)
assert m, 'Chưa có khối <script id="icdData" type="text/plain"></script> trong file HTML'
h = h[:m.start(2)] + '\n' + data + '\n' + h[m.end(2):]
open(HTML, 'w', encoding='utf-8', newline='\n').write(h)
print('Đã ghi', len(lines), 'mã,', len(data.encode('utf-8')), 'byte;', sum(1 for l in lines if l[0] == '*'), 'mã hay dùng')

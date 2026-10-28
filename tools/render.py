"""@drop.the.food 캐러셀 렌더러 v2 (컬러 팝 + 인포그래픽)
usage: python3 render.py <issue_dir>/slides.json   -> slide_XX.png (1080x1350)
"""
import json, sys, html, base64, math
import illust
from pathlib import Path
from playwright.sync_api import sync_playwright

INK = "#16131A"
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{font-family:'Noto Sans CJK KR',sans-serif;color:#16131A;-webkit-font-smoothing:antialiased;
 word-break:keep-all;position:relative;overflow:hidden}
.frame{position:absolute;inset:52px 60px 48px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center}
.logo{background:#16131A;color:#fff;font-weight:900;font-size:22px;letter-spacing:.16em;padding:10px 20px;border-radius:999px}
.tagrow{display:flex;gap:10px;align-items:center;font-size:22px;font-weight:700}
.tag{background:#fff;border:3px solid #16131A;border-radius:999px;padding:6px 16px}
.tag.dark{background:#16131A;color:#fff}
.bottom{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:19px;opacity:.75}
.page{font-weight:900;font-size:22px;opacity:1}
.box{background:#fff;border:3.5px solid #16131A;border-radius:28px;box-shadow:8px 8px 0 #16131A}
.q{font-weight:900;letter-spacing:-.04em;line-height:1.12}
/* cover */
.c-kicker{display:inline-block;margin-top:56px;background:#16131A;color:#FFD43B;font-weight:900;font-size:30px;padding:10px 22px;border-radius:12px;transform:rotate(-2deg);align-self:flex-start}
.c-title{font-size:118px;margin-top:30px}
.c-title em{font-style:normal;background:#fff;padding:0 14px;border-radius:16px;box-shadow:6px 6px 0 #16131A;border:3.5px solid #16131A;display:inline-block;line-height:1.05;margin:6px 0}
.c-sub{font-size:32px;font-weight:700;margin-top:26px;line-height:1.45}
.c-img{position:absolute;right:-20px;bottom:70px;width:540px;height:540px;border-radius:50%;overflow:hidden;border:5px solid #16131A;box-shadow:12px 12px 0 #16131A}
.c-img img{width:100%;height:100%;object-fit:cover}
.c-list{position:absolute;left:0;bottom:110px;display:flex;flex-direction:column;gap:12px}
.c-list div{background:#fff;border:3px solid #16131A;border-radius:14px;padding:8px 18px;font-size:26px;font-weight:800;box-shadow:4px 4px 0 #16131A;align-self:flex-start}
.c-list b{color:#FF4D2E;margin-right:10px}
.swipe{position:absolute;right:0;bottom:46px;font-weight:900;font-size:24px}
/* product */
.p-q{font-size:60px;margin-top:32px}
.mid{display:flex;gap:28px;margin-top:28px;height:420px}
.p-img{width:420px;height:420px;border-radius:32px;overflow:hidden;border:3.5px solid #16131A;box-shadow:8px 8px 0 #16131A;position:relative;flex:0 0 auto}
.p-img img{width:100%;height:100%;object-fit:cover}
.p-img .ai{position:absolute;left:14px;bottom:14px;background:rgba(22,19,26,.75);color:#fff;font-size:16px;padding:4px 10px;border-radius:8px}
.side{flex:1;display:flex;flex-direction:column;gap:18px;min-width:0}
.namebox{padding:22px 24px}
.namebox .store{font-size:22px;font-weight:900;letter-spacing:.06em}
.namebox .nm{font-size:38px;font-weight:900;line-height:1.2;letter-spacing:-.03em;margin-top:6px}
.sticker{position:absolute;top:-26px;right:-22px;width:168px;height:168px;border-radius:50%;background:#FF4D2E;color:#fff;
 border:3.5px solid #16131A;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(10deg);
 font-weight:900;box-shadow:5px 5px 0 #16131A;z-index:3}
.sticker .s1{font-size:18px;opacity:.9}.sticker .s2{font-size:40px;letter-spacing:-.04em;line-height:1.05}
.sticker.small .s2{font-size:28px}
.chips{display:flex;flex-direction:column;gap:12px}
.chip{display:flex;align-items:center;gap:14px;background:#fff;border:3px solid #16131A;border-radius:18px;padding:12px 16px;font-size:25px;font-weight:700;line-height:1.3}
.dot{flex:0 0 34px;height:34px;border-radius:50%;border:3px solid #16131A;display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:900}
.scale{margin-top:28px;padding:18px 30px 10px}
.scale h4{font-size:22px;font-weight:900;letter-spacing:.04em;display:flex;justify-content:space-between}
.scale h4 span{font-weight:700;opacity:.6;letter-spacing:0}
.note{margin-top:20px;display:flex;gap:18px;align-items:flex-start;background:#16131A;color:#fff;border-radius:22px;padding:22px 26px;font-size:28px;line-height:1.45;font-weight:600}
.note .lb{flex:0 0 auto;background:#FFD43B;color:#16131A;font-weight:900;font-size:22px;padding:4px 12px;border-radius:8px;margin-top:4px}
.clip{margin-top:22px;display:flex;gap:16px;align-items:center;background:#FFFDF7;border:3px dashed #16131A;border-radius:14px;padding:14px 20px;transform:rotate(-.6deg)}
.clip .ty{flex:0 0 auto;font-size:20px;font-weight:900;padding:4px 12px;border-radius:8px;color:#fff;background:#16131A}
.clip .ty.off{background:#6C63FF}
.clip .ou{flex:0 0 auto;font-size:22px;font-weight:900}
.clip .tx{font-size:24px;font-weight:600;line-height:1.35;min-width:0}
.p-img .ph{position:absolute;left:14px;bottom:14px;background:rgba(22,19,26,.75);color:#fff;font-size:16px;padding:4px 10px;border-radius:8px}
/* insight */
.i-q{font-size:78px;margin-top:40px;color:#fff}
.i-q em{font-style:normal;color:#FFD43B}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:48px}
.card{background:#fff;border:3.5px solid #16131A;border-radius:28px;padding:22px 24px;box-shadow:8px 8px 0 #FFD43B}
.card h5{font-size:22px;font-weight:900;letter-spacing:.02em}
.card .cap{font-size:19px;opacity:.65;margin-top:4px;line-height:1.35}
.wide{grid-column:1/3}
.cta{margin-top:44px;background:#FFD43B;border:3.5px solid #16131A;border-radius:24px;padding:22px 28px;font-size:34px;font-weight:900;letter-spacing:-.02em;display:flex;justify-content:space-between;align-items:center}
.dk .bottom{color:#fff}.dk .logo{background:#FFD43B;color:#16131A}
.cta small{font-size:22px;font-weight:700}
"""

def esc(s): return html.escape(str(s))

def visual(s):
    # 1순위: 사진(img = 회차 폴더 안 파일, img_url에서 받아 둔 것 포함)
    if s.get("img") and Path(s["img"]).exists():
        if s.get("img_credit"):
            # 기업 공식 배포 사진: 네모칸을 꽉 채우고, img_pos(초점 위치)·img_zoom(확대)으로 제품 쪽을 클로즈업해요
            pos = s.get("img_pos", "50% 50%")
            zoom = float(s.get("img_zoom", 1))
            return (f'<img src="{img_uri(s["img"])}" style="object-fit:cover;object-position:{pos};'
                    f'transform:scale({zoom});transform-origin:{pos}">'
                    f'<div class="ph">{esc(s["img_credit"])}</div>')
        label = s.get("img_label") or ("AI 연출 이미지 · 실제 제품과 달라요" if s.get("img_url") else "직접 촬영")
        return f'<img src="{img_uri(s["img"])}"><div class="ph">{esc(label)}</div>'
    # 2순위: illus_svg(회차별 새 일러스트), 3순위: illus 키
    if s.get("illus_svg"):
        svg = s["illus_svg"].strip()
        return svg if svg.startswith("<svg") else illust._wrap(svg, s.get("illus_bg"))
    name = s.get("illus") if s.get("illus") in illust.LIB else "basket"
    return illust.get(name, s.get("illus_bg"))

def fetch_images(slides, out):
    """사진 받기. 우선순위: img_url(기업 공식 배포 사진이면 img_credit 함께) → ai_img_url(AI 연출 사진) → 일러스트.
    받은 파일은 <회차>/src/img_NN-press.* 또는 img_NN-ai.*로 저장해요(캐러셀 JPG와 섞이지 않게 하위 폴더)."""
    import urllib.request
    from urllib.parse import urlsplit
    src = out / "src"
    for i, s in enumerate(slides, 1):
        cands = []
        if s.get("img_url"):
            cands.append(("press" if s.get("img_credit") else "ai", s["img_url"]))
        if s.get("ai_img_url"):
            cands.append(("ai", s["ai_img_url"]))
        if not cands:
            continue
        done = False
        for kind, url in cands:
            have = sorted(src.glob(f"img_{i:02d}-{kind}.*")) if src.exists() else []
            if have:
                f = have[0]
            else:
                try:
                    ref = s.get("img_referer") or "{0.scheme}://{0.netloc}/".format(urlsplit(url))
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Referer": ref})
                    data = urllib.request.urlopen(req, timeout=40).read()
                    if len(data) < 2000:
                        raise ValueError("too small")
                    ext = ".png" if data[:4] == b"\x89PNG" else (".webp" if data[8:12] == b"WEBP" else ".jpg")
                    src.mkdir(exist_ok=True)
                    f = src / f"img_{i:02d}-{kind}{ext}"
                    f.write_bytes(data)
                    print(f"사진 받음: {i:02d}장 {kind} ({len(data)//1024}KB)")
                except Exception as e:
                    print(f"사진 못 받음: {i:02d}장 {kind} ({e.__class__.__name__})")
                    continue
            s["img"] = str(f)
            if kind == "ai":
                s.pop("img_credit", None)
                s["img_url"] = url  # AI 라벨이 붙도록
            done = True
            break
        if not done:
            print(f"{i:02d}장은 일러스트로 대신해요")

def img_uri(path):
    if not path: return ""
    p = Path(path)
    if not p.exists(): return ""
    mime = {".png": "image/png", ".webp": "image/webp"}.get(p.suffix.lower(), "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

def shell(inner, s, page, total, issue, overlay=""):
    tags = "".join(f'<span class="tag{" dark" if i==0 else ""}">{esc(t)}</span>' for i, t in enumerate(s.get("tags", [issue])))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body class="{'dk' if s['kind']=='insight' else ''}" style="background:{s.get('bg','#FFD43B')}">{overlay}<div class="frame">
<div class="top"><div class="logo">DROP THE FOOD</div><div class="tagrow">{tags}</div></div>
{inner}
<div class="bottom"><div>{esc(s.get('src',''))}</div><div class="page">{page:02d} / {total:02d}</div></div>
</div></body></html>"""

# ---------- infographic pieces ----------
def price_scale(items, hi_idx, maxv=6000, color="#FF4D2E"):
    """items: [{label, lo, hi}] ; renders a horizontal price ruler with all items, highlights one"""
    W, H, x0, x1, y = 960, 150, 30, 930, 70
    def X(v): return x0 + (x1 - x0) * v / maxv
    g = [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>']
    step = max(1000, round(maxv / 6 / 1000) * 1000)
    for t in range(0, maxv + 1, step):
        lab = "0" if t == 0 else (f"{t/10000:g}만" if t >= 10000 else f"{t//1000}천")
        g.append(f'<line x1="{X(t)}" y1="{y-10}" x2="{X(t)}" y2="{y+10}" stroke="{INK}" stroke-width="3"/>')
        g.append(f'<text x="{X(t)}" y="{y+40}" font-size="19" text-anchor="middle" fill="{INK}" opacity=".55" font-weight="700">{lab}</text>')
    # low-price zone
    g.append(f'<rect x="{x0}" y="{y-26}" width="{X(1000)-x0}" height="52" rx="10" fill="#4DA8FF" opacity=".22"/>')
    for i, it in enumerate(items):
        hl = i == hi_idx
        c = color if hl else "#BDB6C6"
        r = 17 if hl else 11
        if it["hi"] != it["lo"]:
            g.append(f'<line x1="{X(it["lo"])}" y1="{y}" x2="{X(it["hi"])}" y2="{y}" stroke="{c}" stroke-width="{14 if hl else 9}" stroke-linecap="round"/>')
            cx = X((it["lo"] + it["hi"]) / 2)
        else:
            cx = X(it["lo"])
            g.append(f'<circle cx="{cx}" cy="{y}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="3"/>')
        if hl:
            lab = esc(it["label"])
            g.append(f'<g transform="translate({cx},{y-34})"><rect x="-70" y="-30" width="140" height="38" rx="10" fill="{INK}"/>'
                     f'<text y="-4" font-size="21" font-weight="900" fill="#fff" text-anchor="middle">{lab}</text></g>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" height="{H}">{"".join(g)}</svg>'

def gauge(value, prev, lo=0, hi=200, base=100, prev_label="이전"):
    cx, cy, R = 200, 190, 150
    def pt(v, r=R):
        a = math.pi * (1 - (v - lo) / (hi - lo))
        return cx + r * math.cos(a), cy - r * math.sin(a)
    def arc(v0, v1, col, w):
        x0, y0 = pt(v0); x1, y1 = pt(v1)
        return f'<path d="M{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="butt"/>'
    g = [arc(lo, base, "#FF4D2E", 34), arc(base, hi, "#5CD6A9", 34)]
    bx, by = pt(base, R + 30); g.append(f'<text x="{bx:.0f}" y="{by:.0f}" font-size="18" text-anchor="middle" font-weight="700" fill="{INK}" opacity=".6">기준 {base}</text>')
    px, py = pt(prev, R - 40)
    g.append(f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{INK}" stroke-width="5" stroke-dasharray="6 6" opacity=".35"/>')
    qx, qy = pt(prev, R + 34)
    g.append(f'<text x="{qx:.0f}" y="{qy:.0f}" font-size="19" font-weight="800" text-anchor="middle" fill="{INK}" opacity=".55">{esc(prev_label)} {prev}</text>')
    nx, ny = pt(value, R - 30)
    g.append(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{INK}"/>')
    g.append(f'<text x="{cx}" y="{cy+62}" font-size="56" font-weight="900" text-anchor="middle" fill="#FF4D2E">{value}</text>')
    return f'<svg viewBox="0 -44 400 314" width="100%" height="270">{"".join(g)}</svg>'

def bars(rows, maxv, wide=False, prefix=""):
    W, rowh = (880, 74) if wide else (400, 74)
    full = W - 20
    g = []
    for i, (lab, v, col) in enumerate(rows):
        y = 18 + i * rowh
        w = full * v / maxv
        g.append(f'<text x="0" y="{y}" font-size="20" font-weight="800" fill="{INK}">{esc(lab)}</text>')
        g.append(f'<rect x="0" y="{y+10}" width="{full}" height="34" rx="10" fill="#EEE9F3"/>')
        g.append(f'<rect x="0" y="{y+10}" width="{w:.0f}" height="34" rx="10" fill="{col}" stroke="{INK}" stroke-width="3"/>')
        g.append(f'<text x="{min(w+12,full-70):.0f}" y="{y+36}" font-size="24" font-weight="900" fill="{INK}">{esc(prefix)}{v}%</text>')
    return f'<svg viewBox="0 0 {W} {18+len(rows)*rowh}" width="100%" height="{18+len(rows)*rowh}">{"".join(g)}</svg>'

def split_map(items, color_hi="#FF4D2E", color_lo="#4DA8FF", maxv=6000):
    """두 갈래 소비 지도: 1천원 이하 vs 3천원 이상"""
    W, H, x0, x1, y = 920, 170, 20, 900, 92
    def X(v): return x0 + (x1 - x0) * v / maxv
    g = [f'<rect x="{x0}" y="{y-40}" width="{X(1000)-x0:.0f}" height="80" rx="16" fill="{color_lo}" opacity=".25"/>',
         f'<rect x="{X(3500):.0f}" y="{y-40}" width="{x1-X(3500):.0f}" height="80" rx="16" fill="{color_hi}" opacity=".2"/>',
         f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{INK}" stroke-width="4"/>',
         f'<text x="{x0+8}" y="{y-52}" font-size="21" font-weight="900" fill="{color_lo}">습관 소비 · 1천 원 이하</text>',
         f'<text x="{x1-8}" y="{y-52}" font-size="21" font-weight="900" fill="{color_hi}" text-anchor="end">이유 있는 소비 · 3.5천 원 이상</text>']
    # 같은 가격은 '·'로 합치고, 가까운 라벨은 두 줄로 엇갈리게 놓아요
    pts = []
    for it in sorted(items, key=lambda i: (i["lo"] + i["hi"]) / 2):
        cx = X((it["lo"] + it["hi"]) / 2)
        col = color_lo if it["hi"] <= 1000 else (color_hi if it["lo"] >= 3500 else "#B69CFF")
        if pts and abs(pts[-1][0] - cx) < 4:
            pts[-1][2].append(it["short"])
        else:
            pts.append([cx, col, [it["short"]]])
    last = [-1e9, -1e9]
    for cx, col, names in pts:
        label = "·".join(names)
        half = len(label) * 9 + 8
        row = 0 if cx - half > last[0] else (1 if cx - half > last[1] else 0)
        last[row] = cx + half
        ly = y + 44 + row * 30
        if row:
            g.append(f'<line x1="{cx:.0f}" y1="{y+16}" x2="{cx:.0f}" y2="{ly-18}" stroke="{INK}" stroke-width="2" opacity=".4"/>')
        g.append(f'<circle cx="{cx:.0f}" cy="{y}" r="15" fill="{col}" stroke="{INK}" stroke-width="3"/>')
        g.append(f'<text x="{cx:.0f}" y="{ly}" font-size="18" font-weight="800" text-anchor="middle" fill="{INK}">{esc(label)}</text>')
    return f'<svg viewBox="0 0 {W} {H+28}" width="100%" height="{H+28}">{"".join(g)}</svg>'

# ---------- slide kinds ----------
def cover(s, spec):
    lst = "".join(f'<div><b>{i+1:02d}</b>{esc(t)}</div>' for i, t in enumerate(s.get("list", [])))
    inner = f"""<div class="c-kicker">{esc(s['kicker'])}</div>
<div class="q c-title">{s['title']}</div>
<div class="c-sub">{esc(s['sub'])}</div>
<div style="position:relative;flex:1">
 <div class="c-img">{visual(s)}</div>
 <div class="c-list">{lst}</div>
 <div class="swipe">넘겨보기 →</div>
</div>"""
    return inner

def clip(s):
    c = s.get("clip")
    if not c: return ""
    off = " off" if c["type"] != "기사" else ""
    return f'<div class="clip"><span class="ty{off}">{esc(c["type"])}</span><span class="ou">{esc(c["outlet"])} · {esc(c["date"])}</span><span class="tx">{esc(c["text"])}</span></div>'

def product(s, spec):
    items = spec["price_items"]
    chips = "".join(f'<div class="chip"><div class="dot" style="background:{c}">{i+1}</div><div>{esc(t)}</div></div>'
                    for i, (t, c) in enumerate(zip(s["chips"], ["#FFD43B", "#5CD6A9", "#B69CFF", "#4DA8FF"])))
    small = " small" if len(s["price_tag"]) > 6 else ""
    return f"""<div class="q p-q">{s['q']}</div>
<div class="mid">
 <div class="p-img">{visual(s)}</div>
 <div class="side" style="position:relative">
  <div class="sticker{small}"><div class="s1">{esc(s.get('price_label','가격'))}</div><div class="s2">{esc(s['price_tag'])}</div></div>
  <div class="box namebox"><div class="store">{esc(s['store'])} · {esc(s['date'])}</div><div class="nm" style="padding-right:110px">{esc(s['name'])}</div></div>
  <div class="chips">{chips}</div>
 </div>
</div>
<div class="box scale"><h4>{esc(spec.get("scale_title","이번 주 신상 가격 지도"))} <span>파란 구간 = 1천 원 이하</span></h4>{price_scale(items, s['price_idx'], maxv=spec.get('scale_max',6000), color=s.get('accent','#FF4D2E'))}</div>
{clip(s)}
<div class="note"><span class="lb">관찰</span><div>{esc(s['note'])}</div></div>"""

def insight(s, spec):
    """관찰 노트. 회차마다 바뀌는 문구는 slides.json에서 받는다.
    gauge: {value, prev, prev_label?, title, cap, lo?, hi?, base?}  (생략 가능)
    bars:  {title, cap, max, rows:[[label, value, color], ...]}      (생략 가능)
    map_title: 가격 분포 지도 제목"""
    cards = []
    g = s.get("gauge")
    if g:
        cards.append(f'<div class="card"><h5>{esc(g.get("title",""))}</h5><div class="cap">{esc(g.get("cap",""))}</div>'
                     f'{gauge(g["value"], g["prev"], g.get("lo",0), g.get("hi",200), g.get("base",100), g.get("prev_label","이전"))}</div>')
    b = s.get("bars")
    if b:
        if isinstance(b, list): b = {"title": "", "cap": "", "max": 20, "rows": b}
        cards.append(f'<div class="card"><h5>{esc(b.get("title",""))}</h5><div class="cap">{esc(b.get("cap",""))}</div>'
                     f'<div style="margin-top:22px">{bars([tuple(r) for r in b["rows"]], b.get("max", max(r[1] for r in b["rows"])*1.15), wide=not g, prefix=b.get("prefix",""))}</div></div>')
    wide = ' wide' if len(cards) != 1 else ''
    cards.append(f'<div class="card wide"><h5>{esc(s.get("map_title","이번 회차 아이템, 어디에 찍혔을까요?"))}</h5>'
                 f'{split_map(spec["price_items"], maxv=spec.get("scale_max",6000))}</div>')
    if len(cards) == 2:  # gauge나 bars 하나만 있으면 넓게
        cards[0] = cards[0].replace('class="card"', 'class="card wide"', 1)
    return f"""<div class="q i-q">{s['title']}</div>
<div class="grid">{''.join(cards)}</div>
<div class="cta"><div>{esc(s['cta'])}</div><small>댓글로 알려주세요 ↓</small></div>"""

KINDS = {"cover": cover, "product": product, "insight": insight}

def main(spec_path):
    spec_path = Path(spec_path)
    spec = json.loads(spec_path.read_text())
    out = spec_path.parent
    slides = spec["slides"]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for s in slides:
            if s.get("img") and not s.get("img_url"): s["img"] = str(out / s["img"])
        fetch_images(slides, out)
        for i, s in enumerate(slides, 1):
            pg.set_content(shell(KINDS[s["kind"]](s, spec), s, i, len(slides), spec["issue"]))
            pg.wait_for_timeout(200)
            pg.screenshot(path=str(out / f"slide_{i:02d}.png"))
        b.close()
    print("rendered", len(slides))

if __name__ == "__main__":
    main(sys.argv[1])

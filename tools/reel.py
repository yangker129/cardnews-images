"""@drop.the.food 릴스·스토리 생성기
usage: python3 reel.py <회차폴더>          (slides.json, slide_01~07.png가 있는 폴더)
out  : reel.mp4 (1080x1920, H.264, 30fps, 무음 AAC 트랙 포함), reel_cover.jpg, story.jpg
       선택: <회차폴더>/bgm.mp3 (또는 저장소 assets/bgm.mp3 경로를 BGM 환경변수로) 가 있으면 배경음으로 깔고 페이드아웃
"""
import json, os, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
INK = (22, 19, 26)
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
FONT_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def font(size, bold=False):
    for f in ([FONT_B] if bold else [FONT]) + [FONT, FONT_B]:
        if Path(f).exists():
            return ImageFont.truetype(f, size, index=1)  # index 1 = KR
    return ImageFont.load_default()


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def pill(draw, xy, text, fnt, fill, color, pad=(26, 12), radius=999, outline=None):
    x, y = xy
    tw = draw.textlength(text, font=fnt)
    asc, desc = fnt.getmetrics()
    box = [x, y, x + tw + pad[0] * 2, y + asc + desc + pad[1] * 2]
    draw.rounded_rectangle(box, radius=min(radius, (box[3] - box[1]) // 2), fill=fill,
                           outline=outline, width=4 if outline else 0)
    draw.text((x + pad[0], y + pad[1]), text, font=fnt, fill=color)
    return box


def card_with_shadow(card, scale):
    cw, ch = int(card.width * scale), int(card.height * scale)
    c = card.resize((cw, ch), Image.LANCZOS)
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw, ch], radius=36, fill=255)
    layer = Image.new("RGBA", (cw + 16, ch + 16), (0, 0, 0, 0))
    sh = Image.new("RGBA", (cw, ch), INK + (255,))
    layer.paste(sh, (14, 14), mask)
    layer.paste(c, (0, 0), mask)
    border = ImageDraw.Draw(layer)
    border.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=36, outline=INK, width=6)
    return layer


def frame(card, bg, idx, total, issue, top_text, bottom_text):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    # 배경 도트 패턴
    dot = tuple(max(0, c - 18) for c in bg)
    for yy in range(40, H, 64):
        for xx in range(40 + (yy // 64 % 2) * 32, W, 64):
            d.ellipse([xx - 5, yy - 5, xx + 5, yy + 5], fill=dot)
    # 상단
    pill(d, (60, 120), "DROP THE FOOD", font(34), INK, (255, 255, 255))
    f = font(30, True)
    tw = d.textlength(issue, font=f)
    pill(d, (W - 60 - tw - 52, 120), issue, f, (255, 255, 255), INK, outline=INK)
    tf = font(58)
    d.text((60, 230), top_text, font=tf, fill=INK)
    # 카드
    layer = card_with_shadow(card, 0.84)
    x = (W - layer.width) // 2
    y = 330
    im.paste(layer, (x, y), layer)
    # 하단 진행 바
    by = y + layer.height + 46
    seg = (W - 120 - (total - 1) * 12) / total
    for i in range(total):
        x0 = 60 + i * (seg + 12)
        d.rounded_rectangle([x0, by, x0 + seg, by + 14], radius=7,
                            fill=INK if i <= idx else tuple(max(0, c - 40) for c in bg))
    bf = font(40, True)
    btw = d.textlength(bottom_text, font=bf)
    d.text(((W - btw) / 2, by + 40), bottom_text, font=bf, fill=INK)
    return im


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", " ", s).replace("  ", " ").strip()


def build(folder):
    folder = Path(folder)
    spec = json.loads((folder / "slides.json").read_text())
    slides = spec["slides"]
    issue = spec["issue"].split("·")[0].strip()
    total = len(slides)
    tmp = Path(tempfile.mkdtemp())
    frames, durs = [], []
    for i, s in enumerate(slides, 1):
        card = Image.open(folder / f"slide_{i:02d}.png").convert("RGB")
        bg = hex2rgb(s.get("bg", "#FFD43B"))
        if s["kind"] == "insight":
            bg = (255, 212, 59)
        if s["kind"] == "cover":
            top, bottom, dur = "이번 회차 질문 ↓", "끝까지 보면 답이 보여요", 3.2
        elif s["kind"] == "product":
            top = f"{i-1:02d}  {s.get('store','')} · {s.get('price_tag','')}"
            bottom, dur = "전체 내용은 게시물에서 →", 2.3
        else:
            top, bottom, dur = "그래서, 결론은요", "당신의 지갑은 어느 쪽인가요? 댓글로!", 3.6
        p = tmp / f"f{i:02d}.png"
        frame(card, bg, i - 1, total, issue, top, bottom).save(p)
        frames.append(p); durs.append(dur)

    # ffmpeg: 각 장면 살짝 줌인 → xfade 슬라이드 전환
    fps, tr = 30, 0.35
    inputs, filters = [], []
    for i, (p, dur) in enumerate(zip(frames, durs)):
        inputs += ["-loop", "1", "-t", f"{dur + tr:.2f}", "-i", str(p)]
        n = int((dur + tr) * fps)
        filters.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0009*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                       f":d={n}:s={W}x{H}:fps={fps},setsar=1,format=yuv420p[v{i}]")
    last, off = "v0", 0.0
    for i in range(1, len(frames)):
        off += durs[i - 1]
        trans = "slideleft" if i < len(frames) - 1 else "fade"
        filters.append(f"[{last}][v{i}]xfade=transition={trans}:duration={tr}:offset={off:.2f}[x{i}]")
        last = f"x{i}"
    total_dur = sum(durs) + tr
    bgm = folder / "bgm.mp3"
    if not bgm.exists() and os.environ.get("BGM"):
        bgm = Path(os.environ["BGM"])
    if bgm.exists():
        inputs += ["-i", str(bgm)]
        st = float(os.environ.get("BGM_START", "0"))
        filters.append(f"[{len(frames)}:a]atrim={st:.2f}:{st+total_dur:.2f},asetpts=PTS-STARTPTS,"
                       f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,"
                       f"afade=t=in:st=0:d=0.3,afade=t=out:st={total_dur-1.2:.2f}:d=1.2[a]")
    else:
        inputs += ["-f", "lavfi", "-t", f"{total_dur:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
        filters.append(f"[{len(frames)}:a]anull[a]")
    out = folder / "reel.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters),
           "-map", f"[{last}]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(fps), "-c:a", "aac", "-b:a", "128k",
           "-movflags", "+faststart", "-t", f"{total_dur:.2f}", str(out)]
    subprocess.run(cmd, check=True)
    Image.open(frames[0]).convert("RGB").save(folder / "reel_cover.jpg", quality=92)

    # 스토리: 표지 카드 + 새 게시물 안내
    cover = Image.open(folder / "slide_01.png").convert("RGB")
    st = Image.new("RGB", (W, H), (255, 212, 59))
    d = ImageDraw.Draw(st)
    for yy in range(40, H, 64):
        for xx in range(40 + (yy // 64 % 2) * 32, W, 64):
            d.ellipse([xx - 5, yy - 5, xx + 5, yy + 5], fill=(237, 194, 41))
    pill(d, (60, 150), "NEW POST", font(64), (255, 77, 46), (255, 255, 255), pad=(40, 16), outline=INK)
    d.text((60, 300), "새 카드뉴스가 올라왔어요", font=font(64), fill=INK)
    layer = card_with_shadow(cover, 0.82)
    lx, ly = (W - layer.width) // 2, 440
    st = st.convert("RGBA"); st.alpha_composite(layer, (lx, ly)); st = st.convert("RGB")
    d = ImageDraw.Draw(st)
    pill(d, (60, ly + layer.height + 60), "프로필에서 7장 전체 보기 →", font(48, True), INK, (255, 255, 255), pad=(36, 18))
    st.save(folder / "story.jpg", quality=92)

    # 스토리 영상: 같은 이미지에 살짝 줌인 + 배경음 (배경음이 없으면 영상은 만들지 않고 이미지 스토리로 올려요)
    if bgm.exists():
        sdur = float(os.environ.get("STORY_SECONDS", "12"))
        n = int(sdur * fps)
        sst = float(os.environ.get("BGM_START", "0"))
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", f"{sdur:.2f}", "-i", str(folder / "story.jpg"),
               "-i", str(bgm), "-filter_complex",
               f"[0:v]scale=1188:2112,zoompan=z='min(1+0.0006*on,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
               f":d={n}:s={W}x{H}:fps={fps},setsar=1,format=yuv420p[v];"
               f"[1:a]atrim={sst:.2f}:{sst+sdur:.2f},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,"
               f"afade=t=in:st=0:d=0.3,afade=t=out:st={sdur-1.2:.2f}:d=1.2[a]",
               "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-profile:v", "high",
               "-pix_fmt", "yuv420p", "-r", str(fps), "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
               "-t", f"{sdur:.2f}", str(folder / "story.mp4")]
        subprocess.run(cmd, check=True)
    print(f"reel.mp4 {total_dur:.1f}s, reel_cover.jpg, story.jpg" + (", story.mp4" if bgm.exists() else ""))


if __name__ == "__main__":
    build(sys.argv[1])

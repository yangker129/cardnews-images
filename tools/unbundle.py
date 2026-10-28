"""Make가 보낸 회차 묶음(repository_dispatch client_payload)을 posts/<날짜>/ 파일로 풀어요.
payload: {"date": "2026-10-28", "slides": {...slides.json...}, "caption": "...", "reel_caption": "..."}
취소:    {"date": "2026-10-28", "action": "cancel"}  → posted.txt에 canceled를 써서 9시 게시를 막아요
출력: GITHUB_OUTPUT에 folder, mode(render|cancel)"""
import json, os, re, sys
from pathlib import Path

event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
p = event.get("client_payload") or {}
date = str(p.get("date", "")).strip()
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}|test-[A-Za-z0-9-]{1,40}", date):
    sys.exit(f"오류: date 형식이 이상해요 ({date!r})")
def out(**kv):
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as o:
            for k, v in kv.items():
                o.write(f"{k}={v}\n")

folder = Path("posts") / date
if p.get("action") == "cancel":
    if (folder / "posted.txt").exists() and (folder / "posted.txt").read_text().strip() != "canceled":
        sys.exit(f"오류: {folder}는 이미 게시돼서 취소할 수 없어요")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "posted.txt").write_text("canceled\n")
    print(f"{folder} 취소 표시 완료")
    out(folder=folder, mode="cancel")
    sys.exit(0)

slides = p.get("slides")
if isinstance(slides, str):
    slides = json.loads(slides)
if not isinstance(slides, dict) or not slides.get("slides"):
    sys.exit("오류: slides가 비어 있어요")

if (folder / "posted.txt").exists() and (folder / "posted.txt").read_text().strip() != "canceled":
    sys.exit(f"오류: {folder}는 이미 게시된 회차라서 덮어쓰지 않아요")
folder.mkdir(parents=True, exist_ok=True)
# 이전 렌더 결과 정리 (장 수가 바뀌어도 남는 파일이 없게)
for f in list(folder.glob("[0-9][0-9].jpg")) + [folder / n for n in ("reel.mp4", "reel_cover.jpg", "story.jpg", "story.mp4", "render_done.txt")]:
    if f.exists():
        f.unlink()
# 사진은 새로 받도록 지워요 (img_url이 바뀌었을 수 있어요)
import shutil
shutil.rmtree(folder / "src", ignore_errors=True)
(folder / "slides.json").write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding="utf-8")
(folder / "caption.txt").write_text(str(p.get("caption", "")).strip() + "\n", encoding="utf-8")
if p.get("reel_caption"):
    (folder / "reel_caption.txt").write_text(str(p["reel_caption"]).strip() + "\n", encoding="utf-8")
# 취소했던 회차를 다시 보내면 취소 표시를 풀어요
if (folder / "posted.txt").exists():
    (folder / "posted.txt").unlink()
print(folder)
out(folder=folder, mode="render")

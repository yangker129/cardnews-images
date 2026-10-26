"""렌더 마무리: slide_NN.png → NN.jpg(인스타용 JPEG)로 바꾸고 png는 지워요. render_done.txt에 장 수를 남겨요."""
import sys, datetime
from pathlib import Path
from PIL import Image

folder = Path(sys.argv[1])
pngs = sorted(folder.glob("slide_[0-9][0-9].png"))
if not pngs:
    sys.exit("오류: 렌더된 카드가 없어요")
for p in pngs:
    Image.open(p).convert("RGB").save(folder / f"{p.stem[-2:]}.jpg", quality=92)
    p.unlink()
for need in ("reel.mp4", "reel_cover.jpg", "story.jpg"):
    if not (folder / need).exists():
        sys.exit(f"오류: {need}가 없어요")
stamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d %H:%M KST")
(folder / "render_done.txt").write_text(f"{len(pngs)} cards · {stamp}\n")
print(f"{folder}: 카드 {len(pngs)}장 JPG 변환 완료")

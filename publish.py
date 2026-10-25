# publish.py — 폴더 안의 콘텐츠를 인스타에 올립니다
#   피드 : 01.jpg~ (1~10장) + caption.txt          → 올리면 posted.txt
#   릴스 : reel.mp4 (+ reel_caption.txt, reel_cover.jpg) → 올리면 posted_reel.txt
#   스토리: story.jpg                                → 올리면 posted_story.txt
# 각 항목은 표시 파일이 없을 때만 올라가서 두 번 올라가지 않아요.
# posted.txt 내용이 canceled면 그 폴더는 전부 건너뛰어요.
import os, sys, glob, time, urllib.parse, requests

API = "https://graph.instagram.com/v21.0"
USER = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]
BASE = os.environ["IMG_BASE"].rstrip("/")
folder = sys.argv[1].strip("/")

SPECIAL = {"story.jpg", "reel_cover.jpg"}


def url_of(path):
    return BASE + "/" + urllib.parse.quote(path.replace("\\", "/"))


def call(path, **data):
    data["access_token"] = TOKEN
    r = requests.post(f"{API}/{path}", data=data, timeout=120).json()
    if "error" in r:
        e = r["error"]
        raise RuntimeError(f"오류(#{e.get('code')}): {e.get('message')}")
    return r["id"]


def wait_ready(container, minutes=5):
    """인스타가 사진·영상을 다 받아 갈 때까지 기다려요"""
    for _ in range(minutes * 6):
        state = requests.get(f"{API}/{container}",
                             params={"fields": "status_code,status", "access_token": TOKEN}, timeout=30).json()
        code = state.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"인스타가 파일을 처리하지 못했어요: {state.get('status')}")
        time.sleep(10)
    raise RuntimeError("처리 시간이 너무 오래 걸려요(5분 초과)")


def mark(name, text):
    open(f"{folder}/{name}", "w").write(text)


def read(name, default=""):
    p = f"{folder}/{name}"
    return open(p, encoding="utf-8").read() if os.path.exists(p) else default


def done(name):
    return os.path.exists(f"{folder}/{name}")


if read("posted.txt").strip() == "canceled":
    print(f"{folder}는 취소된 회차라서 건너뛰어요")
    sys.exit(0)

results, failures = [], []

# 1) 피드(캐러셀)
if not done("posted.txt"):
    photos = sorted(p for p in glob.glob(f"{folder}/*")
                    if p.lower().endswith((".jpg", ".jpeg")) and os.path.basename(p) not in SPECIAL)[:10]
    if photos:
        try:
            caption = read("caption.txt")
            urls = [url_of(p) for p in photos]
            if len(urls) == 1:
                box = call(f"{USER}/media", image_url=urls[0], caption=caption)
            else:
                kids = [call(f"{USER}/media", image_url=u, is_carousel_item="true") for u in urls]
                box = call(f"{USER}/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)
            wait_ready(box)
            pid = call(f"{USER}/media_publish", creation_id=box)
            mark("posted.txt", pid)
            results.append(f"피드 게시 완료: {pid}")
        except Exception as e:
            failures.append(f"피드 실패 — {e}")

# 2) 릴스
if done("reel.mp4") and not done("posted_reel.txt"):
    try:
        params = dict(media_type="REELS", video_url=url_of(f"{folder}/reel.mp4"),
                      caption=read("reel_caption.txt", read("caption.txt")), share_to_feed="true")
        if done("reel_cover.jpg"):
            params["cover_url"] = url_of(f"{folder}/reel_cover.jpg")
        box = call(f"{USER}/media", **params)
        wait_ready(box, minutes=8)
        pid = call(f"{USER}/media_publish", creation_id=box)
        mark("posted_reel.txt", pid)
        results.append(f"릴스 게시 완료: {pid}")
    except Exception as e:
        failures.append(f"릴스 실패 — {e}")

# 3) 스토리
if done("story.jpg") and not done("posted_story.txt"):
    try:
        box = call(f"{USER}/media", media_type="STORIES", image_url=url_of(f"{folder}/story.jpg"))
        wait_ready(box)
        pid = call(f"{USER}/media_publish", creation_id=box)
        mark("posted_story.txt", pid)
        results.append(f"스토리 게시 완료: {pid}")
    except Exception as e:
        failures.append(f"스토리 실패 — {e}")

for r in results:
    print(r)
for f in failures:
    print(f)
if not results and not failures:
    print(f"{folder}에 새로 올릴 게 없어요")
sys.exit(1 if failures else 0)

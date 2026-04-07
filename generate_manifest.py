"""
執行方式：python generate_manifest.py
在 英文口說練習/ 資料夾執行，自動掃描 lessons/ 資料夾並產生 manifest.json
dg（對話版）與 pb（完整版）同編號自動配對合併成一個 lesson。
"""
import os, json, re

教材資料夾 = "lessons"
raw = {}  # key = base name (e.g. "englishpod_0001dg")

for fname in os.listdir(教材資料夾):
    base, ext = os.path.splitext(fname)
    ext = ext.lower()
    if ext not in (".mp3", ".txt", ".pdf"):
        continue
    if base not in raw:
        raw[base] = {"mp3": None, "txt": None, "pdf": None}
    if ext == ".mp3":
        raw[base]["mp3"] = f"{教材資料夾}/{fname}"
    elif ext == ".txt":
        raw[base]["txt"] = f"{教材資料夾}/{fname}"
    elif ext == ".pdf":
        raw[base]["pdf"] = f"{教材資料夾}/{fname}"

# 配對 dg / pb：找出所有 dg，嘗試合併對應 pb
DG_RE = re.compile(r'^(.+)dg$', re.IGNORECASE)
lessons = {}

for base, files in raw.items():
    m = DG_RE.match(base)
    if m:
        prefix = m.group(1)          # e.g. "englishpod_0001"
        pb_base = prefix + "pb"
        pb = raw.get(pb_base, {})
        lessons[prefix] = {
            "name":   prefix,
            "mp3_pb": pb.get("mp3"),           # 完整版 mp3
            "mp3_dg": files.get("mp3"),        # 對話版 mp3
            "txt":    files.get("txt"),
            "pdf":    files.get("pdf"),
        }
    elif not base.lower().endswith("pb"):
        # 不是 dg 也不是 pb → 獨立 lesson（相容舊格式）
        if base not in lessons:
            lessons[base] = {
                "name":   base,
                "mp3_pb": files.get("mp3"),
                "mp3_dg": None,
                "txt":    files.get("txt"),
                "pdf":    files.get("pdf"),
            }

result = {"lessons": sorted(lessons.values(), key=lambda x: x["name"])}

with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"OK manifest.json generated: {len(result['lessons'])} lessons")

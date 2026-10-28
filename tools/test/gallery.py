#!/usr/bin/env python3
"""Галерея теста модели (скилл /comfy-test): <proj>/index.html из workflows/results.jsonl и workflows/notes.json.

gallery.py <id> [--proj DIR]

notes.json: {имя прогона: {"v": "ok|part|fail|info", "note": "…", "cmp": "имя другого прогона"?},
             "_summary": ["вывод", …], "_sections": [["Заголовок", ["имя", …]], …]?}
Без заметки у любого прогона галерея не собирается — каждый результат должен быть просмотрен.
"""
import argparse, html, json, os, sys

ROWS = os.path.expanduser("~/ai/tools/table/rows.json")
TESTS = os.path.expanduser("~/Videos/ai/tests")
STYLE_ORDER = [("real", "Реализм"), ("anime", "Аниме"), ("drawn", "Рисованное 2D"), ("graphic", "Графика и текст"), ("sound", "Звук")]
BADGE = {"ok": "годно", "part": "частично", "fail": "не вышло", "info": "сравнение"}
IMG, VID, AUD = (".png", ".jpg", ".jpeg", ".webp", ".gif"), (".mp4", ".webm", ".mov", ".mkv"), (".wav", ".mp3", ".flac", ".ogg", ".opus", ".m4a")

ap = argparse.ArgumentParser()
ap.add_argument("id")
ap.add_argument("--proj")
a = ap.parse_args()
proj = a.proj or os.path.join(TESTS, a.id)
row = next((r for r in json.load(open(ROWS)) if r["id"] == a.id), None) or sys.exit(f"Модели «{a.id}» нет в таблице")

R = {}
for line in open(os.path.join(proj, "workflows", "results.jsonl")):
    r = json.loads(line)
    R[r["name"]] = r
notes_path = os.path.join(proj, "workflows", "notes.json")
N = json.load(open(notes_path)) if os.path.exists(notes_path) else {}
missing = [n for n in R if n not in N]
if missing:
    sys.exit(f"Нет заметки у {len(missing)} прогонов: {', '.join(missing)}")

if "_sections" in N:
    sections = N["_sections"]
else:
    by = {}
    for n, r in R.items():
        by.setdefault(r.get("style", "tech"), []).append(n)
    sections = [(t, by.pop(k)) for k, t in STYLE_ORDER if k in by]
    tech = by.pop("tech", None)
    sections += [(k, v) for k, v in sorted(by.items())]
    if tech:
        sections.append(("Технические проверки", tech))


def media(rel):
    src = html.escape(rel)
    ext = os.path.splitext(rel)[1].lower()
    if ext in IMG:
        return f'<a href="{src}" target="_blank"><img loading="lazy" src="{src}" alt=""></a>'
    if ext in VID:
        return f'<video controls preload="metadata" src="{src}"></video>'
    if ext in AUD:
        return f'<audio controls preload="none" src="{src}"></audio>'
    if ext == ".txt":
        return f'<pre>{html.escape(open(os.path.join(proj, rel)).read()[:4000])}</pre>'
    return f'<a href="{src}">{src}</a>'


def card(n):
    r, note = R[n], N[n]
    kind = note.get("v", "info")
    items = [media(f) for f in r["files"]]
    if note.get("cmp") in R:
        items = [media(f) for f in R[note["cmp"]]["files"][:1]] + items
    meta = [f"{k}: {v}" for k, v in (r.get("meta") or {}).items()]
    if r.get("time_s") is not None:
        meta.append(f"{str(r['time_s']).replace('.', ',')} с")
    if r["status"] != "success":
        meta.append(f"<b>{html.escape(r['status'])}</b> {html.escape(r.get('error', ''))}")
    pr = f"<details><summary>Промпт</summary><p>{html.escape(r['prompt'])}</p></details>" if r.get("prompt") else ""
    return f'''<article class="card">
  <div class="media{' two' if len(items) == 2 else ''}">{''.join(items) or '<div class="empty">нет файла</div>'}</div>
  <div class="body">
    <div class="head"><code>{html.escape(n)}</code><span class="b {kind}">{BADGE.get(kind, kind)}</span></div>
    <div class="meta">{' · '.join(meta)}</div>
    <p class="note">{html.escape(note.get('note', ''))}</p>
    {pr}
  </div>
</article>'''


parts = [f'<h2>{html.escape(t)}</h2><div class="grid">' + "\n".join(card(n) for n in names) + "</div>" for t, names in sections]
summary = "".join(f"<li>{s}</li>" for s in N.get("_summary", []))
ok = sum(1 for n in R if N[n].get("v") == "ok")
page = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Тест {html.escape(row["name"])}</title>
<style>
:root{{--bg:#f6f5f2;--fg:#1d1d1f;--mut:#6b6b70;--card:#fff;--line:#e2e0db;--ok:#2e7d4f;--part:#b26a00;--fail:#c0392b;--info:#4a5a8a}}
@media (prefers-color-scheme: dark){{:root{{--bg:#151517;--fg:#ececee;--mut:#9a9aa2;--card:#1f1f23;--line:#2f2f35;--ok:#5cc489;--part:#e0a040;--fail:#ef6b5e;--info:#8fa2dd}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:1500px;margin:0 auto;padding:24px 16px 60px}}
h1{{margin:0 0 4px;font-size:26px}} h2{{margin:40px 0 12px;font-size:20px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.sum{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 20px}} .sum li{{margin:6px 0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}}
.media{{display:grid;background:#0002}} .media.two{{grid-template-columns:1fr 1fr}}
.media img,.media video{{width:100%;height:260px;object-fit:contain;display:block;background:#0003}}
.media audio{{width:100%;margin:12px 0}} .media pre{{margin:0;padding:10px;max-height:260px;overflow:auto;white-space:pre-wrap;font-size:13px}}
.empty{{height:120px;display:grid;place-items:center;color:var(--mut)}}
.body{{padding:10px 12px;display:flex;flex-direction:column;gap:6px;flex:1}}
.head{{display:flex;justify-content:space-between;align-items:center;gap:8px}} code{{font-size:13px;overflow-wrap:anywhere}}
.b{{font-size:12px;padding:1px 8px;border-radius:99px;color:#fff;white-space:nowrap}}
.b.ok{{background:var(--ok)}} .b.part{{background:var(--part)}} .b.fail{{background:var(--fail)}} .b.info{{background:var(--info)}}
.meta{{color:var(--mut);font-size:13px}} .note{{margin:0}}
details{{font-size:13px;color:var(--mut)}} details p{{margin:4px 0 0}}
</style></head><body><main>
<h1>Тест {html.escape(row["name"])}</h1>
<p style="color:var(--mut);margin-top:0">{len(R)} прогонов, годных {ok} · RTX 4070 12 ГБ · клик по картинке — полный размер</p>
<div class="sum"><ul>{summary}</ul></div>
{"".join(parts)}
</main></body></html>'''
open(os.path.join(proj, "index.html"), "w").write(page)
print(f"{os.path.join(proj, 'index.html')}: {len(R)} прогонов, разделов {len(sections)}")

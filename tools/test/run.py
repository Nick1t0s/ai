#!/usr/bin/env python3
"""Прогон теста модели через API ComfyUI (скилл /comfy-test).

run.py <id> <jobs.json> [--only a,b] [--resume] [--prep] [--proj DIR] [--timeout S] [--front] [--api URL]

<id> — строка таблицы (~/ai/tools/table/rows.json). Workflow задачи должен быть в `wf` этой строки;
с --prep (подготовка входных файлов) — в `wf` любой строки таблицы.
--front ставит задачи в начало очереди ComfyUI (цепочки правок, где следующий шаг ждёт предыдущий).

Задача в jobs.json (список):
  name    уникальное имя; f_… — доработка
  style   папка результата: real / anime / drawn / graphic / sound / tech / режим (int8, controlnet, edit…)
  wf      «категория/Имя» → ~/ai/workflows/<категория>/api/<Имя>.json
  set     {node_id: {input: value}}           — правка входов (связь — [node_id, index])
  add     {node_id: {class_type, inputs}}     — новые ноды
  del     [node_id, …]                        — удалить ноды (превью, сравнения)
  upload  {node_id: {input: путь к файлу}}    — загрузка через POST /upload/image
  prompt, meta                                 — только для галереи
"""
import argparse, difflib, json, mimetypes, os, shutil, sys, time, urllib.parse, urllib.request

API = "http://127.0.0.1:8188"
WF = os.path.expanduser("~/ai/workflows")
ROWS = os.path.expanduser("~/ai/tools/table/rows.json")
TESTS = os.path.expanduser("~/Videos/ai/tests")
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call(path, data=None):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Content-Type": "application/json"})
    return json.load(opener.open(req))


def upload_file(filepath, prefix=""):
    """Upload a file via POST /upload/image, return the server-side filename."""
    basename = os.path.basename(filepath)
    server_name = f"{prefix}_{basename}" if prefix else basename
    mime = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    boundary = f"----ComfyUpload{int(time.time() * 1000)}"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{server_name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode() + open(filepath, "rb").read() + (
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="overwrite"\r\n\r\n'
        f"true\r\n"
        f"--{boundary}--\r\n"
    ).encode()
    req = urllib.request.Request(
        f"{API}/upload/image", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    resp = json.load(opener.open(req))
    name = resp.get("name", server_name)
    sub = resp.get("subfolder", "")
    return os.path.join(sub, name) if sub else name


def download_file(filename, subfolder, dest):
    """Download an output file via GET /view."""
    params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": "output"})
    req = urllib.request.Request(f"{API}/view?{params}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with opener.open(req) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def table_row(mid):
    rows = json.load(open(ROWS))
    for r in rows:
        if r["id"] == mid:
            return r, rows
    near = difflib.get_close_matches(mid, [r["id"] for r in rows] + [r["name"] for r in rows], n=5, cutoff=0.3)
    sys.exit(f"Модели «{mid}» нет в таблице. Похожие: {', '.join(near) or '—'}")


def build(j, mid, allowed):
    if j["wf"] not in allowed:
        sys.exit(f"{j['name']}: workflow «{j['wf']}» не из строки {mid} в таблице")
    cat, name = j["wf"].split("/", 1)
    p = json.load(open(os.path.join(WF, cat, "api", name + ".json")))
    for nid in j.get("del", []):
        p.pop(nid, None)
    p.update(j.get("add", {}))
    for nid, inputs in j.get("set", {}).items():
        if nid not in p:
            sys.exit(f"{j['name']}: ноды {nid} нет в {j['wf']}")
        p[nid]["inputs"].update(inputs)
    for nid, d in j.get("upload", {}).items():
        for inp, src in d.items():
            p[nid]["inputs"][inp] = upload_file(src, f"test_{mid}")
    saves = [nid for nid, n in p.items() if "filename_prefix" in n.get("inputs", {})]
    for nid in saves:
        tail = "" if len(saves) == 1 else "_" + nid.replace(":", "-")
        p[nid]["inputs"]["filename_prefix"] = f"tests/{mid}/{j['name']}{tail}"
    return p


def wait(pid, timeout):
    t0, last_q = time.time(), 0
    while True:
        h = call(f"/history/{pid}").get(pid)
        if h and h.get("status", {}).get("status_str") in ("success", "error"):
            return h
        if time.time() - last_q > 30:   # удалён из очереди руками — не ждать вечно
            last_q = time.time()
            q = call("/queue")
            if not h and all(it[1] != pid for k in ("queue_running", "queue_pending") for it in q[k]):
                return None
        if timeout and time.time() - t0 > timeout:
            return None
        time.sleep(2)


def collect(h, j, proj):
    outs, texts = [], []
    for out in (h.get("outputs") or {}).values():
        for key, items in out.items():
            if not isinstance(items, list):
                continue
            for it in items:
                if isinstance(it, dict) and it.get("filename") and it.get("type", "output") == "output":
                    outs.append(it)
                elif key == "text" and isinstance(it, str):
                    texts.append(it)
    d = os.path.join(proj, j["style"])
    os.makedirs(d, exist_ok=True)
    files = []
    for k, it in enumerate(outs):
        ext = os.path.splitext(it["filename"])[1]
        dst = os.path.join(d, j["name"] + (f"_{k}" if len(outs) > 1 else "") + ext)
        download_file(it["filename"], it.get("subfolder", ""), dst)
        files.append(os.path.relpath(dst, proj))
    if texts:
        dst = os.path.join(d, j["name"] + ".txt")
        open(dst, "w").write("\n\n".join(texts))
        files.append(os.path.relpath(dst, proj))
    return files


def record(h, j, pid, mid, proj):
    if h is None:
        return dict(j, status="lost", time_s=None, files=[], pid=pid, model=mid)
    st = h["status"]
    ts = {m[0]: m[1] for m in st.get("messages", [])}
    end = next((ts[k] for k in ("execution_success", "execution_error", "execution_interrupted") if k in ts), None)
    dt = round((end["timestamp"] - ts["execution_start"]["timestamp"]) / 1000, 1) if end and "execution_start" in ts else None
    rec = dict(j, status=st["status_str"], time_s=dt, files=collect(h, j, proj), pid=pid, model=mid)
    if "execution_error" in ts:
        e = ts["execution_error"]
        rec["error"] = f"{e.get('node_type')}: {e.get('exception_message', '').strip()[:500]}"
    if "execution_interrupted" in ts:
        rec["status"] = "interrupted"
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("jobs", nargs="?")
    ap.add_argument("--only")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--prep", action="store_true")
    ap.add_argument("--proj")
    ap.add_argument("--timeout", type=float, default=0)
    ap.add_argument("--front", action="store_true")
    ap.add_argument("--api", default="http://127.0.0.1:8188")
    a = ap.parse_args()
    global API
    API = a.api.rstrip("/")
    if not API.startswith("http://") and not API.startswith("https://"):
        API = "http://" + API
    row, rows = table_row(a.id)
    proj = a.proj or os.path.join(TESTS, a.id)
    os.makedirs(os.path.join(proj, "workflows"), exist_ok=True)
    pend_path = os.path.join(proj, "workflows", "pending.jsonl")
    log_name = "prep.jsonl" if a.prep else "results.jsonl"

    if a.resume:
        queued = [json.loads(l) for l in open(pend_path)] if os.path.exists(pend_path) else []
        queued = [(q["job"], q["pid"]) for q in queued]
    else:
        jobs = json.load(open(a.jobs))
        if a.only:
            only = set(a.only.split(","))
            jobs = [j for j in jobs if j["name"] in only]
        allowed = {w for r in rows for w in r["wf"]} if a.prep else set(row["wf"])
        built = []
        for j in jobs:
            j.setdefault("style", "inputs" if a.prep else "tech")
            j["_log"] = log_name
            built.append((j, build(j, a.id, allowed)))
        queued = []
        with open(pend_path, "a") as pf:
            for j, p in built:
                pid = call("/prompt", {"prompt": p, **({"front": True} if a.front else {})})["prompt_id"]
                queued.append((j, pid))
                pf.write(json.dumps({"job": j, "pid": pid}, ensure_ascii=False) + "\n")
        print(f"в очереди: {len(queued)}", flush=True)

    done = set()
    for j, pid in queued:
        h = wait(pid, a.timeout)
        rec = record(h, j, pid, a.id, proj)
        log = rec.pop("_log", log_name)
        with open(os.path.join(proj, "workflows", log), "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        done.add(pid)
        left = [l for l in open(pend_path) if json.loads(l)["pid"] not in done]
        open(pend_path, "w").writelines(left)
        size = sum(os.path.getsize(os.path.join(proj, f)) for f in rec["files"]) // 1024
        print(f"{j['name']:<30} {rec['status']:<11} {rec['time_s']}s  {size} KB  {rec.get('error', '')}", flush=True)


main()

"""Статическая проверка workflow без запуска ComfyUI: типы узлов есть в коде, файлы из виджетов есть в models/."""
import json, os, re, glob, sys
import ast
_v = ast.parse(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'verify.py')).read())
TEMPLATES = next(n.value.func.value.value for n in _v.body if isinstance(n, ast.Assign) and n.targets[0].id == 'TEMPLATES').split()
TPL = os.path.expanduser('~/ai/comfyui/venv/lib/python3.11/site-packages/comfyui_workflow_templates_json/templates')
MD = os.path.expanduser('~/ai/comfyui/models')
WF = os.path.expanduser('~/ai/comfyui/user/default/workflows')

ROOT = os.path.expanduser('~/ai/comfyui')
lit = set()
for py in glob.glob(ROOT + '/**/*.py', recursive=True):
    if '/venv/' in py:
        continue
    try:
        lit |= set(re.findall(r'''["']([^"'\n]{2,80})["']''', open(py, errors='ignore').read()))
    except OSError:
        pass
# фронтенд-узлы, которые не живут в python
FRONT = {'Note', 'MarkdownNote', 'Reroute', 'PrimitiveNode', 'PrimitiveString', 'GroupNode'}
files = {}
for root, _, fs in os.walk(MD, followlinks=True):
    for f in fs:
        files.setdefault(f, []).append(root)
EXT = ('.safetensors', '.pt', '.pth', '.ckpt', '.bin', '.gguf', '.onnx', '.sft')

def check(w, label):
    sg_ids = {sg['id'] for sg in (w.get('definitions') or {}).get('subgraphs', [])}
    nodes = w.get('nodes', []) + [n for sg in (w.get('definitions') or {}).get('subgraphs', []) for n in sg['nodes']]
    bad = []
    for n in nodes:
        t = n['type']
        if t in sg_ids or t in FRONT or t in lit:
            pass
        else:
            bad.append('node:' + t)
        if n.get('mode') == 4:      # bypass — файлы не нужны
            continue
        wv = n.get('widgets_values')
        vals = wv.values() if isinstance(wv, dict) else (wv or [])
        for v in vals:
            if isinstance(v, str) and v.lower().endswith(EXT) and '/' not in v and os.path.basename(v) not in files:
                bad.append(f'file:{t}:{v}')
    print('OK  ' if not bad else 'BAD ', label, *sorted(set(bad)))
    return bool(bad)

nb = 0
for name in TEMPLATES:
    nb += check(json.load(open(os.path.join(TPL, name + '.json'))), name)
for p in sorted(glob.glob(os.path.join(WF, '*.json'))):
    nb += check(json.load(open(p)), '[wf] ' + os.path.basename(p))
print('с проблемами:', nb)

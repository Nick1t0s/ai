"""Сверка widgets_values узлов сторонних нод с текущими INPUT_TYPES (без сервера и без загрузки моделей)."""
import asyncio, glob, json, os, sys
ROOT = os.path.expanduser('~/ai/comfyui')
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from unittest.mock import MagicMock  # noqa: E402
import server  # noqa: E402
server.PromptServer.instance = MagicMock()   # VHS/DiffuEraser регистрируют HTTP-маршруты при импорте
import nodes  # noqa: E402
r = nodes.init_extra_nodes(init_custom_nodes=True)
if asyncio.iscoroutine(r):
    asyncio.run(r)
WIDGET = {'INT', 'FLOAT', 'STRING', 'BOOLEAN', 'COMBO'}


def expected(cls):
    it = cls.INPUT_TYPES()
    out = []
    for sect in ('required', 'optional'):
        for name, spec in (it.get(sect) or {}).items():
            t = spec[0]
            opts = spec[1] if len(spec) > 1 and isinstance(spec[1], dict) else {}
            if opts.get('forceInput'):
                continue
            if isinstance(t, (list, tuple)):
                out.append((name, 'COMBO', list(t), opts))
            elif t == 'COMBO':
                out.append((name, 'COMBO', opts.get('options', []), opts))
            elif t in WIDGET:
                out.append((name, t, None, opts))
                if t == 'INT' and (opts.get('control_after_generate') or name in ('seed', 'noise_seed')):
                    out.append((name + ':control', 'CTRL', ['fixed', 'increment', 'decrement', 'randomize'], {}))
    return out


SPECS = {}
for p in sorted(glob.glob(os.path.join(ROOT, 'user/default/workflows/*.json'))):
    w = json.load(open(p))
    probs = []
    for n in w['nodes']:
        cls = nodes.NODE_CLASS_MAPPINGS.get(n['type'])
        if cls is None:
            if n['type'] not in ('Note', 'MarkdownNote', 'Reroute', 'PrimitiveNode') and len(n['type']) != 36:
                probs.append(f"{n['id']} {n['type']}: НЕТ УЗЛА")
            continue
        if not str(getattr(cls, 'RELATIVE_PYTHON_MODULE', '')).startswith('custom_nodes'):
            continue
        wv = n.get('widgets_values')
        exp = expected(cls)
        SPECS[n['type']] = [(e[0], e[1], (e[2] or [])[:60], e[3].get('default')) for e in exp]
        if isinstance(wv, dict):
            names = {e[0] for e in exp}
            extra = [k for k in wv if k not in names and k not in ('videopreview', 'choose video to upload')]
            missing = [k for k in names if k not in wv and not k.endswith(':control')]
            if extra or missing:
                probs.append(f"{n['id']} {n['type']}: лишние {extra}, нет {missing}")
            continue
        if not isinstance(wv, list):
            continue
        if len(wv) != len(exp):
            probs.append(f"{n['id']} {n['type']}: значений {len(wv)}, виджетов {len(exp)}: {[e[0] for e in exp]}")
        for (name, t, choices, opts), v in zip(exp, wv):
            if t in ('COMBO', 'CTRL') and choices and v not in choices:
                probs.append(f"{n['id']} {n['type']}.{name} = {v!r} не из {choices[:8]}")
            elif t == 'BOOLEAN' and not isinstance(v, bool):
                probs.append(f"{n['id']} {n['type']}.{name} = {v!r} не bool")
            elif t in ('INT', 'FLOAT') and (not isinstance(v, (int, float)) or isinstance(v, bool)
                                           or v < opts.get('min', -1e30) or v > opts.get('max', 1e30)):
                probs.append(f"{n['id']} {n['type']}.{name} = {v!r} вне диапазона/не число")
            elif t == 'STRING' and not isinstance(v, str):
                probs.append(f"{n['id']} {n['type']}.{name} = {v!r} не строка")
    print(('OK  ' if not probs else 'BAD ') + os.path.basename(p))
    for x in probs:
        print('    ', x)
json.dump(SPECS, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1, default=str)

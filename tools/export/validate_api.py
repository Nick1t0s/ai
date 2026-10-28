"""Офлайн-проверка API-копий по /object_info: типы нод, required-входы, ссылки, значения combo (в т.ч. имена моделей)."""
import glob, json, os, sys

info = json.load(open(sys.argv[1]))
root = sys.argv[2]
INPUT_FILE_KEYS = {'image', 'audio', 'video', 'file', 'upload', 'mask'}


def combo_options(spec):
    t = spec[0]
    if isinstance(t, list):
        return t
    if t == 'COMBO' and len(spec) > 1 and isinstance(spec[1], dict):
        return spec[1].get('options')
    return None


total, bad_files, placeholders = 0, 0, {}
for p in sorted(glob.glob(f'{root}/*/api/*.json')):
    total += 1
    api = json.load(open(p))
    errs = []
    # ComfyUI исполняет и проверяет только выходные ноды и то, от чего они зависят
    todo = [k for k, n in api.items() if info.get(n.get('class_type'), {}).get('output_node')]
    live = set()
    while todo:
        k = todo.pop()
        if k in live or k not in api:
            continue
        live.add(k)
        todo += [v[0] for v in api[k].get('inputs', {}).values() if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str)]
    if not live:
        errs.append('нет ни одной выходной ноды')
    for nid, n in api.items():
        if nid not in live:
            continue
        ct = n.get('class_type')
        if ct not in info:
            errs.append(f'{nid}: неизвестный тип {ct}')
            continue
        req = info[ct]['input'].get('required', {})
        opt = info[ct]['input'].get('optional', {})
        ins = n.get('inputs', {})
        for k, spec in req.items():
            if spec[0] == 'COMFY_AUTOGROW_V3':   # может быть пустым
                continue
            if k not in ins and not any(x.startswith(k + '.') for x in ins):
                errs.append(f'{nid} {ct}: нет required-входа {k}')
        for k, v in ins.items():
            if isinstance(v, list) and len(v) == 2 and isinstance(v[1], int) and isinstance(v[0], str):
                if v[0] not in api:
                    errs.append(f'{nid} {ct}.{k}: ссылка на отсутствующий узел {v[0]}')
                continue
            spec = req.get(k) or opt.get(k)
            if not spec:
                continue
            kind = spec[0]
            # сдвиг widgets_values обычно даёт значение не того типа
            if (kind in ('INT', 'FLOAT') and (isinstance(v, bool) or not isinstance(v, (int, float)))) or \
               (kind == 'BOOLEAN' and not isinstance(v, bool)) or (kind == 'STRING' and not isinstance(v, str)):
                errs.append(f'{nid} {ct}.{k}: {kind} получил {v!r}'[:200])
                continue
            if ct == 'CustomCombo':   # варианты задаются в самом workflow
                continue
            opts = combo_options(spec)
            if opts is not None and v not in opts:
                if k in INPUT_FILE_KEYS or 'upload' in (spec[1] if len(spec) > 1 and isinstance(spec[1], dict) else {}):
                    placeholders.setdefault(p, []).append(f'{ct}.{k}={v}')
                else:
                    errs.append(f'{nid} {ct}.{k}: значение {v!r} не из списка ({len(opts)} вариантов)')
    if errs:
        bad_files += 1
        print('FAIL', os.path.relpath(p, root))
        for e in errs[:12]:
            print('    ', e)
print(f'API-файлов: {total}, с ошибками: {bad_files}')
json.dump(placeholders, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
print('файлов с входными плейсхолдерами:', len(placeholders))

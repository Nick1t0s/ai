"""Собирает ~/ai/models.md и ~/ai/models.xlsx (через .fods + LibreOffice) из models_data.py."""
import html, json, os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estimate import A_LIM, SAFE, fmt_pct, fmt_t, max_frames, ratio, run_s, step_s, tokens, DISK   # noqa: E402
from models_data import R, SHEETS, STYLES   # noqa: E402

AI = os.path.expanduser('~/ai')
WFD = AI + '/workflows'
MD = AI + '/comfyui/models'
ALIAS = {'clip': 'text_encoders', 'unet': 'diffusion_models'}
# модели кастомных нод: размер папок (ГБ), по id строки или по id модели
DISK_MANUAL = {'fish-s2': 8.0, 'qwen3-tts': 14.0, 'voxcpm2': 4.7, 'chatterbox': 3.0, 'mmaudio': 5.3, 'hunyuan-foley': 8.2,
               'heartmula': 22.4, 'heartmula-lyrics': 3.1}
STYLE_TITLE = dict(STYLES)
assert len({r['id'] for r in R}) == len(R) and len({r['name'] for r in R}) == len(R), 'дубли id или имён строк'
DM_DIRS = ('diffusion_models', 'checkpoints')


def wf_files(names):
    files = {}
    for n in names:
        cat, base = n.split('/', 1)
        p = f'{WFD}/{cat}/ui/{base}.json'
        assert os.path.exists(p), p
        w = json.load(open(p))
        nodes = w['nodes'] + [x for sg in (w.get('definitions') or {}).get('subgraphs', []) for x in sg['nodes']]
        for x in nodes:
            for mm in (x.get('properties') or {}).get('models') or []:
                d = ALIAS.get(mm['directory'], mm['directory'])
                f = os.path.join(MD, d, mm['name'])
                if os.path.exists(f):
                    files[(d, mm['name'])] = os.path.getsize(f)
            if x['type'] == 'CheckpointLoaderSimple' and x.get('widgets_values'):
                f = os.path.join(MD, 'checkpoints', x['widgets_values'][0])
                if os.path.exists(f):
                    files[('checkpoints', x['widgets_values'][0])] = os.path.getsize(f)
    return files


def gb(b):
    return f'{b / 1e9:.1f}'.replace('.', ',')


rows = []
for r in R:
    files = wf_files([w for w in r['wf'] if w not in r.get('wf_nosize', ())])
    manual = DISK_MANUAL.get(r['id'], DISK_MANUAL.get(r['base']))
    total = sum(files.values()) / 1e9 if files else (manual or 0)
    if manual:
        total = max(total, manual)
    dm = [s for (d, _), s in files.items() if d in DM_DIRS]
    biggest = max(files.values()) if files else 0
    dm_bytes = max(dm) if dm else 0
    if r['base'] == 'ltx23':         # в чекпоинте кроме трансформера VAE, аудио-VAE и вокодер
        dm_bytes = 19e9
    out = dict(r, total=total, biggest=biggest / 1e9, nfiles=len(files))
    a = r.get('arch')
    if r['kind'] == 'image':
        T = tokens(a, a['W'], a['H'])
        rt = ratio(a, T)
        t_run = run_s(a, a['W'], a['H'], 1, a['steps'], dm_bytes)
        t_step = step_s(a, T, dm_bytes)
        T2 = tokens(a, 1448, 1448)
        lab0, st0, ps0 = (a.get('modes') or [(None, a['steps'], a['passes'])])[0]
        t2 = run_s(dict(a, passes=ps0), 1448, 1448, 1, st0, dm_bytes)
        out['mem'] = (f'Веса пайплайна {gb(total * 1e9)} ГБ, самый большой файл {gb(biggest)} ГБ. VRAM займёт ~10–11 ГБ (dynamic VRAM), '
                      f'что не влезло — подкачивается из RAM. Активации {a["W"]}×{a["H"]}: {fmt_pct(rt)} от твоего предела.')
        modes = a.get('modes') or [(f'{a["steps"]} шагов', a['steps'], a['passes'])]
        mt = [(lab, run_s(dict(a, passes=ps), a['W'], a['H'], 1, st, dm_bytes)) for lab, st, ps in modes]
        t_run = min(t for _, t in mt)
        out['time'] = (f'{a["W"]}×{a["H"]}: ' + '; '.join(f'{lab} — {fmt_t(t)}' for lab, t in mt) +
                       f'. Первый запуск +{fmt_t(total * 1e9 / DISK)} на чтение весов с диска.')
        out['maxs'] = r.get('maxs') or f'{r["native"]}. 2 МП (1448²){", " + lab0 if lab0 else ""}: {fmt_t(t2)}, активации {fmt_pct(ratio(a, T2))} — память не ограничивает, предел задаёт сама модель.'
        out['ratio'] = rt
        out['t_default'] = t_run
    elif r['kind'] == 'video':
        F = a['F']
        T = tokens(a, a['W'], a['H'], F)
        rt = ratio(a, T)
        t_run = run_s(a, a['W'], a['H'], F, a['steps'], dm_bytes)
        t_step = step_s(a, T, dm_bytes)
        out['mem'] = (f'Веса пайплайна {gb(total * 1e9)} ГБ, самый большой файл {gb(biggest)} ГБ. VRAM ~10–11 ГБ (dynamic VRAM), '
                      f'остальное идёт через RAM/mmap. Активации по умолчанию ({a["W"]}×{a["H"]}×{F}): {fmt_pct(rt)} от твоего предела.')
        modes = a.get('modes') or [(f'{a["steps"]} шагов', a['steps'], a['passes'])]
        mt = [(lab, run_s(dict(a, passes=ps), a['W'], a['H'], F, st, dm_bytes)) for lab, st, ps in modes]
        t_run = min(t for _, t in mt)
        out['time'] = (f'{a["W"]}×{a["H"]}, {F} кадров: ' + '; '.join(f'{lab} — {fmt_t(t)}' for lab, t in mt) +
                       f'. Первый запуск +{fmt_t(total * 1e9 / DISK)} на чтение весов.')
        parts = []
        for (W, H, lab) in ((832, 480, '480p'), (1280, 720, '720p')):
            fmax, fmem = max_frames(a, W, H)
            sec = fmax / a['fps']
            lab0, st0, ps0 = modes[0]
            t = run_s(dict(a, passes=ps0), W, H, fmax, st0, dm_bytes)
            note = '' if fmem <= a['native_F'] else f' (память позволила бы до {fmem}, но дальше родного предела модели)'
            parts.append(f'{lab}: до {fmax} кадров ≈ {sec:.1f} с, {fmt_t(t)}{note}'.replace('.', ',', 1))
        out['maxs'] = f'{r["native"]}. Время — в режиме «{modes[0][0]}». ' + '; '.join(parts) + '.'
        out['ratio'] = rt
        out['t_default'] = t_run
    elif r['kind'] == 'sdxl':
        out['mem'] = f'Чекпоинт {gb(biggest)} ГБ — целиком в VRAM. Активации — доли процента от предела.'
        out['time'] = r.get('time') or '832×1216, 28–30 шагов: ~8–12 с (≈3–4 it/s с CFG на 4070). Первый запуск +~3 с.'
        out['maxs'] = r.get('maxs') or f'{r["native"]}. Больше 1,5 МП без hires fix даёт дубли и артефакты (ограничение SDXL, а не памяти).'
        out['ratio'], out['t_default'] = 0.01, 10
    else:   # audio / tool
        out['mem'] = (f'Модели {gb(total * 1e9)} ГБ. ' if total else '') + r.get('mem', '')
        out['ratio'], out['t_default'] = 0.0, 0
    # вердикт
    v, why = '✅', 'укладывается с запасом'
    if out['ratio'] > 0.9:
        v, why = '❌', 'по умолчанию выше предела активаций'
    elif out['ratio'] > 0.65:
        v, why = '⚠️', 'близко к пределу активаций'
    if out['biggest'] > 22:
        v, why = '⚠️', 'файл больше RAM-кэша: подкачка с диска, медленнее'
    if out['t_default'] > 1800:
        v, why = '⚠️', 'запустится, но по умолчанию очень долго — снижай разрешение'
    if r['id'] == 'heartmula':       # транскриптор (heartmula-lyrics) патч не касается
        v, why = '⚠️', 'без моего патча не влезла бы в VRAM; патч не проверен запуском'
    out['verdict'], out['why'] = v, why
    rows.append(out)

SHEET_ORDER = {k: i for i, (k, *_) in enumerate(SHEETS)}
rows.sort(key=lambda x: SHEET_ORDER[x['sheet']])   # по листам, внутри листа — порядок models_data.py
json.dump([{k: v for k, v in x.items() if k != 'arch'} for x in rows], open(os.path.join(os.path.dirname(__file__), 'rows.json'), 'w'), ensure_ascii=False, indent=1)

# ───────────────────────── Markdown ─────────────────────────
INTRO = f"""# Модели ComfyUI на этом ПК: что умеют, сколько ждать, где предел

RTX 4070 12 ГБ · 31 ГБ RAM + zram 16 ГБ · ComfyUI в `~/ai/comfyui` · шаблоны в `~/ai/workflows/<папка>/ui|api/`.

**Цифры времени и памяти — оценки, а не замеры, кроме помеченных «Замер».** Как считал — в разделе «Методика» в конце. Точность по времени примерно ±50%.

**Строка — модель в одном режиме работы.** Режимы различаются тем, что подаётся на вход: текст, картинка, видео, аудио, маска. У модели с несколькими режимами (Wan, LTX, Qwen-Image, TTS…) несколько строк, id режима — с суффиксом (`-i2v`, `-edit`, `-control`, `-clone`…).

**Разделы (и листы в `models.xlsx`):** {' · '.join(f'[{t}](#sheet-{k})' for k, t, *_ in SHEETS)}. В каждом — свои колонки умений: ✓ — режим это умеет в наших шаблонах, — — не умеет, ? — не проверено.

**Колонки «Опыт»** ({', '.join(t for _, t in STYLES)}) — выводы из реальных прогонов в этом стиле: что модель делает хорошо, где ошибается, как это обойти. Прочерк — в этом стиле модель ещё не запускалась.

## Коротко: взлетит или нет

- **Вес моделей — не стена.** ComfyUI по умолчанию включает Dynamic VRAM (comfy-aimdo): модели открываются через mmap и по частям подгружаются из RAM или с NVMe. Поэтому MiniMax H3 с 44 ГБ весов у тебя и работал. Большой файл делает генерацию медленнее, но не ломает её.
- **Стена — активации** (разрешение × длительность). Твой замер MiniMax H3 (25 с при 0,4 МП) взят за 100%. Почти все шаблоны по умолчанию используют **5–50%** этого предела.
- **Что под вопросом:**
  - **HeartMuLa:** без патча не влезла бы в VRAM (модель и кодек одновременно — 14,3 ГБ). Я исправил ноду так, чтобы они лежали на GPU по очереди. Патч не проверен запуском.
  - **LTX-2.3:** самый большой файл, 29,5 ГБ. Веса будут подкачиваться, генерация медленнее.
  - **Hunyuan 1.5 на 720p×121:** запустится, но займёт около часа. Бери 480p.
- **Рабочий стол отнимает запас.** Открытые IDE и браузер занимают ~11 ГБ RAM и 1,3 ГБ VRAM, поэтому в оценках «максимума» оставлен запас: {int(SAFE * 100)}% от твоего предела.
- **Если что-то упадёт по памяти:** уменьши разрешение или длину, закрой тяжёлые программы. Если пойдут чёрные кадры или шум — убери `--force-fp16` из `start_lowvram.sh` или вставь в workflow ноду `ModelComputeDtype` (bf16) после загрузчика модели (проверено: Qwen-Image и Qwen Edit с `--force-fp16` дают чёрный кадр).

"""

def exp(x, k):
    return (x.get('exp') or {}).get(k) or '—'


def cap(x, k):
    return x['cap'].get(k) or '—'


def cell_md(v):
    return str(v).replace('|', '\\|').replace('\n', ' ')


lines = [INTRO]
for key, title, caps, styles in SHEETS:
    part = [x for x in rows if x['sheet'] == key]
    head = ['', 'Модель', 'Режим'] + [t for _, t in caps] + ['Вес, ГБ', 'Время по умолчанию'] + [f'Опыт: {STYLE_TITLE[k]}' for k in styles]
    lines += [f'<a id="sheet-{key}"></a>\n## {title}\n', '| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for x in part:
        lines.append('| ' + ' | '.join(cell_md(v) for v in [x['verdict'], f"[{x['model']}](#{x['id']})", x['mode']] + [cap(x, k) for k, _ in caps] +
                                       [gb(x['total'] * 1e9), x['time'].split(' Первый запуск')[0]] + [exp(x, k) for k in styles]) + ' |')
    lines.append('')
lines.append('✅ — укладывается с запасом · ⚠️ — работает с оговорками (см. раздел модели) · ❌ — по умолчанию не влезет · '
             'умения: ✓ — умеет, — — нет, ? — не проверено · «Опыт» — выводы из реальных прогонов, прочерк — не запускалась\n')

for x in rows:
    lines += [f'\n---\n\n<a id="{x["id"]}"></a>\n## {x["verdict"]} {x["name"]}\n',
              f'*{x["cat"]}* · лицензия: {x["lic"]} · вердикт: {x["why"]}\n',
              f'**Режим:** {x["mode"]} · id `{x["id"]}`\n',
              '**Умеет:** ' + '; '.join(f'{t} — {v}' for k, t in next(s[2] for s in SHEETS if s[0] == x['sheet']) if (v := x['cap'].get(k)) and v != '—') + '\n',
              '**Шаблоны** (`~/ai/workflows/…/ui/` — для ручной работы, `…/api/` — для API):\n']
    lines += [f'- `{w.split("/")[0]}/ui|api/{w.split("/", 1)[1]}.json`' for w in x['wf']]
    lines += ['', f'**Память:** {x["mem"]}', '', f'**Время:** {x["time"]}', '', f'**Максимум на этом ПК:** {x["maxs"]}', '',
              f'**Как писать промпт:** {x["prompt"]}', '', f'**Сильные стороны:** {x["plus"]}', '', f'**Слабые стороны:** {x["minus"]}', '']
    if x.get('exp'):
        lines += ['**Опыт (реальные прогоны):**', ''] + [f'- *{t}:* {x["exp"][k]}' for k, t in STYLES if k in x['exp']] + ['']
    lines += ['**Источники:** ' + ' · '.join(f'<{s}>' for s in x['src'])]

METHOD = f"""

---

## Методика оценок

- **Предел активаций (100%).** Взят твой замер: MiniMax H3, 25 с при 0,4 МП (864×480, 600 кадров @24fps). Это ≈69 тыс. латентных токенов × ширина FFN 28 672 = {A_LIM / 1e9:.2f}·10⁹ элементов. Для другой модели доля = токены × её ширина FFN / этот предел.
  - Токены = (ширина / px) × (высота / px) × латентные кадры. px = сжатие VAE × patch: 16 у Wan 2.1/2.2-14B, Hunyuan, Qwen, Flux; 32 у Wan 5B, LTX, MiniMax.
  - По времени кадры сжимаются так: 4n+1 у Wan и Hunyuan, 8n+1 у LTX, 17k+5 у MiniMax.
  - Референсы и исходное видео умножают число токенов (×2 у Bernini, SCAIL, Animate и Qwen-Edit).
  - «Максимум» в таблице считается при {int(SAFE * 100)}% предела (запас на рабочий стол) и не выходит за родной предел модели.
- **Время шага** = проходы (CFG>1 → 2) × (2·N·T + 4·L·T²·d) / 62 TFLOPS + подкачка невлезающих весов по PCIe (~13 ГБ/с, в VRAM держится ~9 ГБ весов).
  - 62 «эффективных» TFLOPS для 4070 откалиброваны по шаблону Wan 2.2 14B на RTX 4090D (640×640×81: 20 шагов ≈ 513 с, 4 шага ≈ 71 с) с поправкой 4070 ≈ 0,4 × 4090D.
  - Сверка с отзывами для 4070: Z-Image Turbo — по оценке 6–8 с, в отзывах 3–4 с; Wan 14B Lightning 480p — по оценке ~2 мин, в отзывах на 12–16 ГБ картах 2–5 мин.
  - Плюс декод VAE (секунды на мегапиксель-кадр) и первая загрузка весов с NVMe (~3 ГБ/с).
- **Аудио, утилиты и LLM** — по RTF и замерам из источников, грубее (×2).
- **Не учтено:**
  - сэмплеры с двумя вызовами модели на шаг (heun, dpmpp_sde) — их время ×2;
  - «холодный» compile;
  - TeaCache и EasyCache — они ускоряют;
  - нехватка RAM при открытых IDE: тогда веса читаются с диска на каждом шаге, +1–3 с/шаг у LTX и MiniMax.
"""
lines.append(METHOD)
open(AI + '/models.md', 'w').write('\n'.join(lines) + '\n')

# ───────────────────────── XLSX через Flat ODS: лист на сферу ─────────────────────────
HEAD_L = [('Взлетит?', 9), ('Категория', 16), ('Модель', 26), ('Режим (вход → выход)', 30)]
HEAD_R = [('Вердикт', 22), ('Шаблоны (папка/имя; ui и api)', 40), ('Вес на диске, ГБ', 9),
          ('Память', 40), ('Время (оценка)', 40), ('Максимум на этом ПК', 46), ('Как писать промпт', 70), ('Сильные стороны', 45),
          ('Слабые стороны', 45), ('Лицензия', 22), ('Источники', 40), ('id', 18)]


def cell(v, style='wrap'):
    if isinstance(v, (int, float)):
        return f'<table:table-cell table:style-name="{style}" office:value-type="float" office:value="{v:.1f}"><text:p>{v:.1f}</text:p></table:table-cell>'
    paras = ''.join(f'<text:p>{html.escape(p)}</text:p>' for p in str(v).split('\n'))
    return f'<table:table-cell table:style-name="{style}" office:value-type="string">{paras}</table:table-cell>'


def col_letter(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def sheet(key, name, header, data, widths):
    cols = ''.join(f'<table:table-column table:style-name="{key}{i}"/>' for i in range(len(widths)))
    out = [f'<table:table table:name="{html.escape(name)}">{cols}',
           '<table:table-row>' + ''.join(cell(h, 'head') for h in header) + '</table:table-row>']
    for row in data:
        out.append('<table:table-row>' + ''.join(cell(v) for v in row) + '</table:table-row>')
    out.append('</table:table>')
    return '\n'.join(out)


tables, col_styles, ranges = [], [], []
for si, (key, title, caps, styles) in enumerate(SHEETS):
    cols = HEAD_L + [(t, 16) for _, t in caps] + [(f'Опыт: {STYLE_TITLE[k]}', 40) for k in styles] + HEAD_R
    data = [[x['verdict'], x['cat'], x['model'], x['mode']] + [cap(x, k) for k, _ in caps] + [(x.get('exp') or {}).get(k, '') for k in styles] + [
             x['why'], '\n'.join(x['wf']), round(x['total'], 1), x['mem'], x['time'], x['maxs'],
             x['prompt'].replace('**', ''), x['plus'].replace('**', ''), x['minus'].replace('**', ''), x['lic'], '\n'.join(x['src']), x['id']]
            for x in rows if x['sheet'] == key]
    tables.append(sheet(key, title, [c for c, _ in cols], data, [w for _, w in cols]))
    col_styles += [f'<style:style style:name="{key}{i}" style:family="table-column"><style:table-column-properties style:column-width="{w * 0.21:.2f}cm"/></style:style>'
                   for i, (_, w) in enumerate(cols)]
    ranges.append(f'<table:database-range table:name="__Anonymous_Sheet_DB__{si}" table:target-range-address="\'{title}\'.A1:\'{title}\'.{col_letter(len(cols))}{len(data) + 1}" '
                  'table:display-filter-buttons="true"/>')
method_rows = [[p.strip('- ').replace('**', '')] for p in (INTRO.split('## Коротко: взлетит или нет')[1] + METHOD).split('\n') if p.strip() and not p.startswith('#') and p.strip() != '---']
fods = f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" office:version="1.3" office:mimetype="application/vnd.oasis.opendocument.spreadsheet">
<office:automatic-styles>{''.join(col_styles)}
<style:style style:name="m0" style:family="table-column"><style:table-column-properties style:column-width="30cm"/></style:style>
<style:style style:name="wrap" style:family="table-cell"><style:table-cell-properties fo:wrap-option="wrap" style:vertical-align="top"/></style:style>
<style:style style:name="head" style:family="table-cell"><style:table-cell-properties fo:wrap-option="wrap" fo:background-color="#dde6f0" style:vertical-align="middle"/><style:text-properties fo:font-weight="bold"/></style:style>
</office:automatic-styles>
<office:body><office:spreadsheet>
{chr(10).join(tables)}
{sheet('m', 'Методика', ['Как читать таблицу и откуда цифры'], method_rows, [140])}
<table:database-ranges>{''.join(ranges)}</table:database-ranges>
</office:spreadsheet></office:body></office:document>
"""
tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(tmp, exist_ok=True)
open(f'{tmp}/models.fods', 'w').write(fods)
subprocess.run(['soffice', '--headless', '--convert-to', 'xlsx', '--outdir', tmp, f'{tmp}/models.fods'], check=True,
               capture_output=True, env=dict(os.environ, HOME=tmp))
shutil.move(f'{tmp}/models.xlsx', AI + '/models.xlsx')
print('rows', len(rows), {t: sum(x['sheet'] == k for x in rows) for k, t, *_ in SHEETS}, {v: sum(x['verdict'] == v for x in rows) for v in ('✅', '⚠️', '❌')})

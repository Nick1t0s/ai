"""Оценки памяти и времени для RTX 4070 12 ГБ / 31 ГБ RAM (без запуска моделей).

Калибровка:
  * предел активаций — реальный замер пользователя: MiniMax H3, 25 с при 0,4 МП (864×480, 600 кадров)
    = 69 030 токенов × ширина FFN 28 672 → A_LIM;
  * производительность — шаблон Comfy Wan 2.2 14B на RTX 4090D (640×640×81: 20 шагов ≈ 513 с, 4 шага ≈ 71 с)
    → ~150 «эффективных» TFLOPS по этой формуле; RTX 4070 ≈ 0,40 от 4090D → EFF ≈ 62 TFLOPS.
"""
import math

A_LIM = 69030 * 28672          # предел пользователя = 1.0
SAFE = 0.8                     # запас под рабочий стол (1,3 ГБ VRAM) и фрагментацию
EFF = 62e12                    # FLOPs/с, RTX 4070
PCIE = 13e9                    # Б/с, подкачка невлезающих весов на каждый проход
VRAM_W = 9e9                   # сколько весов реально держится в VRAM
DISK = 3e9                     # Б/с, первое чтение с NVMe


def lat(F, tf):
    if tf == 'wan':
        return (F - 1) // 4 + 1
    if tf == 'ltx':
        return (F - 1) // 8 + 1
    if tf == 'mm':
        return max(1, (F - 5) // 17 * 5 + 2)
    return 1


def frames(lf, tf):
    if tf == 'wan':
        return (lf - 1) * 4 + 1
    if tf == 'ltx':
        return (lf - 1) * 8 + 1
    if tf == 'mm':
        return (lf - 2) // 5 * 17 + 5
    return 1


def tokens(a, W, H, F=1):
    sp = math.ceil(W / a['px']) * math.ceil(H / a['px'])
    return sp * lat(F, a.get('tf')) * a.get('mult', 1)


def ratio(a, T):
    return T * a['ffn'] / A_LIM


def step_s(a, T, dm_bytes):
    flops = a['passes'] * (2 * a['N'] * 1e9 * T + 4 * a['L'] * T * T * a['d'])
    stream = max(0.0, dm_bytes - VRAM_W) / PCIE * a['passes']
    return flops / EFF + stream


def run_s(a, W, H, F, steps, dm_bytes):
    """Время одного прогона без загрузки с диска: шаги + декод VAE."""
    if a.get('ltx'):    # две ступени: половинное разрешение (8 шагов) + полное (3 шага)
        t = 8 * step_s(a, tokens(a, W // 2, H // 2, F), dm_bytes) + 3 * step_s(a, tokens(a, W, H, F), dm_bytes)
    else:
        t = steps * step_s(a, tokens(a, W, H, F), dm_bytes)
    return t + a['vae'] * W * H / 1e6 * F


def max_frames(a, W, H):
    """Сколько кадров влезает в SAFE-долю предела активаций, но не больше родного предела модели."""
    sp = math.ceil(W / a['px']) * math.ceil(H / a['px']) * a.get('mult', 1)
    lf = int(SAFE * A_LIM / a['ffn'] / sp)
    f_mem = frames(max(lf, 1), a['tf'])
    return min(f_mem, a['native_F']), f_mem


def fmt_t(s):
    if s < 60:
        return f'~{max(1, round(s))} с'
    if s < 3600:
        return f'~{s / 60:.0f} мин' if s >= 600 else f'~{s / 60:.1f} мин'.replace('.', ',')
    return f'~{s / 3600:.1f} ч'.replace('.', ',')


def fmt_pct(r):
    return f'{r * 100:.0f}%' if r >= 0.01 else '<1%'

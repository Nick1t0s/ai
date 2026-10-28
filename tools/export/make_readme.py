"""~/ai/workflows/README.md: как пользоваться ui/ и api/, состав папок, какие входы подставить в API-копиях."""
import collections, json, os, sys

S = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(f'{S}/list.json'))
ph = json.load(open(f'{S}/placeholders.json'))
W = os.path.expanduser('~/ai/workflows')
DESC = {
    'image-photo': 'Фото: реализм и универсальные модели', 'image-anime': 'Фото: аниме', 'image-edit': 'Редактирование фото',
    'video': 'Видео: текст/картинка → видео',
    'video-reference': 'Видео по референсу: замена персонажа, перенос движения, озвучка, монтаж, удаление объектов',
    'audio-tts': 'Речь (TTS, клон голоса)', 'audio-music': 'Музыка и песни', 'audio-sound': 'Звуки, SFX, звук к видео',
    'utility': 'Утилиты: апскейл, маски, поза, глубина, основы', 'llm': 'LLM: текст, подписи к картинкам',
    '3d': '3D: геометрия и меши', 'training': 'Обучение (LoRA, дообучение голоса)'}
cnt = collections.Counter(i['cat'] for i in items)
kinds = collections.Counter(i['kind'] for i in items)
F = '```'

L = ['# Workflow для ComfyUI: UI- и API-копии', '',
     'Каждый workflow лежит в двух экземплярах с одинаковым именем:', '',
     '- `ui/` — обычный workflow для ручной работы. Перетащи файл в окно ComfyUI или открой через Workflow → Open.',
     '- `api/` — тот же граф в API-формате для `POST /prompt`. Его сделал сам фронтенд ComfyUI (`graphToPrompt`), поэтому подграфы развёрнуты, а выключенные (bypass) ноды убраны.',
     '', 'Описание моделей, оценки времени и памяти, советы по промптам — в `~/ai/models.md` и `~/ai/models.xlsx`.', '',
     '## Папки', '', '| Папка | Что внутри | Шт. |', '|---|---|---|']
L += [f'| `{c}/` | {d} | {cnt[c]} |' for c, d in DESC.items()]
L += ['', f'Всего {len(items)} workflow ({len(items) * 2} файлов). Откуда они:', '',
      f'- {kinds["template"]} — официальные шаблоны ComfyUI, для которых скачаны все модели;',
      f'- {kinds["own"]} — мои: SDXL, AnimeGen, Qwen Edit 2511 на fp8 и исправленные примеры аудио-нод (они же лежат в боковой панели ComfyUI);',
      f'- {kinds["upstream"]} — примеры из репозиториев нод (HeartMuLa, Qwen-TTS, VoxCPM). Ноды вывода текста из неустановленных паков заменены на встроенную `PreviewAny`;',
      f'- {kinds["external"]} — авторский workflow NetaYume с Tensor.Art, переключён на локальный чекпоинт.', '',
      'Не вошли:', '',
      '- официальные workflow Kandinsky 5 от Сбера: им нужны собственные ноды `Kandinsky5*`, а T2I, T2V и I2V уже есть во встроенных шаблонах;',
      '- `differaser.json`: для DiffuEraser не хватает моделей, удалять объекты из видео лучше через `video-reference/VOID`.', '',
      '## Как запустить API-копию', '',
      'ComfyUI должен быть запущен: `cd ~/ai/comfyui && ./start_lowvram.sh`. Запрос идёт на локальный адрес, поэтому прокси не нужен:', '',
      F + 'bash', 'cd ~/ai/workflows/image-photo/api',
      'jq -n --slurpfile p "Z-Image-Turbo текст в изображение.json" \'{prompt: $p[0]}\' |',
      '  curl --noproxy "*" -s -X POST http://127.0.0.1:8188/prompt -H "Content-Type: application/json" -d @-',
      '# ответ: {"prompt_id": "..."}; статус: GET /history/<prompt_id>; файлы: /tmp/comfyui/output', F, '',
      'На Python:', '', F + 'python', 'import json, urllib.request',
      'p = json.load(open("Z-Image-Turbo текст в изображение.json"))',
      '# промпт: найди ноду CLIPTextEncode / TextEncode… и поменяй её inputs["text"]',
      'req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=json.dumps({"prompt": p}).encode(),',
      '                             headers={"Content-Type": "application/json"})',
      'print(urllib.request.urlopen(req).read().decode())', F, '',
      '**Входные файлы.** Картинки, видео и аудио, указанные в шаблонах, — примеры авторов, у тебя их нет. '
      'Положи свои файлы в папку input (`/tmp/comfyui/input` при запуске через `start_lowvram.sh`) или загрузи через `POST /upload/image`, '
      'а потом впиши имя файла в нужное поле API-копии (список полей ниже). В UI просто выбери файл в ноде Load Image / Load Audio / Load Video.', '',
      'Примеры входов к официальным шаблонам: https://github.com/Comfy-Org/workflow_templates/tree/main/input', '',
      '**Особые случаи:**', '',
      '- `audio-tts/TTS - Qwen3-TTS save voice`: файл `designed_voice.wav` появится после шага 1 (сохранения голоса). До этого Load Speaker подсвечен красным.',
      '- `training/Qwen3-TTS - дообучение голоса`: в UI-копии все ноды выключены, как в оригинале автора. В API-копии они включены, поэтому отправка сразу запустит обучение.',
      '- `training/VoxCPM - обучение LoRA`: поправь пути к датасету и выходной папке (в примере автора пути Windows).', '',
      '## Какие поля заменить в API-копиях', '', '| Файл | Входы: нода.поле = имя файла в шаблоне |', '|---|---|']
for p, v in sorted(ph.items()):
    L.append(f'| `{os.path.relpath(p, W)}` | ' + ', '.join(f'`{x}`' for x in dict.fromkeys(v)) + ' |')
open(W + '/README.md', 'w').write('\n'.join(L) + '\n')
print(len(L), dict(kinds))

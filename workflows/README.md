# Workflow для ComfyUI: UI- и API-копии

Каждый workflow лежит в двух экземплярах с одинаковым именем:

- `ui/` — обычный workflow для ручной работы. Перетащи файл в окно ComfyUI или открой через Workflow → Open.
- `api/` — тот же граф в API-формате для `POST /prompt`. Его сделал сам фронтенд ComfyUI (`graphToPrompt`), поэтому подграфы развёрнуты, а выключенные (bypass) ноды убраны.

Описание моделей, оценки времени и памяти, советы по промптам — в `~/ai/models.md` и `~/ai/models.xlsx`.

## Папки

| Папка | Что внутри | Шт. |
|---|---|---|
| `image-photo/` | Фото: реализм и универсальные модели | 18 |
| `image-anime/` | Фото: аниме | 9 |
| `image-edit/` | Редактирование фото | 17 |
| `video/` | Видео: текст/картинка → видео | 18 |
| `video-reference/` | Видео по референсу: замена персонажа, перенос движения, озвучка, монтаж, удаление объектов | 10 |
| `audio-tts/` | Речь (TTS, клон голоса) | 6 |
| `audio-music/` | Музыка и песни | 5 |
| `audio-sound/` | Звуки, SFX, звук к видео | 3 |
| `utility/` | Утилиты: апскейл, маски, поза, глубина, основы | 23 |
| `llm/` | LLM: текст, подписи к картинкам | 3 |
| `3d/` | 3D: геометрия и меши | 2 |
| `training/` | Обучение (LoRA, дообучение голоса) | 2 |

Всего 116 workflow (232 файлов). Откуда они:

- 92 — официальные шаблоны ComfyUI, для которых скачаны все модели;
- 20 — мои: SDXL, AnimeGen, Qwen Edit 2511 на fp8 и исправленные примеры аудио-нод (они же лежат в боковой панели ComfyUI);
- 3 — примеры из репозиториев нод (HeartMuLa, Qwen-TTS, VoxCPM). Ноды вывода текста из неустановленных паков заменены на встроенную `PreviewAny`;
- 1 — авторский workflow NetaYume с Tensor.Art, переключён на локальный чекпоинт.

Не вошли:

- официальные workflow Kandinsky 5 от Сбера: им нужны собственные ноды `Kandinsky5*`, а T2I, T2V и I2V уже есть во встроенных шаблонах;
- `differaser.json`: для DiffuEraser не хватает моделей, удалять объекты из видео лучше через `video-reference/VOID`.

## Как запустить API-копию

ComfyUI должен быть запущен: `cd ~/ai/comfyui && ./start_lowvram.sh`. Запрос идёт на локальный адрес, поэтому прокси не нужен:

```bash
cd ~/ai/workflows/image-photo/api
jq -n --slurpfile p "Z-Image-Turbo текст в изображение.json" '{prompt: $p[0]}' |
  curl --noproxy "*" -s -X POST http://127.0.0.1:8188/prompt -H "Content-Type: application/json" -d @-
# ответ: {"prompt_id": "..."}; статус: GET /history/<prompt_id>; файлы: /tmp/comfyui/output
```

На Python:

```python
import json, urllib.request
p = json.load(open("Z-Image-Turbo текст в изображение.json"))
# промпт: найди ноду CLIPTextEncode / TextEncode… и поменяй её inputs["text"]
req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=json.dumps({"prompt": p}).encode(),
                             headers={"Content-Type": "application/json"})
print(urllib.request.urlopen(req).read().decode())
```

**Входные файлы.** Картинки, видео и аудио, указанные в шаблонах, — примеры авторов, у тебя их нет. Положи свои файлы в папку input (`/tmp/comfyui/input` при запуске через `start_lowvram.sh`) или загрузи через `POST /upload/image`, а потом впиши имя файла в нужное поле API-копии (список полей ниже). В UI просто выбери файл в ноде Load Image / Load Audio / Load Video.

Примеры входов к официальным шаблонам: https://github.com/Comfy-Org/workflow_templates/tree/main/input

**Особые случаи:**

- `audio-tts/TTS - Qwen3-TTS save voice`: файл `designed_voice.wav` появится после шага 1 (сохранения голоса). До этого Load Speaker подсвечен красным.
- `training/Qwen3-TTS - дообучение голоса`: в UI-копии все ноды выключены, как в оригинале автора. В API-копии они включены, поэтому отправка сразу запустит обучение.
- `training/VoxCPM - обучение LoRA`: поправь пути к датасету и выходной папке (в примере автора пути Windows).

## Какие поля заменить в API-копиях

| Файл | Входы: нода.поле = имя файла в шаблоне |
|---|---|
| `3d/api/MoGe Оценка перспективной геометрии.json` | `LoadImage.image=modern_living_room.png` |
| `3d/api/Moge Панорама в Сетку.json` | `LoadImage.image=lego_street_panorama.png` |
| `audio-sound/api/Video to Audio - MMAudio.json` | `VHS_LoadVideo.video=CogVideoX_1_5_I2V_00092.mp4` |
| `audio-tts/api/TTS - Fish Audio S2 Pro.json` | `LoadAudio.audio=sample-2.mp3`, `LoadAudio.audio=sample-1.mp3` |
| `audio-tts/api/TTS - Qwen3-TTS (clone, design, custom).json` | `LoadAudio.audio=voice_sample.mp3` |
| `image-anime/api/Anima Lllite Любое управление к Изображению.json` | `LoadImage.image=wired_serenity_cyber_figure.png` |
| `image-anime/api/Anima Lllite Управление глубиной изображения.json` | `LoadImage.image=anima_depth_ref.png` |
| `image-edit/api/Anima Lllite Инпейнтинг изображения.json` | `LoadImage.image=goat_horned_spirit_girl.png` |
| `image-edit/api/Bernini-R Редактирование изображений.json` | `LoadImage.image=desert_oasis_backyard.png` |
| `image-edit/api/Flux Kontext Dev Редактирование изображения.json` | `LoadImage.image=flux_kontext_dev_basic_input_image.jpg` |
| `image-edit/api/Flux.2 Klein 4B - редактор изображений.json` | `LoadImage.image=robed_women.png` |
| `image-edit/api/Flux.2 Klein 4B Distilled - редактор изображений.json` | `LoadImage.image=handbag_white.png` |
| `image-edit/api/Mage-Flow-Edit Turbo Редактирование изображения.json` | `LoadImage.image=hot_air_balloons_rising.png` |
| `image-edit/api/Mage-Flow-Edit Редактирование изображения.json` | `LoadImage.image=calm_amid_ruin.png` |
| `image-edit/api/Qwen Edit 2509 - иллюстрация в реализм.json` | `LoadImage.image=robot_office_worker_in_space.png` |
| `image-edit/api/Qwen Edit 2509 - перенос освещения на портрет.json` | `LoadImage.image=woman_with_sunbeam.jpg`, `LoadImage.image=women_with_blue_orb.jpg` |
| `image-edit/api/Qwen Edit 2509 - переосвещение портрета (app).json` | `LoadImage.image=input_2-relight.png`, `LoadImage.image=input_1-relight.png` |
| `image-edit/api/Qwen Edit 2509 - переосвещение фото.json` | `LoadImage.image=warm_living_room.png` |
| `image-edit/api/Qwen Edit 2509 - ракурсы сцены одним кликом.json` | `LoadImage.image=comfy_billboard.png` |
| `image-edit/api/Qwen Edit 2509 - редактирование изображения.json` | `LoadImage.image=image_qwen_image_edit_2509_input_image.png` |
| `image-edit/api/Qwen Edit 2511 - INFL8 Inflation (fp8).json` | `LoadImage.image=inflation_lora_input.png` |
| `image-edit/api/Qwen Edit 2511 - Multiple Character Angles (fp8).json` | `LoadImage.image=character_input.png` |
| `image-edit/api/Qwen Edit 2511 - SYSTMS Action (fp8).json` | `LoadImage.image=western_rider.png` |
| `image-edit/api/Qwen Edit 2511 - замена материала.json` | `LoadImage.image=leather_sofa.png`, `LoadImage.image=texture_fur.png` |
| `image-photo/api/Krea-2 Int8 Референс стиля изображения.json` | `LoadImage.image=krea2_reference_image.png` |
| `image-photo/api/Qwen-Image 2512 Fun Union ControlNet.json` | `LoadImage.image=low_angle_shot.png` |
| `image-photo/api/Z-Image-Turbo контроль в изображение.json` | `LoadImage.image=image_z_image_turbo_fun_union_controlnet_input_image.png` |
| `llm/api/Qwen3-VL Генерация текста.json` | `LoadImage.image=example.png` |
| `llm/api/Qwen3.5 Генерация текста.json` | `LoadImage.image=man_with_red_hat.png` |
| `utility/api/BiRefNet Удаление фона.json` | `LoadImage.image=the_lily_veil.png` |
| `utility/api/Depth Anything 3 Оценка глубины видео.json` | `LoadVideo.file=empty_room_assembly.mp4` |
| `utility/api/Depth Anything 3 Оценка глубины изображения.json` | `LoadImage.image=retro_futuristic_home.png` |
| `utility/api/GAN-апскейлер видео (быстрый).json` | `LoadVideo.file=gan_input.mp4` |
| `utility/api/MoGe Оценка глубины.json` | `LoadImage.image=alien_world.png` |
| `utility/api/SAM3 Сегментация видео.json` | `LoadVideo.file=drinking_unicorn.mp4` |
| `utility/api/SAM3 Сегментация изображений.json` | `LoadImage.image=neon_guitarist.png` |
| `utility/api/SDPose-OOD Видео в карту поз.json` | `LoadVideo.file=man_in_the_rain.mp4` |
| `utility/api/SDPose-OOD Изображение в карту позы.json` | `LoadImage.image=dancer.png` |
| `utility/api/SeedVR2 3B Int8 Апскейл Видео.json` | `LoadVideo.file=grainy_perfume_shot_crf32.mp4` |
| `utility/api/SeedVR2 3B Int8 Масштабировать изображение.json` | `LoadImage.image=watch_macro_shot.png` |
| `utility/api/SeedVR2 7B Int8 Масштабировать изображение.json` | `LoadImage.image=indoor_portrait.png` |
| `utility/api/Upscale - SeedVR2 7B (видео).json` | `LoadVideo.file=grainy_perfume_shot_crf32.mp4` |
| `utility/api/Upscale - SeedVR2 7B Sharp fp16 (фото).json` | `LoadImage.image=indoor_portrait.png` |
| `utility/api/Upscale - Аниме hires-fix (Illustrious).json` | `LoadImage.image=example.png` |
| `utility/api/Upscale - Фото 4K (Z-Image + SeedVR2 7B).json` | `LoadImage.image=fighter_jet.png` |
| `utility/api/Апскейл изображения Z-Image-Turbo 2K.json` | `LoadImage.image=fighter_jet.png` |
| `utility/api/Апскейл изображения интерполяцией (без нейросети).json` | `LoadImage.image=pray.png` |
| `utility/api/Интерполяция кадров видео.json` | `LoadVideo.file=white_armored_warrior.mp4` |
| `utility/api/Основы - коррекция цвета.json` | `LoadImage.image=example.png` |
| `utility/api/Сшивание изображений в сетку 2x2.json` | `LoadImage.image=angle_1.png`, `LoadImage.image=angle_2.png`, `LoadImage.image=angle_3.png`, `LoadImage.image=angle_4.png` |
| `video-reference/api/Bernini-R Видеомонтаж.json` | `LoadVideo.file=vintage_field_style_look.mp4` |
| `video-reference/api/InfiniteTalk Полное озвучивание видео тела на основе аудио.json` | `LoadAudio.audio=audio_speaker1_woman.mp3`, `LoadImage.image=two_character_talking.png`, `LoadAudio.audio=audio_speaker2_man.mp3` |
| `video-reference/api/LTX 2.3 IC-LoRA Union Control.json` | `LoadVideo.file=stone_ruins.mp4`, `LoadImage.image=the_forgotten_gate.png` |
| `video-reference/api/LTX-2.3 IC-LoRA Управление опорным листом.json` | `LoadImage.image=german_shepherd_news_anchor_ref.png` |
| `video-reference/api/LTX-2.3 ID LoRA.json` | `LoadImage.image=vintage_thinker.png`, `LoadAudio.audio=ltx23_reference_audio.mp3` |
| `video-reference/api/MiniMax H3 Референс в видео.json` | `LoadImage.image=red_superboy_on_city_roof.png`, `LoadImage.image=mecha_dragon_lightning.png` |
| `video-reference/api/SCAIL-2 Int8 Замена персонажа.json` | `LoadImage.image=asian_model_in_white_clothes.png`, `LoadVideo.file=girl_eats_apple.mp4` |
| `video-reference/api/VOID Инпейнтинг видео.json` | `LoadVideo.file=snowboarder.mp4` |
| `video-reference/api/Wan Animate 2 Перенос движения.json` | `LoadImage.image=pink_hair_mech_arms_ref.png`, `LoadVideo.file=street_dance_drive.mp4` |
| `video-reference/api/Wan2.2-S2V Генерация Видео на Основе Аудио.json` | `LoadImage.image=video_wan2_2_14B_s2v_reference_image.jpg`, `LoadAudio.audio=video_wan2_2_14B_s2v_input_audio.MP3` |
| `video/api/AnimeGen-I2V (Wan 2.2).json` | `LoadImage.image=video_wan2_2_14B_i2v_input_image.jpg` |
| `video/api/Hunyuan Видео 1.5 изображение в видео.json` | `LoadImage.image=video_hunyuan_video_1.5_720p_i2v_input_image.png` |
| `video/api/Kandinsky 5.0 Видео Lite изображение в видео.json` | `LoadImage.image=crystal_flower.png` |
| `video/api/LTX-2.3 FLF2V.json` | `LoadImage.image=high_view_classic_car.png`, `LoadImage.image=low_view_classic_car.png` |
| `video/api/LTX-2.3 Изображение и аудио в видео.json` | `LoadImage.image=cactus_man.png`, `LoadAudio.audio=ltx_23_audio.mp3` |
| `video/api/LTX-2.3 изображение в видео.json` | `LoadImage.image=egyptian_queen.png` |
| `video/api/MiniMax H3 изображение в видео.json` | `LoadImage.image=transparent_rgb_gaming_mouse.png` |
| `video/api/MiniMax H3 продолжение видео.json` | `LoadImage.image=transparent_rgb_gaming_mouse.png` |
| `video/api/Wan 2.2 14B Первый-Последний кадр в Видео.json` | `LoadImage.image=video_wan2_2_14B_flf2v_start_image.png`, `LoadImage.image=video_wan2_2_14B_flf2v_end_image.png` |
| `video/api/Wan 2.2 14B изображение в видео.json` | `LoadImage.image=video_wan2_2_14B_i2v_input_image.jpg` |
| `video/api/Wan 2.2 14B ключевые кадры (склейка FLF-сегментов).json` | `LoadImage.image=6-key-frames-1.jpg`, `LoadImage.image=6-key-frames-2.png`, `LoadImage.image=6-key-frames-3.png`, `LoadImage.image=6-key-frames-4.png`, `LoadImage.image=6-key-frames-5.png`, `LoadImage.image=6-key-frames-6.png` |
| `video/api/Стилевой переход LTX-2.3.json` | `LoadImage.image=ltx23_flf2v_last_frame.png`, `LoadImage.image=ltx23_flf2v_first_frame.png` |

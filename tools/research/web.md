# Web research notes (сырые, для таблицы)

## Z-Image Turbo (6B, distilled, Tongyi)
- Prompt: проза, не теги (обучена на натур. подписях EN/ZH). Структура: субъект, сцена, композиция, свет, стиль, ограничения. Свет — главный рычаг. Камера/объектив/плёнка → документальный реализм; "realistic/8K/beautiful" почти ничего не дают. Главное и текст для рендера — в начало (внимание падает к ~512 токенам). 8 шагов (4 — черновик), CFG не трогать (1.0, distilled), negative почти не работает → ограничения в основной промпт.
- Сильные: скорость, фотореализм, следование инструкциям, текст EN/ZH (вывески, постеры).
- Слабые: меньше мелкой детализации, чем у крупных моделей; дефолтный «глянцевый стоковый» вид лиц без указания камеры/плёнки; при 40 шагах — сеточные артефакты.
- Src: https://deapi.ai/blog/z-image-turbo-prompting-guide-formula-tips-and-5-example-prompts ; https://fliki.ai/blog/z-image-turbo-prompting-guide ; https://learn.rundiffusion.com/z-image-turbo-rundiffusion

## Qwen-Image 2512 (20B MMDiT)
- Сильные (карточка): заметно меньше «AI-вида», реализм людей, натуральные текстуры, лучший текст и вёрстка (особенно китайский и английский), 10k+ слепых сравнений AI Arena.
- Prompt: субъект в начало; подробные описания позы работают («body leaning slightly forward»); для текста 35+ шагов; CFG 4–7 (fal), Comfy-шаблон 50 шагов/CFG 4 или 4-step/2-step LoRA.
- Разрешения: 1328², 1664×928, 928×1664, 1472×1104, 1584×1056.
- Src: https://fal.ai/learn/devs/qwen-image-2512-text-to-image-prompt-guide ; https://docs.krea.ai/user-guide/features/qwen2512 ; https://replicate.com/qwen/qwen-image-2512

## Flux.1 Krea Dev (12B)
- «Opinionated» эстетика, без пересвеченного AI-лука, фотореализм; разнообразнее лица, чем у Flux dev (нет «flux chin», глянцевой кожи). Совместим с экосистемой Flux.1 dev LoRA.
- Prompt: естественный язык, короче и образнее; guidance ~3.5–4.5 (FluxGuidance), 20–30 шагов. Слабые: следование промпту сильно зависит от стиля промпта; "white background" может давать размытость; нет negative (guidance-distilled). Лицензия FLUX.1 dev non-commercial.
- Src: https://bfl.ai/blog/flux-1-krea-dev ; https://blog.fal.ai/introducing-the-flux-1-krea-dev-on-fal ; https://blog.segmind.com/flux-prompting-guide-image-creation/

## Chroma1-HD (8.9B, на базе Flux.1 schnell, Apache 2.0)
- Prompt: проза (субъект, место, стиль+палитра, свет, композиция), очень короткие промпты хуже; без весов (word:1.4); negative работает (CFG>1): "low quality, blurry, deformed, flat colors…"; 40 шагов, CFG 3–4; понимает и danbooru-теги частично. Без цензуры, широкий диапазон стилей.
- Src: https://huggingface.co/docs/diffusers/main/api/pipelines/chroma ; https://civitai.com/ecosystems/chroma

## Krea-2 Turbo (12B DiT, июнь 2026)
- Distilled из Raw, 8 шагов, нативно до 2K; LoRA тренировать на Raw, гонять на Turbo; 9 стилевых LoRA в шаблоне с триггерами. Встроенный prompt enhance (Qwen) в шаблоне. Лицензия community (бесплатно коммерчески для небольших команд). 2-е место среди независимых лаб на Artificial Analysis (самоотчёт).
- Src: https://comfyui-wiki.com/en/news/2026-06-22-krea-2-open-source-text-to-image ; https://www.krea.ai/krea-2-open-source ; https://gigazine.net/gsc_news/en/20260624-krea-2-raw-turbo/

## Ideogram 4 (9.3B, open weights, июнь 2026)
- Обучен на структурированных JSON-подписях: scene summary, style block, background, объекты с bbox и hex-палитрами. JSON надёжнее прозы; есть шаблон для LLM («Ideogram4 Caption Prompt Template»). Нет отдельного negative (асимметричный CFG). Встроенный safety-фильтр (на прозе больше ложных срабатываний). Текст-энкодер Qwen3-VL-8B. Нативно 2K. Сильное: типографика, постеры, вёрстка.
- Src: https://ideogram.ai/blog/ideogram-4-json-prompting/ ; https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui ; https://docs.comfy.org/tutorials/image/ideogram/ideogram-v4

## Mage-Flow / Turbo / Edit (Microsoft, 4B, июль 2026, MIT)
- GenEval 0.90 (выше FLUX.2-dev 32B и Qwen-Image 20B — самоотчёт), LongText-EN 0.944 / CN 0.823 — сильный текст. Turbo: 4 шага, CFG 1, 0.59 с/1024² на A100, GenEval 0.88. Mage-VAE 16×. Нативное разрешение 512–2048, кратно 16, до 4:1. Промпт по-английски; negative опционально (не для Turbo). Edit: «сначала что сохранить, потом что поменять», 1–3 референса.
- Слабые: независимых обзоров мало; качество за пределами 2048 падает.
- Src: https://aiweekly.co/alerts/microsoft-ships-mage-flow-4b-claims-geneval-lead-on-flux2 ; https://huggingface.co/papers/2607.19064 ; https://github.com/microsoft/Mage

## Kandinsky 5.0 Image Lite (6B, Sber AI, MIT)
- Понимает русский и английский (энкодер Qwen2.5-VL-7B + CLIP-L), культурный контекст РФ. Шаблон ComfyUI.
- Src: https://comfy.org/workflows/image_kandinsky5_t2i-4d989a34d147/ ; https://github.com/kandinskylab/kandinsky-5

## Flux.2 Klein 4B (BFL, Apache 2.0)
- t2i + редактирование до 4 референсов, ~8–13 ГБ VRAM; 9B лучше, но некоммерческий/gated. Нет prompt upsampling → промпт явный. Edit: «что сохранить + что поменять»; референсы одного стиля (не мешать акварель/фото/3D). Distilled: 4 шага, CFG 1; base: ~50 шагов, CFG 4–5.
- Src: https://blog.comfy.org/p/flux2-klein-4b-fast-local-image-editing ; https://help.bfl.ai/articles/8642316687-flux-2-klein-fast-generation-guide ; https://fal.ai/learn/devs/flux-2-klein-user-guide

## Z-Image (base, non-distilled)
- 28–50 шагов, CFG 3–5 (4), negative работает; база для LoRA; разнообразнее стили; LoRA Turbo ≠ Base. LoRA strength ~1 (артефакты >1.3).
- Src: https://huggingface.co/Tongyi-MAI/Z-Image ; https://comfyui-wiki.com/en/news/2026-01-28-alibaba-z-image-base-release

## RealVisXL V5 (SDXL)
- DPM++ SDE Karras 30+ шагов или DPM++ 2M Karras 50+; CFG ~4–7; negative: bad hands, bad anatomy, ugly, deformed, (face asymmetry, eyes asymmetry…); hires fix 1.1–1.5×, denoise 0.1–0.3, 4x-UltraSharp. Clip skip 1.
- Src: https://huggingface.co/SG161222/RealVisXL_V5.0

## Juggernaut XL v9 (RunDiffusion Photo v2)
- 832×1216, 30–40 шагов, CFG 3–7 (ниже — реалистичнее), DPM++ 2M Karras; промпт ≤75 токенов, «cinematic, skin texture, shallow depth of field…».
- Src: https://huggingface.co/RunDiffusion/Juggernaut-XL-v9 ; https://www.rundiffusion.com/prompting/prompting-guide-for-juggernaut-x

## Anima base v1 (2B, CircleStone Labs + Comfy Org, non-commercial)
- Аниме-концепты/персонажи/стили, неплохо иной не-фото арт; фотореализм плохо. Данные: миллионы аниме + ~800k арт, без синтетики. Промпт: ≥2 предложений; теги и проза вперемешку; качество/художник в начале; персонаж: имя + описание внешности (голые имена путают, особенно несколько персонажей). Base — для гибкости/LoRA; есть Aesthetic и Turbo (8–12 шагов, CFG1). LLLite-контроль (canny/depth/inpaint) в шаблонах.
- Src: https://huggingface.co/circlestone-labs/Anima ; https://comfyui-wiki.com/en/models/anima

## NetaYume Lumina v3.5 (Lumina-Image-2.0 2.6B + Gemma-2B энкодер)
- Системный промпт-префикс обязателен (в шаблоне фиксированная часть до «Prompt Start»); danbooru-теги + натуральный язык, многоязычный; @artist для художников. CFG 4–5.5, 30–50 шагов, Euler a/normal или res_multistep/linear_quadratic, ≥1024², лучше 1024×1024 (пробовать 1024×1536). Сильное: аниме, персонажи danbooru, детали аксессуаров/одежды.
- Src: https://huggingface.co/duongve/NetaYume-Lumina-Image-2.0 ; https://civarchive.com/articles/16274/neta-lumina-drawing-model-prompt-guide

## NewBie-image Exp0.1 (3.5B Next-DiT, Gemma3-4B + Jina CLIP v2, VAE Flux, non-commercial newbie-nc-1.0)
- XML-структурированные промпты (<character_1><n>…</n><appearance>…</appearance>…</character_1><general_tags>…) с danbooru-тегами внутри → точнее в многоперсонажных сценах; поддерживает и прозу/теги.
- Src: https://docs.comfy.org/tutorials/image/newbie-image/newbie-image-exp-0-1 ; https://comfyui-wiki.com/en/models/newbie/newbie-image-exp0-1

## Illustrious-XL v2.0 (SDXL)
- 512–1536, кратно 32, до 1:10; в широких кадрах (1344×768, 1536²) склонен дублировать субъект → квадрат/вертикаль. Euler a, 20–30 шагов, CFG ~5–7. Теги danbooru + натуральный язык, теги качества в начале. Лучшая совместимость с LoRA «Illustrious».
- Src: https://huggingface.co/OnomaAIResearch/Illustrious-XL-v2.0 ; https://huggingface.co/SceneWorks/illustrious-xl-v2-mlx

## NoobAI-XL 1.1 eps / V-pred 1.0 (SDXL, danbooru+e621)
- eps: CFG 5–6, 25–30 шагов, Euler a. V-pred: CFG 4–5 (3.5–5.5), 28–35 шагов, Euler (другие сэмплеры могут ломать), ModelSamplingDiscrete v_prediction+zsnr, RescaleCFG 0.7 при пережоге. Теги: masterpiece, best quality, newest, absurdres, highres, safe. Огромный охват персонажей/художников. v-pred: шире динамический диапазон, глубокие тени/чёрный.
- Src: https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0 ; https://anifusion.ai/models/noobai-xl-epsilon-1-1/

## Animagine XL 4.0 (SDXL, Cagliostro)
- Порядок тегов: 1girl/1boy → имя персонажа → серия → rating → прочее → в конце качество: masterpiece, high score, great score, absurdres (score-теги сильнее). Negative: lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry. CFG 4–7 (5), 25–28 шагов, Euler a. 1024², 832×1216, 1216×832.
- Src: https://huggingface.co/cagliostrolab/animagine-xl-4.0

## Qwen Image Edit 2511 (20B, fp8mixed)
- vs 2509: меньше дрейфа (не трогает неотредактированные области), сильнее консистентность персонажа, встроенные «LoRA-эффекты» (ракурсы, свет), промышленный дизайн, геометрия, групповые фото из 2 людей. Офиц.: true_cfg 4, 40 шагов; Comfy 20 шагов/CFG4; Lightning 4 шага/CFG1. Промпт: сцена с позициями субъектов («X слева, Y справа»), что менять + что сохранить; до 3 изображений.
- Src: https://huggingface.co/Qwen/Qwen-Image-Edit-2511 ; https://docs.sglang.io/cookbook/diffusion/Qwen-Image/Qwen-Image-Edit

## Qwen Image Edit 2509
- Мульти-изображения 1–3 (person+person, person+product, person+scene); в промпте явно Image 1/2/3 и роли; краткие инструкции «ограничения сначала». ControlNet-подобный ввод (поза/глубина/канни) встроен. Слабее 2511 по дрейфу/консистентности.
- Src: https://huggingface.co/Qwen/Qwen-Image-Edit-2509 ; https://www.runcomfy.com/comfyui-workflows/qwen-image-edit-2509-in-comfyui-multi-image-merge-edit

## Flux.1 Kontext dev (12B, non-commercial)
- Техники (из шаблона): конкретика, «change/replace» вместо «transform», явно что сохранить, по шагам; текст в кавычках. Слабые: многошаговое редактирование копит артефакты и дрейф лица (6 правок — заметно), иногда игнорирует требования, ограниченные знания о мире, артефакты дистилляции.
- Src: https://arxiv.org/pdf/2506.15742 ; https://bfl.ai/announcements/flux-1-kontext

## Bernini-R (ByteDance, 14B Wan 2.2 renderer, Apache-2.0)
- Рендерер без MLLM-планировщика; задачи через системный префикс: t2i, i2i edit, r2i, v2v, mv2v, rv2v (смена образа), r2v, ads2v (вставка видео). Промпт EN: что меняем + что неизменно; image0/image1… для референсов; до ~5 референсов надёжно. Turbo (LightX2V, 6 шагов, CFG1) — превью; финал 40 шагов CFG5. Внутр. арена ByteDance: «первый эшелон» (самоотчёт). 848×480/832×480, 81 кадр @16fps (4n+1).
- Src: https://docs.comfy.org/tutorials/video/bytedance/bernini-r ; https://comfyui-wiki.com/en/models/bernini/bernini-r ; https://github.com/bytedance/Bernini

## Wan 2.2 14B (A14B MoE high/low noise, Apache-2.0)
- Порядок: субъект → действие → окружение → камера → свет → стиль → движение. В I2V описывать движение, а не то, что уже на картинке. Не перегружать движениями камеры (первое побеждает). Свет/грейд: volumetric dusk, neon rim light, teal-and-orange, Kodak Portra, anamorphic bokeh, 16mm grain. ≤5 с, 16 fps (81 кадр), до 1280×720. Слабые: сложные взаимодействия нескольких субъектов, экстремальные трансформации; без указаний движения — статика/морфинг. Lightning LoRA (4 шага) снижает динамику. Negative — китайский дефолт.
- Бенч (шаблон Comfy): RTX 4090D, 640×640×81: 20 шагов ≈513 с, 4 шага Lightning ≈71 с (2-й запуск).
- Src: https://www.instasd.com/post/wan2-2-whats-new-and-how-to-write-killer-prompts ; https://help.scenario.com/articles/9790083883-wan-2-2-the-essentials ; https://www.veed.io/learn/wan-2-2-prompting-guide ; https://aistudynow.com/how-to-write-better-wan-2-2-prompts-tested-in-comfyui/

## LTX-2.3 (22B, видео+аудио)
- Один связный абзац в настоящем времени: главное действие → детали движения → персонаж/место → камера → свет; ≤200 слов; описывать звук/диалоги (речь в кавычках), пространственные указания (слева/справа) соблюдаются. Размеры кратны 32, кадры 8n+1. Слабые (карточка): не всегда точно следует промпту, зависит от стиля промпта; аудио без речи бывает хуже. Шаблон: 2-ступенчато (половинное разрешение → апскейл латента x2), distilled LoRA.
- Src: https://ltx.io/blog/how-to-improve-ltx-2-3-prompt-adherence ; https://deapi.ai/blog/ltx-2-3-video-generation-guide ; https://ltxworkflow.com/resources/tutorials/ltx-23-prompting-guide ; https://huggingface.co/Lightricks/LTX-2.3

## MiniMax H3 (open weights 3 авг 2026; fl2va и ref2va; видео+стерео-аудио одним проходом)
- t2v/i2v/первый-последний кадр/референсы (до 9 картинок, 3 видео, 3 аудио; теги <Picture 1>, <Video 1>, <Audio 1> в порядке подключения). 4–15 с @24fps, нативно 768p (до 1344×768), 2K — под вопросом локально. Промпт: шоты, движения камеры, и звук (диалоги, SFX, музыка) одним блоком; шаблон-пример: стиль/настроение → Timeline [0s-1s]… → правила монтажа → Audio. Эмбеддинги стиля (embedding:minimaxh3_…). ref2va очень чувствителен к формулировкам, точно ссылаться на теги. Сэмплер res_multistep, beta/normal. Турбо-LoRA 8 шагов (fl2v) и 4 шага (ref2v).
- Слабые: заявки про 3060/2K не подтверждены независимо; Qwen3-VL-32B энкодер тяжёлый (15.7 ГБ nvfp4).
- Пользователь: предел ~25 с при 0.4 МП на пустой машине без zram.
- Src: https://blog.comfy.org/p/minimax-h3-day-0-support-in-comfyui ; https://comfyui-wiki.com/en/news/2026-08-03-minimax-h3-open-weights-comfyui ; https://runtimewire.com/article/minimax-h3-open-video-benchmark-lead

## HunyuanVideo 1.5 (8.3B, Tencent Hunyuan Community License)
- Длинные подробные промпты значительно улучшают результат; официальный rewrite (Gemini/vLLM) — t2v/i2v системные промпты; EN/ZH, не смешивать языки в одном промпте. Порядок: субъект, окружение, движение, камера. Офиц. 50 шагов, CFG 6, shift 7 (720p i2v)/9 (720p t2v); шаблон 20 шагов. 121 кадр @24fps. SR до 1080p отдельной моделью. Лицензия не действует в ЕС/UK/Юж. Корее.
- Src: https://huggingface.co/tencent/HunyuanVideo-1.5 ; https://www.runcomfy.com/models/tencent/hunyuan-video-v1.5/text-to-video

## Kandinsky 5.0 Video Lite (2B, MIT)
- 768×512, 24 fps, 5 с (121 кадр) или 10 с (241, размеры кратны 128); RU+EN, «понимание российской культуры»; Сбер: лучше Wan 2.1 14B / Wan 2.2 5B (внутр. тесты). 12 ГБ потребительские карты.
- Src: https://ppc.world/news/vyshla-novaya-lineyka-modeley-kandinsky-50-dlya-generacii-vizuala-v-vysokom-kachestve/ ; https://github.com/kandinskylab/kandinsky-5

## Wan 2.2 TI2V 5B (dense, VAE 16×16×4, Apache-2.0)
- 720p@24fps, T2V+I2V в одной модели; ниже качество чем 14B, но быстрее, влезает в 8–12 ГБ без квантования. RTX 4090: ~9 мин на 5 с 720p (20–30 шагов, блог).
- Src: https://wan27.org/blog/wan-2-2-5b-vs-14b-vs-rapid-all-in-one ; https://evezone.evetech.co.za/daily-drop/wan-2-2-hits-local-rigs-720p-video-on-24gb-of-vram

## AnimeGen-I2V (AIdeaLab, июль 2026, Apache-2.0, файнтюн Wan 2.2 I2V A14B)
- Лучше аниме-движение, отрисовка персонажей, цвет, консистентность. Промпт — короткое действие простым языком (карточка), «Japanese anime style» в начале (мой шаблон по карточке), 832×480, shift 3, 4 шага с Lightning.
- Src: https://huggingface.co/aidealab/AnimeGen-I2V ; https://ai-revolution.co.jp/media/what-is-animegen/

## Wan Animate 2 (Alibaba, 7 авг 2026, Apache-2.0)
- Референс (кто) + управляющее видео (движение) без извлечения позы; идентичность; фон и камера — из текста. text_1: внешность + фон (без движения), text_2: движение. 81 кадр за сегмент, цепочка сегментов вручную. Главная причина брака — несовпадение крупности (close-up vs full body). Кэш WanAnimate2Cache на CPU против пиков VRAM.
- Src: https://docs.comfy.org/tutorials/video/wan/wan-animate-2 ; https://huggingface.co/Wan-AI/Wan-Animate-2-14B ; https://comfyui-wiki.com/en/news/2026-08-07-wan-animate-2

## SCAIL-2 (Zhipu zai-org, на Wan 2.1 14B, int8; MIT/Apache)
- Замена персонажа в видео / анимация персонажа по позе. Промпт описывает ИТОГОВОЕ видео (не инструкцию), включая одежду заменяющего персонажа и предметы рядом. Размеры кратны 32; 512p/704p, замена лучше на 704p. Сегменты по 81 кадр (перекрытие 5), продление — вручную. Маски SAM3 важны (без масок анимация ведёт себя как замена).
- Слабые: сложное движение и длинные видео — качество падает, «якорение» ослабевает.
- Src: https://huggingface.co/zai-org/SCAIL-2 ; https://arxiv.org/pdf/2606.10804 ; https://docs.comfy.org/tutorials/video/zai/scail2

## Wan 2.2 S2V (14B, аудио→видео)
- Картинка + аудио + текст → говорящее/поющее видео; губы, мимика, движение под звук. Чанки по 77 кадров (минимум 73), продление копированием подграфа. Lightning 4 шага CFG1 или 20 шагов CFG6. Хак против пережжённого первого кадра в шаблоне. Промпт: описать сцену/эмоцию/камеру.
- Src: https://comfyui-wiki.com/en/tutorial/advanced/video/wan2.2/wan2-2-s2v ; https://wan27.org/blog/wan-2-2-s2v-explained

## InfiniteTalk (MeiGen, на Wan 2.1 14B I2V)
- Дубляж «sparse-frame»: держит идентичность, жесты, камеру по опорным кадрам, анимирует губы/голову/тело под новое аудио; неограниченная длина цепочкой сегментов (по 81 кадр@25fps=3.24 с). Лип-синк 1.11 vs LatentSync 2.32 / MuseTalk 2.57 (человеч. оценка, самоотчёт). Пиксельно дальше от исходника, чем классические липсинки (генерирует движение). Два персонажа — маски в MaskEditor.
- Src: https://arxiv.org/pdf/2508.14033 ; https://www.themoonlight.io/en/review/infinitetalk-audio-driven-video-generation-for-sparse-frame-video-dubbing

## VOID (Netflix, CogVideoX-Fun 5B InP, Apache-2.0, ECCV 2026)
- Удаляет объект И его физическое влияние (тень, падающие предметы); quadmask; 2 прохода (2-й — стабильность на длинных клипах). Оригинал требует 40 ГБ+ VRAM — в ComfyUI оптимизировано, 672×384×45 по умолчанию. Позитивный промпт = описание результата («empty kitchen counter…»), SAM3-фраза = что удалить. 64.8% предпочтений против 18.4% Runway (самоотчёт). Слабые: плохие маски, хаотичное движение, объект на весь кадр.
- Src: https://github.com/netflix/void-model ; https://comfyui-wiki.com/en/models/void/void ; https://eu.36kr.com/en/p/3756719276835586

## SeedVR2 (ByteDance, 3B/7B int8, one-step restoration/upscale, Apache-2.0)
- 1 шаг, без швов тайлов (оконное внимание). 7B качественнее, медленнее/тяжелее; 3B быстрее. Обучен до 121 кадра/720p в оригинале. Слабые: тяжёлая деградация, мелкое движение в AI-клипах → пересвет/переобострение; размытие в движении, сильная темнота; на чистом видео переобостряет. 7B иногда вертикальные полосы. Длинные видео — резать (trim) по сегментам.
- Src: https://docs.comfy.org/tutorials/utility/seedvr2 ; https://replicate.com/zsxkib/seedvr2/readme ; https://www.runcomfy.com/models/community/seedvr2/upscale/video

## ACE-Step 1.5 XL (4B; Turbo 8 шагов без CFG; SFT — качественнее)
- Tags: жанр, инструменты, энергия, тип вокала, BPM, язык вокала («russian vocal»); конкретика лучше «chill music». Lyrics: [verse]/[chorus]/[bridge]/[instrumental], 6–10 слогов в строке, пустые строки между секциями, бэк-вокал в скобках; инструментал — [inst] + «no vocals» в тегах; ~2048 токенов на текст. Коммерчески пригодно (по описанию шаблона).
- Src: https://deapi.ai/blog/ace-step-1-5-prompting-guide-how-to-write-tags-structure-lyrics-and-generate-better-music ; https://huggingface.co/docs/diffusers/v0.39.0/api/pipelines/ace_step ; https://deepinfra.com/ACE-Step/acestep-v15-xl-sft

## MiniMax Music 3 (на Qwen3-8B, песни до ~5 мин; лицензия спорная: CC BY-NC 4.0 / Community — некоммерч.)
- Caption в 3 частях: Global Metadata (жанр, темп «126 BPM», тональность «B-flat major», настроение) → Vocal Details (тембр, подача, эффекты) → Arrangement (инструменты, где вступают/уходят, продакшн). Lyrics: точный текст + теги [intro][verse][chorus][bridge][outro] — только теги управляют структурой. max_duration до ~300 с; тайловый декод для 12 ГБ. Офиц. Caption Rewriter Skill (github MiniMax-AI/MiniMax-Music3).
- Сильные: структура песни (возвращающиеся припевы, бриджи), стабильное качество на минутах (по демо). Независимых тестов нет.
- Src: https://docs.comfy.org/tutorials/audio/minimax/minimax-music-3 ; https://www.instasd.com/post/minimax-music-3-comfyui-guide ; https://mer.vin/news/minimax-music-3-is-open-weight-but-not-open-for-business/

## Stable Audio 3 Medium (1.4B DiT, до ~380 с, стерео, лицензированные данные; Stability Community License)
- Музыка, инструменты, SFX, one-shot. Шаблон: короткая идея → reprompt Qwen по категории (Music/Instrument/SFX/One-shot) → генерация. Без reprompt — полный промпт (жанр, инструменты, BPM, настроение, длина). CFG ~7 для base.
- Слабые: вокал/речь не цель модели; независимых оценок нет.
- Src: https://docs.comfy.org/tutorials/audio/stable-audio/stable-audio-3 ; https://comfyui-wiki.com/en/models/stable-audio/stable-audio-3 ; https://fal.ai/models/fal-ai/stable-audio-3/medium/text-to-audio/api

## HeartMuLa 3B (Apache-2.0; LM 3B + HeartCodec + транскриптор)
- Lyrics с секциями [Intro][Verse][Prechorus][Chorus][Bridge] (именно [Prechorus]); tags через запятую (жанр, настроение, инструменты). Теги могут игнорироваться (issue #90), текст доминирует → экспериментировать с порядком тегов. HeartCodec только fp32 (bf16 портит звук). ≥8 ГБ VRAM с ленивой загрузкой, 16+ комфортно → у нас патч (по очереди на GPU).
- Src: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/creative/creative-heartmula ; https://huggingface.co/spaces/Heartsync/HeartMuLa ; arXiv 2601.10547

## Fish Audio S2 Pro (fp8; Fish Audio Research License — некоммерч.)
- Инлайн-теги эмоций в []: [excited], [angry], [sad], [whisper in small voice], [professional broadcast tone] — свободная форма. Клон: 10–30 с чистой речи + точный текст. Русский — Tier 2 (EN/ZH/JA — Tier 1). 81.88% побед над gpt-4o-mini-tts (EmergentTTS-Eval, самоотчёт). Мультиспикер [speaker_1]: …
- Src: https://github.com/Saganaki22/ComfyUI-FishAudioS2 ; https://cookbook.sglang.io/omni/S2-Pro ; https://www.gradually.ai/en/ai-models/fish-audio-s2-pro/

## Qwen3-TTS 1.7B (Apache-2.0; Base/CustomVoice/VoiceDesign, 10 языков вкл. русский)
- VoiceDesign: голос из описания (пол, возраст, тембр, эмоция, темп) — описание по-английски; CustomVoice: 9 тембров + instruct стиль; Base: клон за 3 с образца (нужен точный текст, либо x_vector_only). «Design once → reuse» через сохранение голоса. Русские ударения/интонации — независимых оценок нет (Habr-обзор есть).
- Src: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign ; https://habr.com/ru/articles/989244/

## VoxCPM2 (2B, MiniCPM-4, 30 языков, 48 кГц; Apache-2.0)
- Без токенизатора; voice design из текста (пол, возраст, тон, эмоция, темп), клон по 16 кГц образцу (точный транскрипт обязателен, 5–15 с), выход 48 кГц. RTF ~0.30 на RTX 4090, ~8 ГБ VRAM. Слабее WER в некоторых языках.
- Src: https://pypi.org/project/voxcpm ; https://huggingface.co/openbmb/VoxCPM2 ; https://wikidocs.net/blog/@jaehong/11880/

## Chatterbox Multilingual v3 (Resemble AI, 23 языка вкл. ru, MIT)
- Дефолт exaggeration 0.5, cfg_weight 0.5. Быстрый референс → cfg_weight ~0.3. Референс на другом языке → cfg_weight 0 (убирает акцент). Драма: exaggeration ≥0.7 + cfg_weight ~0.3 (высокая exaggeration ускоряет речь). Референс чистый и на том же языке, что language_id. Ударения/диакритика помогают произношению.
- Src: https://github.com/travisvn/chatterbox-multilingual ; https://huggingface.co/ResembleAI/chatterbox ; https://www.mintlify.com/yocxy2/chatterboxyocxy/models/chatterbox-multilingual

## MMAudio large 44k v2 (CVPR 2025, Sony/UIUC; веса CC-BY-NC)
- Видео (+текст) → звук 44.1 кГц, синхронизация по Synchformer; обучен на ~8 с клипах (дольше — хуже); разрешение >384 px по короткой стороне не улучшает, только медленнее. Промпт короткий: источник звука + материал/место; negative поддерживается.
- Src: https://github.com/hkchengrex/MMAudio ; https://huggingface.co/hkchengrex/MMAudio ; arXiv 2412.15322

## HunyuanVideo-Foley (Tencent, 48 кГц VAE; research/non-commercial)
- Текст опционален (базовый проход по видео), короткие подсказки о пространстве, дистанции, материале. Лимит ноды 450 кадров (~15 с @30fps) → резать на 15-с сегменты. BlockSwap в шаблоне для 12 ГБ. Сильное: SFX, синхронность, качество 48 кГц; музыка/речь не цель.
- Src: https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley ; https://studio.aifilms.ai/blog/hunyuanvideo-foley ; https://replicate.com/tencent/hunyuanvideo-foley

## SAM 3 (Meta, концептная сегментация)
- Промпт — короткая именная группа («yellow school bus»), ≤32 токена; несколько объектов через запятую, лимит «:N» (eye:2, window panels:4). Не поддерживает сложные запросы/референсные выражения («человек слева от машины»); в видео стоимость растёт с числом объектов; ниши — дообучение.
- Src: https://arxiv.org/pdf/2511.16719 ; https://docs.comfy.org/tutorials/utility/video-segment-sam3

## SDPose-OOD (+RT-DETRv4, нативно в ComfyUI)
- Поза (wholebody 133 точки: тело, лицо, руки), мульти-персона, OOD — нефотографические/стилизованные изображения; image → поза и video → карта поз (для контроля Wan/LTX/SCAIL).
- Src: https://docs.comfy.org/tutorials/utility/pose-detection-sdpose

## Qwen3.5 4B (Apache-2.0, 262K контекст, vision, thinking по умолчанию)
- Лучший <5B по Artificial Analysis (27). Для ComfyUI — расширение/перевод промптов, подписи картинок (VL), локально. Thinking отключать для чистого вывода.
- Src: https://artificialanalysis.ai/articles/qwen3-5-small-models ; https://localclaw.io/models/qwen3.5-4b

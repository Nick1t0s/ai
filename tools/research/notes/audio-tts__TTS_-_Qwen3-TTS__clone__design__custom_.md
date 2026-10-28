## Qwen3-TTS 1.7B

- **Voice Design** — голос по описанию в `instruct` (описание лучше писать по-английски), текст — по-русски, `language` = Russian.
- **Custom Voice** — 9 готовых голосов (`speaker`), эмоция и манера — в `instruct`.
- **Voice Clone** — загрузи в LoadAudio образец 3–30 с и впиши его **точный текст** в `ref_text` (или включи `x_vector_only`: текст не нужен, но сходство хуже).

Ветки независимы: без образца голоса Voice Design и Custom Voice всё равно отработают. Модели: `models/qwen-tts/`.
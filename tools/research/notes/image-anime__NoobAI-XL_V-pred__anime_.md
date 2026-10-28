## NoobAI-XL V-pred 1.0 (аниме, SDXL)

- Модель: `checkpoints/NoobAI-XL-Vpred-v1.0.safetensors`
- Обязателен узел **ModelSamplingDiscrete: v_prediction + zsnr** (уже стоит).
- Euler, 28–35 шагов, CFG 3.5–5.5, scheduler normal. Если цвета «пережжены» — добавьте RescaleCFG 0.7.
- Промпт: теги Danbooru; в начале `masterpiece, best quality, newest, absurdres, highres`.
- Разрешения ~1 МП: 832×1216, 1216×832, 1024×1024.
- LoRA для Illustrious/NoobAI (Civitai) подключаются через LoraLoader между чекпоинтом и ModelSamplingDiscrete.
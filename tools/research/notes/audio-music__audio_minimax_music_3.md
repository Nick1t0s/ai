## MiniMax Music 3

A music generation model by MiniMax that creates complete songs up to 5 minutes long with stable structure and high audio quality. Two inputs drive it: **Caption** (structured music description: style, mood, vocals, arrangement) and **Lyrics** (with `[intro]` `[verse]` `[chorus]` `[bridge]` `[outro]` tags controlling song structure).

### Parameters

| Parameter | Description |
|---|---|
| Caption | Music description. Write it in three sections — Global Metadata → Vocal Details → Arrangement. The more specific, the closer the result. |
| Lyrics | Song lyrics + section tags. Tags are the only executable structural instructions; the lyric text itself only conveys mood. |
| max_duration | Target song length in seconds (default 120 = 2 minutes; the model supports up to ~300 s / 5 minutes). Longer songs take more time and VRAM. |
| seed | Random seed for the generation. Keep it fixed to reproduce the same song; change it to get a different take. |
| Model files | diffusion model / text encoder / VAE.|
| Tiled decode | Decode the audio VAE in overlapping tiles to drastically cut VRAM usage — helpful for long songs on low-VRAM GPUs. Slightly slower, with a small risk of seams at tile boundaries; turn it off on high-VRAM GPUs for the best quality. |

### Prompt Writing Guide

You can find an official [Music Caption Rewriter Skill here](https://github.com/MiniMax-AI/MiniMax-Music3)

---

## Model Links

**diffusion_models**

**text_encoders**


**vae**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   ├── 📂 text_encoders/
│   └── 📂 vae/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)
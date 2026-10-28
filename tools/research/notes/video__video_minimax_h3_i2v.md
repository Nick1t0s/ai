## MiniMax H3

[MiniMax H3](https://www.minimax.io/blog/minimax-h3) is MiniMax's general-purpose, omni-modal generation model. It jointly understands text, image, video, and audio, and generates video with **native stereo audio**: voice, sound effects, and music are modeled jointly in a single forward pass, not layered on afterward. Output is up to 2K resolution, 24fps, and up to about 15 seconds.

## About this workflow

This template runs the **Image to Video** task (`MiniMaxH3ImageToVideo` node), which covers both:

- **t2va** (text-to-video), when no images are connected
- **fl2va** (first/last-frame image-to-video), when `first_frame` and/or `last_frame` are connected

**Key inputs**

- **first_frame / last_frame**: optional keyframes; the model generates the motion between them
- **prompt**: describe the shots, motion, and the accompanying audio (dialogue, SFX, music) in one block
- **width / height**: set via Resolution Selector. H3's native canvas is a 768px short edge, capped at 768x1344 pixels, rounded to a multiple of 32
- **duration (seconds)**: converted to a valid frame `length` by the Math Expression node, snapping up to the model's 17-frame-per-block (17k+5) grid at 24fps

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**Input Assets**
- [transparent_rgb_gaming_mouse.png](https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/input/transparent_rgb_gaming_mouse.png) — required workflow input (`input/transparent_rgb_gaming_mouse.png`)

**vae**


**diffusion_models**


**text_encoders**


**loras**


**embeddings**


## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 vae/
│   ├── 📂 diffusion_models/
│   ├── 📂 text_encoders/
│   ├── 📂 loras/
│   └── 📂 embeddings/
```

## Using Prompt Embeddings

Prompt embeddings (supported since [ComfyUI#15697](https://github.com/Comfy-Org/ComfyUI/pull/15697)) add reusable style tokens to your prompt. Download one or more embeddings from the folder above into `ComfyUI/models/embeddings/`, then reference one in the prompt text with the `embedding:` prefix and the filename without its extension, for example:

`embedding:minimaxh3_art_is_explosion`

Using an embedding is optional and the template runs fine without one.

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

| megapixels | Aspect | Output (multiple=32) |
|---|---|---|
| 0.2 | 16:9 | 608 x 352 |
| 0.3 | 16:9 | 736 x 416 |
| 0.4 | 16:9 | 864 x 480 |
| 0.5 | 16:9 | 960 x 544 |
| 0.6 | 16:9 | 1056 x 608 |
| 0.7 | 16:9 | 1152 x 640 |
| 0.8 | 16:9 | 1216 x 672 |
| 0.9 | 16:9 | 1280 x 736 |
| 0.98 | 16:9 | 1344 x 768 (official 768p) |
## MiniMax H3

[MiniMax H3](https://www.minimax.io/blog/minimax-h3) is MiniMax's general-purpose, omni-modal generation model. It jointly understands text, image, video, and audio, and generates video with **native stereo audio**: voice, sound effects, and music are modeled jointly in a single forward pass, not layered on afterward. Output is up to 2K resolution, 24fps, and up to about 15 seconds.

## ComfyUI links
- [ComfyUI#15224](https://github.com/Comfy-Org/ComfyUI/pull/15224)
- [🤗 Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3)

## About this workflow

This template runs the **reference-to-video (ref2va)** task using the `MiniMaxH3ReferenceToVideo` node. It takes any mix of reference images, videos, and standalone audio, and weaves them into the generation to lock in a character's identity, a style, a motion, a camera move, or a voice.

**Key inputs**

- **ref_images / ref_videos / ref_video_audios / ref_audios**: up to 9 reference images, 3 reference videos (each may carry its own paired soundtrack), and 3 standalone reference audio clips
- **prompt**: reference the inputs by tag, in the exact order they were connected, for example `<Picture 1>`, `<Video 1>`, `<Audio 1>`, then describe the target scene, motion, and audio
- **ref_image_size**: `match` scales references down to the generation's resolution (faster); `max` keeps up to a 2048px short edge for stronger identity fidelity, at the cost of speed since reference tokens ride along every sampling step
- **width / height**: set via Resolution Selector.
- **duration (seconds)**: converted to a valid frame `length` by the Math Expression node

**Sampling and decode**

- Sampler: `res_multistep`. `beta` or `normal` scheduler tends to outperform `simple` for reference-heavy prompts like this one
- The sampler's joint audio+video `LATENT` output feeds directly into both `VAEDecode` (video, `minimax_h3_video_vae_fp16`) and `VAEDecodeAudio` (audio, `minimax_h3_audio_vae_fp32`); each decode node automatically pulls its own half out of the packed latent. `CreateVideo` then muxes the two into a single MP4 with synced sound
- The diffusion model here is `minimax_h3_ref2va_pruned_int8_convrot.safetensors`, a different set of weights from the `fl2va` model used by the t2v/i2v templates

Ref2va's output is very sensitive to prompt wording; matching the reference tags precisely and being explicit about which reference drives which part of the shot tends to work best.

---

## Model Links

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
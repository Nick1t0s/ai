## [Stable Audio 3](https://github.com/Stability-AI/stable-audio-3)

**Stable Audio 3** turns a **text description** into **stereo audio**: music, instruments, SFX, short one-shots, and similar material, guided by what you write (style, instruments, energy, length, and so on).

**What this graph does:** you supply a **short idea**. The workflow can **expand it with Qwen** using a **category-aware** reprompt template (Music / Instrument / SFX / One-shot), then runs the **Stable Audio** checkpoint so the expanded text becomes a **full clip**. The subgraph returns **`AUDIO`** (decoded waveform).

---

## About the Audio Generation (Stable Audio 3 Base)  subgraph

**Inputs** (same order as pins on the subgraph node)

- `user_input` — short text fed into the reprompt template.
- `duration` — clip length in seconds.
- `seed` — KSampler seed.
- `use_reprompt` — enables the reprompt / text-switch path.
- `category` — reprompt preset (Music, Instrument, SFX, One-shot).
- `ckpt_name` — Stable Audio checkpoint.
- `sa_clip` — text encoder for Stable Audio conditioning.
- `qwen_clip` — text encoder for Qwen TextGenerate.

**Output:** `AUDIO`

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**text_encoders**


**checkpoints**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 text_encoders/
│   └── 📂 checkpoints/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)
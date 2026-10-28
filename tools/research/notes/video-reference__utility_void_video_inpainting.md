Related PR: [#13403](https://github.com/Comfy-Org/ComfyUI/pull/13403)

## Model Links

**checkpoints**


**text_encoders**


**vae**


**optical_flow**


**diffusion_models**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 checkpoints/
│   ├── 📂 text_encoders/
│   ├── 📂 vae/
│   ├── 📂 optical_flow/
│   └── 📂 diffusion_models/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

Project: [Netflix/void-model](https://github.com/Netflix/void-model)

## What this stack is good at

Segmentation (**SAM3** from your text cue) defines **what** to erase; the **two-pass** video model **inpaints holes over time**. Strengths:

- **Object removal**, not single-frame patching: coherent motion and lighting across the clip.
- **Interaction-aware seams**: occluded pixels are filled as if the object (and often its immediate influence on nearby stuff) **was never there**, so shadows, overlaps, or simple causal cues can look **more plausible** than a naive erase.
- **Pass 2** refines temporal stability (fewer jitters/flashes) versus **Pass 1** alone — useful on longer cuts or textured backgrounds.

Limits: unclear masks, chaotic motion, or targets that dominate the frame still fail; prompting cannot fix fundamentally wrong segmentation.

## Inputs

- **Source video** — From ComfyUI `input` (`Load Video`).
- **Positive prompt (inpaint fill)** — The **filled** scene after removal (what remains / how it looks and moves).
- **Negative prompt** — Optional anti-artifact list; can be empty.
- **SAM3 object prompt** — Short label for **what** to mask out.

## Prompt writing

**Positive (inpaint)** — Describe the **result**, not “remove X”. Example: `empty kitchen counter, daylight, tiles visible`.

**SAM3 object** — Short referring phrase: `person in blue jacket`, `red cup on table`.

| Field | Role |
|--------|------|
| SAM3 | **What** is removed |
| Positive | **How** the hole is filled in time |

Use **Negative** only when you see repeating defects (watermark, blur, extra limbs, etc.).
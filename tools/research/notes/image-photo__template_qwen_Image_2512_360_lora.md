Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**text_encoders**


**vae**


**diffusion_models**


**loras**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 text_encoders/
│   ├── 📂 vae/
│   ├── 📂 diffusion_models/
│   └── 📂 loras/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

"equirectangular", "360 image", "360 panorama", or "360 degree panorama with equirectangular projection"

---

## [Qwen 360 Diffusion LoRA](https://huggingface.co/ProGamerGov/qwen-360-diffusion/)

Rank-128 LoRA on **Qwen-Image-2512** for **equirectangular 360°** text-to-image. Trained on tens of thousands of 2:1 panoramas (landscapes, interiors, people, objects).

### How it fits this graph

| Subgraph control | Role |
|------------------|------|
| **`lora_model`** | Qwen 360 Diffusion (default strength **1.0**) |
| **`lightning_lora`** + **`enable_turbo_mode`** | Optional 4-step Lightning LoRA — speed only, not 360-specific |

Connect your prompt via the trigger prefix + main text. Trigger phrases → **Note: LoRA Trigger Words** (next to prompt).

### Recommended settings

- **Size:** **2048×1024** (2:1, workflow default). Smaller 2:1 (e.g. 1024×512) can work but horizons may be less stable.
- **Prompt:** Add medium/style (photograph, illustration, etc.). Image **wraps left↔right**; top/bottom are sphere poles.
- **People:** For full-body shots, describe head/face and shoes/boots to reduce limb distortion.

### FP8 base model note

This template uses `qwen_image_2512_fp8_e4m3fn`. With the **int8-trained** 360 LoRA, rare patch/grid artifacts may appear — try slightly lower LoRA strength or prompt tweaks; see the [model card](https://huggingface.co/ProGamerGov/qwen-360-diffusion) for int4 LoRA variants on FP8 quants.

### Next steps

Try to load the output as a background image in the Load 3D node in ComfyUI, it supports panoramic images as the background
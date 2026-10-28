# Mage-Flow-Turbo (Text-to-Image)

**Mage-Flow-Turbo** is the few-step distilled variant of Microsoft's 4B Mage-Flow text-to-image model. Distilled from the Base/RL checkpoints via decoupled-DMD + adversarial perceptual guidance, Turbo trades a small amount of quality for **~7× fewer denoising steps**.

**Good at:** fast prompt iteration, interactive previews, portraits, landscapes, still life, cinematic scenes, and surreal/editorial compositions.

## Links

- **Mage project:** https://github.com/microsoft/Mage
- **ComfyUI integration PR:** https://github.com/Comfy-Org/ComfyUI/pull/15026
- **Model repo:** https://huggingface.co/Comfy-Org/Mage-Flow

This workflow ships with **4 steps / CFG 1.0** pre-configured in the KSampler.

## Resolution limits

| Item | Value |
|------|-------|
| Output range | **512 – 2048** px per side |
| Alignment | Width & height must be a **multiple of 16** |
| Aspect ratio | Any; extreme **4:1** supported (e.g. `2048×512`) |

**Recommendations:** **1024** for everyday use; **1536–2048** when you need more detail. Avoid exceeding **2048**.

## Workflow parameters

| Parameter | Description |
|-----------|-------------|
| `prompt` | Text description (English recommended) |
| `negative_prompt` | Optional; what to avoid |
| `seed` | Fixed seed or randomize |
| `width` / `height` | Via **ResolutionSelector**; step 16 |
| `unet_name` | `mage_flow_turbo_int8_convrot` (default) or `mage_flow_turbo_bf16` |
| `clip_name` | `qwen3vl_4b_bf16.safetensors` (type: mage) |
| `vae_name` | `mage_flow_vae_bf16.safetensors` (shared with all Mage-Flow variants) |

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**diffusion_models** (Mage-Flow-Turbo)


**text_encoders** (shared across all Mage-Flow variants)


**vae** (shared across all Mage-Flow variants)



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
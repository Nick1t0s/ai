# Mage-Flow (Text-to-Image)

- **Mage project:** https://github.com/microsoft/Mage
- **ComfyUI integration PR:** https://github.com/Comfy-Org/ComfyUI/pull/15026

## Resolution limits

| Item | Value |
|------|-------|
| Output range | **512 – 2048** px per side (native-resolution training range) |
| Alignment | Width & height must be a **multiple of 16** (VAE downsamples 16×) |
| Aspect ratio | Any; extreme **4:1** supported (e.g. `2048×512`, `512×2048`) |

**Recommendations:** use **1024** longest side for everyday tests; **1536–2048** for higher quality. Avoid exceeding **2048**.

## Model variants

| Variant | Steps | CFG | Notes |
|---------|-------|-----|-------|
| Base | 30 | 5.0 | Stable baseline |
| RL | 20 | 5.0 | Better prompt following & aesthetics |
| Turbo | **4** | **1.0** | Fastest (~0.6 s/image at 1024² on A100) |

Swap the diffusion model checkpoint in the subgraph to match your variant. Turbo **must** use 4 steps and CFG 1.0.

## Workflow parameters

| Parameter | Description |
|-----------|-------------|
| `prompt` | Text description of the image (English recommended for best results) |
| `negative_prompt` | Optional; what to avoid (blur, artifacts, etc.) |
| `seed` | Fixed seed for reproducibility; randomize to explore |
| `width` / `height` | Output size via **ResolutionSelector**; step 16 |
| `unet_name` | Diffusion model (e.g. `mage_flow_int8_convrot` or `mage_flow_bf16`) |
| `clip_name` | `qwen3vl_4b_bf16.safetensors` (type: mage) |
| `vae_name` | `mage_flow_vae_bf16.safetensors` |

Default sampler in subgraph: **30 steps**, **CFG 5.0**, euler / simple.

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**diffusion_models** (text-to-image — pick one)


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
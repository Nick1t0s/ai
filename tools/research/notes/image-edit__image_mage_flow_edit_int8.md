# Mage-Flow-Edit

**Mage-Flow-Edit** is Microsoft's 4B instruction-based image editing model (Mage-VAE + Native-Resolution DiT + Qwen3-VL). It supports background replacement, style/lighting changes, localized content edits, restoration, and multi-reference editing (1–3 refs recommended).

## Links

- **Mage project:** https://github.com/microsoft/Mage
- **ComfyUI integration PR:** https://github.com/Comfy-Org/ComfyUI/pull/15026

## Resolution limits

| Item | Value |
|------|-------|
| Output range | **512 – 2048** px per side (native-resolution training range) |
| Alignment | Width & height must be a **multiple of 16** (VAE downsamples 16×) |
| Aspect ratio | Any; extreme **4:1** supported (e.g. `2048×512`) |
| Reference input | No hard pixel cap; resized to the target output size |
| VL conditioning | Reference long edge capped at **384px** internally |

**Recommendations:** use **1024** longest side for everyday tests; **1536–2048** for higher quality. Avoid exceeding **2048** — quality and stability drop outside the training distribution.

## Workflow parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `prompt` | — | Edit instruction (English recommended). State what to keep, then what to change. |
| `seed` | randomize | Fixed seed for reproducibility |
| `steps` | 30 | Denoising steps (Base/RL: 30; Turbo: 4) |
| `cfg` | 5.0 | Guidance scale (Turbo: 1.0) |
| `resize_input_image` | true | Pre-scale the reference image before editing |
| `target_megapixels` | 1.0 | Target area in megapixels when resizing (~1.0 ≈ 1024×1024) |
| `match_input_size` | true | Output size follows the (resized) reference; if false, use `width` / `height` |
| `width` / `height` | 1024 | Manual output size (only when `match_input_size` = false); step 16 |

### Size logic

1. `resize_input_image = true` → scale input to `target_megapixels` first
2. `match_input_size = true` → output matches processed reference dimensions
3. `match_input_size = false` → output uses manual `width` × `height`

## Models (BF16)

- `mage_flow_edit_bf16.safetensors` — edit DiT
- `qwen3vl_4b_bf16.safetensors` — Qwen3-VL encoder (type: mage)
- `mage_flow_vae_bf16.safetensors` — Mage-VAE

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

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
Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**vae**


**diffusion_models**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 vae/
│   └── 📂 diffusion_models/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

## SeedVR2

One-step video restoration / upscale (ICLR 2026). This workflow uses the **3B Int8** model for video upscaling.

- Project: [SeedVR2](https://iceclear.github.io/projects/seedvr2/)
- ComfyUI native support: [PR #14424](https://github.com/Comfy-Org/ComfyUI/pull/14424)

### Subgraph parameters

- **trim_video**: enable to cut a segment before upscaling
- **trim_start_time / duration**: trim start (seconds) and length
- **scale_multiplier**: upscale factor (default `2`)
- **seed / sampler / scheduler / denoise**: sampling controls; `denoise=1` means full restore
- **color_correction_method**: optional color match to original (default `none`)
- **unet_name / vae_name**: model files to load

### Tip: long videos

If the input is too long, turn on **trim_video**, upscale in shorter segments, then merge them. This helps avoid OOM / slowdowns on long clips.
# GAN Upscaler Workflow

A fast approach for upscaling videos using GAN models. It can't create new detail like diffusion can, but it's much faster.

- **Model determines output size** — 2x models upscale 2x, 4x models upscale 4x
- **Tip:** Upscale 4x first, then use a resize node to bring it down to your target resolution

## Model Links

**upscale_models**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 upscale_models/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud will be updated after the stable release; nightly-supported models may not be included yet, please wait for the next stable release.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/Comfy-Org/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)
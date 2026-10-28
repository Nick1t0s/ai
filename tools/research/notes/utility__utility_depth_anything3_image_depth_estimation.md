Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Link

**geometry_estimation**


## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   └── 📂 geometry_estimation/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

## About Depth Anything 3

[Depth Anything 3 (DA3)](https://github.com/ByteDance-Seed/Depth-Anything-3) is a vision transformer from ByteDance Seed that recovers spatially consistent geometry from arbitrary visual inputs, with or without known camera poses. A single plain DINO encoder and unified depth-ray representation let one model family cover monocular depth, multi-view depth, camera pose estimation, and 3D reconstruction.

### What this workflow does

Upload one image and run **Image Depth Estimation (Depth Anything 3)** to produce a depth map. The result is shown in **Depth Preview**, with a side-by-side **ImageCompare** against the source image.

### Model variants

- **depth_anything_3_mono_large** (default): High-quality relative monocular depth with sky segmentation. Best starting point for single-image depth maps.
- **depth_anything_3_metric_large**: Metric depth in real-world scale (meters). Use `raw` normalization in Render to preserve scale.
- **depth_anything_3_base**: Any-view foundation model (0.12B). Adds confidence maps and supports multi-view mode.
- **depth_anything_3_small**: Fastest any-view model (0.08B). Lowest VRAM; supports confidence and multi-view.


### Learn more

- Paper: [arXiv:2511.10647](https://arxiv.org/abs/2511.10647)
- Original repo: [ByteDance-Seed/Depth-Anything-3](https://github.com/ByteDance-Seed/Depth-Anything-3)
- ComfyUI weights: [Comfy-Org/Depth-Anything-3](https://huggingface.co/Comfy-Org/Depth-Anything-3)
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

[Depth Anything 3 (DA3)](https://github.com/ByteDance-Seed/Depth-Anything-3) is a vision transformer from ByteDance Seed that recovers spatially consistent geometry from arbitrary visual inputs. In ComfyUI, it can estimate a depth map for every frame of a video.

### What this workflow does

Upload a video with **LoadVideo**, then run **Video Depth Estimation (Depth Anything 3)** to produce a per-frame depth sequence. Inside the subgraph:

1. **GetVideoComponents** splits the input video into a frame **image sequence**, **audio**, and **fps**.
2. **LoadDA3Model** loads the selected DA3 checkpoint.
3. **DA3Inference** runs mono depth estimation on each frame.
4. **DA3Render** converts geometry into a depth preview image per frame.

The subgraph also forwards the original **audio** and **fps** from the source video for downstream reuse.


### Model variants

- **depth_anything_3_mono_large** (default): High-quality relative monocular depth with sky segmentation. Best starting point for per-frame video depth.
- **depth_anything_3_metric_large**: Metric depth in real-world scale (meters). Use `raw` normalization in Render to preserve scale.
- **depth_anything_3_base**: Any-view foundation model (0.12B). Adds confidence maps; supports multi-view mode (not used in this per-frame video workflow).
- **depth_anything_3_small**: Fastest any-view model (0.08B). Lowest VRAM per frame.

### Learn more

- Paper: [arXiv:2511.10647](https://arxiv.org/abs/2511.10647)
- Original repo: [ByteDance-Seed/Depth-Anything-3](https://github.com/ByteDance-Seed/Depth-Anything-3)
- ComfyUI weights: [Comfy-Org/Depth-Anything-3](https://huggingface.co/Comfy-Org/Depth-Anything-3)
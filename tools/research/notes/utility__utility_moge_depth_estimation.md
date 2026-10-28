## moge_depth_estimation

**Single perspective photo -> depth previews + mask**

`Load Image` -> `Depth Estimation (MoGe)`

### Main flow
- Runs MoGe inference on one source image
- Renders both colored depth and raw depth previews
- Converts the rendered `mask` image into a real `MASK` output

### Inputs
| Control | Meaning |
|--------|--------|
| `source_image` | Input RGB image |
| `inference_resolution` | MoGe detail level `0-9`; higher is slower but keeps more detail |
| `inference_batch_size` | Passed to `MoGeInference` batch size; use `1` for a single still image |
| `moge_model` | Model checkpoint loaded by `LoadMoGeModel`; see `Model Link` |
| `auto_resize_input` | Enables pre-inference resize logic for large images |

### Auto-resize logic
When `auto_resize_input` is enabled, the subgraph checks image width first:
- width `> 2048`: resize by longer edge to `2048` before inference
- width `<= 2048`: keep the original image

When `auto_resize_input` is disabled, the original image always goes into inference.

### Outputs
- `depth_colored`: colorized depth preview from `MoGeRender`
- `depth`: raw depth preview from `MoGeRender`
- `MASK`: mask rendered by `MoGeRender` and converted through `ImageToMask`

### What `MASK` means
According to the official MoGe repo, `mask` is a **binary mask for valid pixels**.

In practice, it marks image regions where MoGe believes the geometry is defined and reliable enough to use for downstream geometry results. Regions with undefined geometry, such as sky or other ambiguous areas, are typically excluded.

This is **not** a foreground segmentation or object cutout mask. It is better understood as a **valid geometry mask**.

---

## MoGe — models & downloads

Research repo: [microsoft/MoGe](https://github.com/microsoft/MoGe) (CVPR'25, monocular geometry from a single image).


### Which checkpoint to use

| File | Version | Use when |
|------|---------|----------|
| `moge_1_vitl_fp16` | **MoGe-1** | Point map + depth + mask; relative scale. Lighter baseline. |
| `moge_2_vitl_normal_fp16` | **MoGe-2** | **Recommended.** Metric-scale depth/points, sharper detail, **normal maps** (needed for normal previews & better mesh edges). |

MoGe-2 adds metric scale and normals in one forward pass; MoGe-1 does not predict normals (normals in previews may be derived from points).

### Downloads


## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   └── 📂 geometry_estimation/
```

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

### Issues
Update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)), then install models.
- Runtime: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
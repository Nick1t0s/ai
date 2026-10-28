## moge_image_to_mesh

**Single perspective photo -> textured GLB**

`Load Image` -> `Geometry Estimation (MoGe)` -> `Save GLB`

### Main flow
- Runs MoGe inference on one source image
- Converts the inferred geometry into a mesh
- Exposes OpenGL and DirectX normal previews

### Inputs
| Control | Meaning |
|--------|--------|
| `source_image` | Input RGB image |
| `inference_resolution` | MoGe detail level `0-9`; higher is slower but keeps more detail |
| `inference_batch_size` | Passed to `MoGeInference` batch size; use `1` for a single still image |
| `mesh_frame_index` | Batch/frame index used when converting geometry to mesh; use `0` for one image |
| `mesh_decimation` | Mesh decimation step; `1` keeps the densest mesh |
| `mesh_gap_threshold` | Removes faces across large depth discontinuities; `0` disables the filter |
| `mesh_texture` | Bakes source image colors into the exported GLB |
| `moge_model` | Model checkpoint loaded by `LoadMoGeModel`; see `Model Link` |
| `auto_resize_input` | Enables pre-inference resize logic for large images |

### Auto-resize logic
When `auto_resize_input` is enabled, the subgraph checks image width first:
- width `> 2048`: resize by longer edge to `2048` before inference
- width `<= 2048`: keep the original image

When `auto_resize_input` is disabled, the original image always goes into inference.

### Outputs
- `mesh`: mesh output for `Save GLB`
- `normal_opengl`: preview rendered through `MoGeRender`
- `normal_directx`: preview rendered through `MoGeRender`

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
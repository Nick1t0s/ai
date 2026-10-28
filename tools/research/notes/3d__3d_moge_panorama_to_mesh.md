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

---

## moge_panorama_to_mesh

**Equirectangular (360°) panorama → textured GLB**

`Load Image` → subgraph `source_panorama` → `Save GLB`

Uses **`MoGePanoramaInference`**: 12 perspective views → merge → mesh. Research: [microsoft/MoGe](https://github.com/microsoft/MoGe).

Single photo workflow: `3d_moge_perspective_to_mesh.json` (`MoGeInference` + depth/normal previews).

### Pipeline
1. Optional downscale if `auto_resize_input` and width > 2048
2. Split equirect into **12** crops (90° FOV)
3. MoGe on each crop (`panorama_split_resolution`, `inference_resolution`)
4. **CPU merge** — stitch distance maps into one equirect depth (`panorama_merge_resolution`)
5. `MoGePointMapToMesh` → GLB with vertex colors

Merge disables per-view metric scale; MoGe-2 normals are not stitched. A long **“panorama merge”** progress phase is expected.

### Input
- **Equirectangular** 360°×180°, usually **2:1** (e.g. 2048×1024)
- **One** image per run

### Subgraph ports
| Port | Meaning |
|------|--------|
| `source_panorama` | RGB equirect |
| `inference_resolution` | MoGe detail **0–9** (default 9) |
| `panorama_split_resolution` | Each crop side length — **GPU** (default 512) |
| `panorama_merge_resolution` | Merge grid **long edge** — **CPU** (default 1920; never above input size) |
| `inference_batch_size` | Views per forward, 12 total (default 4) |
| `mesh_frame_index` | **0** for one panorama |
| `mesh_decimation` | Vertex stride; **1** = full |
| `mesh_gap_threshold` | Cull faces at depth jumps; **0** = off |
| `mesh_texture` | Bake panorama into GLB |
| `moge_model` | Checkpoint — **Model Link** |
| `auto_resize_input` | Downscale when width > 2048 |

**Split vs merge:** split = per-view inference sharpness; merge = seam / global depth quality. Example: 4096×2048 + merge **1920** → solve ~1920×960, then upsample to input size for meshing.

### Tuning
| Goal | Try |
|------|-----|
| Faster | resolution 6–7, split 512, merge 1280 |
| Quality | resolution 9, split 768+, merge 2048+, MoGe-2 |
| GPU OOM | batch 1–2, split 512 |
| Slow merge | lower `panorama_merge_resolution` |

### Output
`mesh` → **Save GLB** (default `3d/Moge`). Spherical glTF mesh — view from inside the sphere.
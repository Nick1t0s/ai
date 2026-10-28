# SCAIL-2 Character Replacement

This workflow is using subgraph, please check [here](https://docs.comfy.org/interface/features/subgraph) for more details

## About SCAIL-2

[SCAIL-2](https://huggingface.co/zai-org/SCAIL-2) is an end-to-end character animation model that drives a reference character image with a driving video for character animation or in-video character replacement.


---

## Parameters

### Shared (Base & Extend)

| Input | Notes |
|---|---|
| `pose_video` | Driving video |
| `reference_image` | Character to use |
| `prompt` | Output video description — see **Prompt Writing** below |
| `replace_mode` | `true` = Replacement (default), `false` = Animation |
| `segment_index` | `1` first chunk; `2+` continue. Pose offset = `76 × (index − 1)` |
| `width` / `height` | e.g. 896×512 |
| `frame_count` | Default **81** (4n+1) |
| `previous_frame_count` | Overlap **5** |
| `pose_strength` / `pose_start` / `pose_end` | Pose conditioning |
| `turbo_mode` | Lightx2v fast preset |
| `distill_lora` / `dpo_lora` | Speed / quality LoRA strength |
| `sam3_video_object` | SAM3 text for driving video — see **SAM3** below |
| `sam3_image_object` | SAM3 text for reference image |

### Extend only

| Input | Notes |
|---|---|
| `previous_frames` | IMAGE from previous segment; only last `previous_frame_count` frames used |

---

## Two Modes (`replace_mode`)

| Value | Mode | Summary |
|---|---|---|
| `true` | **Replacement** | Swap tracked person in driving video with reference character. Driving mask bg: **white**. **This workflow default.** |
| `false` | **Animation** | Reference character performs driving motion. Driving mask bg: **black**. |

Set on **both** subgraphs. Animation still needs masks; rewrite `prompt` accordingly.

---

## SAM3 (two inputs)

Not the SCAIL-2 `prompt` — only for mask track/segment:

| Pin | Target | Output mask |
|---|---|---|
| `sam3_video_object` | Driving video | `pose_video_mask` |
| `sam3_image_object` | Reference image | `reference_image_mask` |

Open-vocabulary text (default `human`). Use the same word when subject matches; use different words if video/ref need different focus (e.g. crowded scene → be more specific).

Colored masks bind body regions between ref and driving. Main `prompt` controls final appearance.

---


## How This Workflow Works

1. Load `pose_video` + `reference_image`.
2. **Base** subgraph — segment 1 (`segment_index = 1`, no `previous_frames`).
3. **Extend** subgraph — segment 2+ (`previous_frames` from prior output, increment `segment_index`).
4. Preview / save; stitch segments if needed.


---

## Long Videos

`ceil(total_frames / 76)` segments — see **Estimate Segment Count** group.

| Segments | Action |
|---|---|
| 1 | Base only |
| 2+ | Base + Extend(s); duplicate Extend, chain `previous_frames`, increase `segment_index` |

**No auto loop:** `WanSCAILToVideo` cannot queue all segments automatically — run each segment manually.

---

Requires ComfyUI [PR#14373](https://github.com/Comfy-Org/ComfyUI/pull/14373)

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**loras**


**vae**


**text_encoders**


**clip_vision**


**diffusion_models**


**checkpoints**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 loras/
│   ├── 📂 vae/
│   ├── 📂 text_encoders/
│   ├── 📂 clip_vision/
│   ├── 📂 diffusion_models/
│   └── 📂 checkpoints/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)
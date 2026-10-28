## Bernini-R · Image Editing Workflow

**Official repos**
- Inference & task docs: [bytedance/Bernini](https://github.com/bytedance/Bernini)
- Bernini-R weights (ComfyUI): [Comfy-Org/Bernini-R](https://huggingface.co/Comfy-Org/Bernini-R)
- Paper: [Bernini: Latent Semantic Planning for Video Diffusion](https://arxiv.org/abs/2605.22344)

---

### What is this workflow?

Built for **Bernini-R image generation & editing** in ComfyUI: pick **task type** → connect inputs → write prompt → run.

Bernini-R is ByteDance's **renderer-only** Wan 2.2 model (in-context conditioning). It does **not** include the full Bernini MLLM planner. For longer, official-quality prompts, see `--use_pe` in the [Bernini repo](https://github.com/bytedance/Bernini).

Default **`length = 1`** inside the graph — suited to **single-frame image** output (saved via **Save Video** as a 1-frame clip). Raise `length` only if you intentionally want a short motion clip.

**Prompt format:** `{system prompt from task type}` + `{your English description}` via **Prompt Construction**.

---

### Task types (this workflow)

| Task type | What to connect | Use for |
|-----------|-----------------|---------|
| **Default** | Nothing | Generic generation; default system prompt |
| **Text to Image** | Nothing | Generate an image from text only (`t2i`) |
| **Text to Video** | Nothing | Generate motion from text only (`t2v`; increase `length` if needed) |
| **Image Editing** | **`source_image`** | Edit an existing image — background swap, remove/add objects, style tweaks (`i2i`) |
| **Subject to Image** | **`reference_image(s)`** | Compose a new image from reference subjects / items / scenes (`r2i`) |

Video-editing task types (`v2v`, `rv2v`, `r2v`, `ads2v`, …) are **not** included in this workflow.

---

### Inputs

**`source_image` (slot 1 — Image Editing)**
- The image to edit. **Load Image** (or image frames) → subgraph **`source_image`**.
- Resized to **`width × height`** (inside graph). Match your image aspect; both dimensions should be **multiples of 16**.
- Leave disconnected for **Text to Image / Text to Video / Default**.

**`reference_image(s)` (optional — group: Reference Image input)**
- Used for **Subject to Image**. Each image is a separate in-context stream; long edge capped by **`ref_max_size`** (default **848**), aspect ratio preserved.
- **Wire:** **Load Image** → **Batch Images** (`image0`, `image1`, …) → subgraph **`reference_image`**.
- In prompt, refer to **`image0`, `image1`, …** (order = batch slot order).

**`reference_video`**
- Still available on the subgraph but **not used** by the task types above. Leave disconnected unless you extend the graph yourself.

---

### Turbo mode (`enable_turbo_mode`)

**Turbo = fast preview**, not the official Bernini sampling recipe.

| | **Turbo ON** (default) | **Turbo OFF** |
|--|------------------------|---------------|
| **LightX2V distill LoRA** | ON (high **3.0**, low **1.5**) | OFF |
| **Steps** | **6** (split **3** / **3**) | **40** (split **20** / **20**) |
| **CFG** | **1** | **5** |

Use Turbo to iterate on prompts; turn **OFF** for final quality.

Official defaults: [gradio_demo.py](https://github.com/bytedance/Bernini/blob/main/gradio_demo.py)

---

### Prompt examples

**Image Editing (`source_image`, no reference)**
- Background: *Replace the plain white studio background with a warm beach at sunset … Keep the model's identity, clothing, pose, and framing unchanged.*
- Remove object: *Delete the bicycle in front of the window. Fill the area with matching wall and ground. Keep everything else unchanged.*
- Add element: *Add a small potted plant on the table at center-left. Keep the table, lighting, and all other objects unchanged.*

**Subject to Image (`reference_image` only)**
- *The marble statue from image0, wearing the black T-shirt from image1, sits on the bench in the beach sunset setting from image2, facing the camera in a medium shot.*

More cases: [assets/testcases/](https://github.com/bytedance/Bernini/tree/main/assets/testcases/)

---

### Tips

- **Image Editing:** say both **what changes** and **what must stay** (identity, pose, lighting, composition).
- **Subject to Image:** name each reference (`image0`, `image1`, …) and its role.
- Task type sets the **system prompt prefix** only; wiring (`source_image` vs `reference_image`) determines what BerniniConditioning receives.

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**text_encoders**


**vae**


**loras**


**diffusion_models**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 text_encoders/
│   ├── 📂 vae/
│   ├── 📂 loras/
│   └── 📂 diffusion_models/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

### Reference Image input (multi-image)

Use for **Subject to Image** when you need **one or more reference images** (subject, outfit, scene, props).

1. **Load Image** — one node per reference.
2. **Batch Images** — connect loads to `image0`, `image1`, …
3. **Subgraph** — **Batch Images → IMAGE** → **`reference_image`**.

In the prompt, use **`image0`, `image1`, …** to say which reference is which.

Not needed for **Image Editing** — that task uses **`source_image`** instead.

---

You can find the original settings here: https://github.com/bytedance/Bernini/blob/main/gradio_demo.py
## Bernini-R · Video Editing Workflow

**Official repos**
- Inference & task docs: [bytedance/Bernini](https://github.com/bytedance/Bernini)
- Bernini-R weights (ComfyUI): [Comfy-Org/Bernini-R](https://huggingface.co/Comfy-Org/Bernini-R)
- Paper: [Bernini: Latent Semantic Planning for Video Diffusion](https://arxiv.org/abs/2605.22344)

---

### What is this workflow?

Built for **Bernini-R video editing** in ComfyUI: **source video** + optional **reference image(s)** / **reference video** → pick **task type** → write prompt → run.

Bernini-R is ByteDance's **renderer-only** Wan 2.2 model (in-context conditioning). It does **not** include the full Bernini MLLM planner. For official-quality long prompts, see `--use_pe` in the [Bernini repo](https://github.com/bytedance/Bernini).

| Task | What to connect |
|------|-----------------|
| Text to Video | No media |
| Video Editing (`v2v`, `mv2v`) | `source_video` only |
| Reference to Video (`r2v`) | `reference_image(s)` only |
| **Video Editing with Reference (`rv2v`)** | `source_video` + `reference_image(s)` — **outfit / look swap** |
| Ads / Content Insertion (`ads2v`) | `source_video` + `reference_video` |

**Prompt format:** `{system prompt from task type}` + `{your English description}` via **Prompt Construction**.

---

### Inputs: source video, reference images, reference video

**`source_video` (required for most edits)**
- The clip to edit (canvas). Loaded via **Load Video** → subgraph `source_video`.
- Resized to **`width × height`** and trimmed to **`length`** frames.
- Match output size to your clip (e.g. portrait **832 × 1104**, landscape **848 × 480**). Both dimensions should be **multiples of 16**.

**`reference_image(s)` (optional — group: Reference Image input)**
- Used for **`rv2v`** (edit guided by refs), **`r2v`** (refs only), or multi-item outfits.
- Each image is encoded as a **separate in-context stream**; long edge capped by **`ref_max_size`** (default **848**), **aspect ratio preserved**.
- **How to wire:** put one or more **Load Image** nodes into **Batch Images** (`image0`, `image1`, …) → connect **Batch Images → IMAGE** to the subgraph input **`reference_image`**.
- **Multi-image tips:** e.g. flat-lay coat + pants + boots on separate Load Image slots; in prompt use **image0, image1, …** (order = batch / slot order). Official training supports ~**5** reference streams reliably; the node allows up to **8** slots inside the graph.
- **Not** resized to full canvas — only long-edge limited (unlike `source_video`).

**`reference_video` (optional)**
- Used for **`ads2v`** — content to **insert into** the source scene (moving clip, screen content, etc.).
- Connect a **second video** (often **Load Video → Get Video Components → images**) to subgraph **`reference_video`**, or feed frame sequence as IMAGE.
- Same **`ref_max_size`** / aspect rules as reference images; trimmed to **`length`** frames.
- Prompt can be short: *Add the video on the computer.*

Leave unused inputs **disconnected** for tasks that do not need them.

---

### Turbo mode (`enable_turbo_mode`)

**Turbo = fast preview / iteration**, not the official Bernini-R sampling recipe.

| | **Turbo ON** (default) | **Turbo OFF** (Original settings) |
|--|------------------------|-----------------------------------|
| **LightX2V distill LoRA** | ON (high noise **3.0**, low noise **1.5**) | OFF (pure Bernini-R weights) |
| **Total steps** | **6** | **40** (official default) |
| **High / low split** | **3** / **3** | **20** / **20** |
| **CFG** | **1** | **5** |

Turbo is much **faster** and lighter on VRAM, but **quality and edit fidelity** are usually below official **40-step** inference (which also uses APG guidance in Python — not fully replicated here). Use Turbo to test prompts and wiring; turn **Turbo OFF** for final exports or difficult edits (outfit swap, fine detail).

Toggle **`enable_turbo_mode`** on the main subgraph widget (or **Boolean Enable Turbo LoRA?** inside the graph).

Official defaults reference: [gradio_demo.py](https://github.com/bytedance/Bernini/blob/main/gradio_demo.py)

---

### Recommended resolution & length

| Setting | Recommended |
|---------|-------------|
| **width × height** | **848 × 480** or **832 × 480** (landscape); match source aspect for portrait |
| **ref_max_size** | **848** (raise to **1280** for 720p experiments) |
| **length** | **81** frames @ 16 fps; must be **4n+1** |

Negative prompt: Wan 2.2 **Chinese default** in `bernini/cli.py`.

---

### Task types & prompt examples

Edits: **what to change** + **what stays unchanged**.

- **`rv2v` (outfit swap):** *Remove the hat. Replace the person's clothing with the full outfit from the reference image … Keep pose, framing, lighting, background, and motion unchanged.*
- **`v2v`:** *Add a snowman on the right … Keep the dog, road, and scene unchanged.*
- **`mv2v`:** *Change the person's motion to crouch … preserving framing and background.*
- **`ads2v`:** *Add the video on the computer.*
- **`r2v`:** *The subject from image0 wearing items from image1 and image2 …*

More: [assets/testcases/](https://github.com/bytedance/Bernini/tree/main/assets/testcases/)

---

### Capability notes

**Strengths:** video edit, reference-guided edit, outfit swap (`rv2v`), content insertion (`ads2v`), reference-to-video (`r2v`).

**Limits:** no Bernini planner; Turbo ≠ official 40-step APG; long / 720p needs more VRAM; flat-lay outfit refs are harder than on-person reference photos.

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

Use this group when a task needs **one or more reference images** (`rv2v`, `r2v`, multi-piece outfits).

1. **Load Image** — one node per reference (coat, pants, full outfit, face, etc.).
2. **Batch Images** — connect each load to `image0`, `image1`, … (add slots as needed).
3. **Subgraph** — connect **Batch Images → IMAGE** to **`reference_image`**.

Each batched image becomes its own in-context token. Mention **`image0`, `image1`, …** in the user prompt if refs play different roles.

---

You can find the original settings here: https://github.com/bytedance/Bernini/blob/main/gradio_demo.py
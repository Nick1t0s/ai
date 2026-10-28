### Denoise Parameter Explained
The denoise value controls the creative freedom of the sampler. Lower values keep outputs closer to the input; higher values allow the model to reinterpret and add more details.

| Style | Value Range | Effect |
|------|-------------|--------|
| Subtle Creativity | 0.15 – 0.25 | Output stays close to input |
| High Creativity | 0.25 – 0.35 | More reinterpretation & details |

---

## Note
Denoise values above `0.35` may introduce artifacts. To maintain coherence at high denoise, use a **detailed image caption** as your prompt to provide the model with more context.

**Comparison example at `0.5` denoise:**  
- **Prompt A (minimal):** `masterpiece, 8k`  
- **Prompt B (detailed caption):** `A low-angle head-on view of an F-22 Raptor... masterpiece, 8k`

Using a detailed prompt will result in significantly more stable and coherent outputs.

---

## Model Links

**diffusion_models**


**text_encoders**


**vae**


**upscale_models**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   ├── 📂 text_encoders/
│   ├── 📂 vae/
│   └── 📂 upscale_models/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud will be updated after the stable release; nightly-supported models may not be included yet, please wait for the next stable release.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/Comfy-Org/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

Image Compare is now only available under Nodes 2.0. Open menu -> Nodes 2.0 to switch
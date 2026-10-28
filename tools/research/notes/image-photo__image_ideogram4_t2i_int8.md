Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**vae**


**diffusion_models**


**text_encoders**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 vae/
│   ├── 📂 diffusion_models/
│   └── 📂 text_encoders/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

### About the model

The model is trained on **structured JSON captions** (scene summary, style block, background, and optional per-object descriptions with bounding boxes and hex color palettes). Official inference validates prompts against that schema. Guidance uses **flow-matching** with **asymmetric classifier-free guidance** (the unconditional pass drops text tokens)—not a separate negative prompt string.

**NOTE:**  If you see "Image blocked by safety filter", this is Ideogram 4.0's built-in safety filter. Non-JSON (plain-text) prompts have a higher false-positive rate. Using structured JSON prompts reduces the chance of your prompt being blocked. See the [official prompting guide](https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md#safety-filter) for details.

---

### How to build prompts here

**(a) Raw input**: Paste or type directly into the subgraph. You may use plain natural language, but **structured JSON** (as in the subgraph default) gives the most predictable layout and style control.

**(b) Model-assisted (LLM):** Use the **Ideogram4 Caption Prompt Template** output with any LLM tools to obtain the JSON format prompt

[**Prompting Guide**](https://github.com/ideogram-oss/ideogram4#prompting-guide)

---

This is a prompt construction template. You can copy its input into any LLM to generate matching prompts.

[Prompting Guide](https://github.com/ideogram-oss/ideogram4#prompting-guide)


---
You may try installing or updating [KJNodes](https://github.com/kijai/ComfyUI-KJNodes) and use the **Ideogram 4 Prompt Builder KJ** node to achieve visual control over prompts.
- [About Qwen-Image](https://docs.comfy.org/tutorials/image/qwen/qwen-image) 

## Alvdansen Illustration v1.0 (Qwen Images)


A style LoRA for Qwen-Image trained on 244 curated illustration and anime reference images across diverse visual styles. Produces images spanning cute anime character design, European bande dessinee, indie risograph prints, storybook watercolor, retro shoujo manga, and graphic novel illustration.

---

**Recommended Inference Settings**

```
Sampler: euler
Scheduler: simple
CFG: 3.5
Steps: 45 (30-60 works well)
LoRA strength: 0.8-1.0

```
---

## Model Links

**vae**


**text_encoders**


**diffusion_models**


**loras**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 vae/
│   ├── 📂 text_encoders/
│   ├── 📂 diffusion_models/
│   └── 📂 loras/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)
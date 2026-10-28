Keep the Chinese characters.
Append additional image edit prompt instructions after.

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model links (for local users)

**text_encoders**


**loras**


**diffusion_models**


**vae**



Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 text_encoders/
│   ├── 📂 loras/
│   ├── 📂 diffusion_models/
│   └── 📂 vae/
```


## Report issue

Note: please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud will be updated after the stable release; nightly-supported models may not be included yet, please wait for the next stable release.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/Comfy-Org/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

参考色调，移除图1原有的光照并参考图2的光照和色调对图1重新照明, maintain canny edge of interior glass orb.

---

You can test and find the best setting by yourself. The following table is for reference.
| Parameters   | Qwen Team | Comfy Original | with 4steps LoRA |
|--------|---------|------------|---------------------------|
| Steps  | 50      | 20         | 4                         |
| CFG    | 4.0     | 2.5        | 1.0                       |
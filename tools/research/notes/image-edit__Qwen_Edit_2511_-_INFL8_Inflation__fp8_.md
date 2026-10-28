## About INFL8 LoRA
Note: INFL8 is a LoRA for Qwen Image Edit 2511 that lets you inflate elements within an image, using the prompt "inflate the [insert subject]"


## Model Links

**vae**


**diffusion_models**


**text_encoders**


**loras**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 vae/
│   ├── 📂 diffusion_models/
│   ├── 📂 text_encoders/
│   └── 📂 loras/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud will be updated after the stable release; nightly-supported models may not be included yet, please wait for the next stable release.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/Comfy-Org/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

You can test and find the best setting by yourself. The following table is for reference.
|   | Qwen | Comfy | lightning LoRA |
|--------|---------|------------|---------------------------|
| Steps  | 40      | 20         | 4                         |
| CFG    | 4.0     | 4.0       | 1.0                       |

By default, we use 20 steps as we just don't want it to take too long. Try 40 if you want a better result, but it will take longer.

---

The "Edit Model Reference Method" nodes above are not needed if you use Comfy files, but may be needed if you use repackaged ones from other people.
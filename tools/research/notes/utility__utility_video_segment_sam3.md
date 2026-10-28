Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**checkpoints**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   └── 📂 checkpoints/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

Max tokens for this model is only 32, to separately prompt multiple subjects you can separate prompts with comma, and set the max amount of objects detected for each prompt with :N

For example above test prompt finds 2 cakes, one apron, 4 window panels

```
eye:2, window panels:4
```

---

Max tokens for this model is only 32, to separately prompt multiple subjects you can separate prompts with comma, and set the max amount of objects detected for each prompt with :N

For example above test prompt finds 2 cakes, one apron, 4 window panels
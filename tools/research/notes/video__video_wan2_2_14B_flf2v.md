By default, we set the video to a smaller size for users with low VRAM. If you have enough VRAM, you can change the size

---

Using the Wan2.2 Lighting LoRA will result in the loss of video dynamics, but it will reduce the generation time. This template provides two workflows, and you can enable one as needed.

---

By default, we set the video to a smaller size for users with low VRAM. If you have enough VRAM, you can change the size

---

1. Box-select then use Ctrl + B to enable
2. If you don't want to run both groups simultaneously, don't forget to use **Ctrl + B** to disable the **fp8_scaled + 4steps LoRA** group after enabling the **fp8_scaled** group, or try the [partial - execution](https://docs.comfy.org/interface/features/partial-execution) feature.

---

[Tutorial](https://docs.comfy.org/tutorials/video/wan/wan2_2)


## Model links

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

If you encounter any issues when running this workflow, [report template issue here](https://github.com/Comfy-Org/workflow_templates/issues)

---

## GPU:RTX4090D 24GB

| Model            | Size |VRAM Usage | 1st Generation | 2nd Generation |
|---------------------|-------|-----------|---------------|-----------------|
| fp8_scaled               |640*640| 84%               | ≈  536s              | ≈ 513s                   |
| fp8_scaled +  4steps LoRA  | 640*640  | 89%                | ≈ 108s               | ≈ 71s                   |
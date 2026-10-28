## GPU:RTX4090D 24GB

| Model            | Size |VRAM Usage | 1st Generation | 2nd Generation |
|---------------------|-------|-----------|---------------|-----------------|
| fp8_scaled               |640*640| 84%               | ≈  536s              | ≈ 513s                   |
| fp8_scaled +  4steps LoRA  | 640*640  | 83%                | ≈ 97s               | ≈ 71s                   |

---

[Tutorial](https://docs.comfy.org/tutorials/video/wan/wan2_2
)

**Diffusion Model**

**LoRA**

**VAE**

**Text Encoder**   


File save location

```
ComfyUI/
├───📂 models/
│   ├───📂 diffusion_models/
│   ├───📂 loras/
│   ├───📂 text_encoders/
│   └───📂 vae/
```
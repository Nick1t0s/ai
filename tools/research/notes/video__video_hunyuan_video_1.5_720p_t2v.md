50 inference steps just take too long to get the final video, so by default we set the step to 20 steps. If you want a better quality, please try the original settings below

## Original setting from Hunyuan team
| Model              | cfg | embeded_cfg | shift | inference step |
|-----------------------|-----|-------------|-------|----------------|
| 480p_t2v              | 6   | None        | 5     | 50             |
| 480p_i2v              | 6   | None        | 5     | 50             |
| 720p_t2v              | 6   | None        | 9     | 50             |
| 720p_i2v              | 6   | None        | 7     | 50             |
| 480p_t2v_distilled    | 1   | None        | 5     | 50             |
| 480p_i2v_distilled    | 1   | None        | 5     | 50             |
| 720p_t2v_distilled    | 1   | None        | 9     | 50             |
| 720p_i2v_distilled    | 1   | None        | 7     | 50             |

---

If you don't have enough VRAM and encounter the OOM error, please try to set the `weight_dtype` to `fp8_e4n3fn`.

---

## Report issue

If you found any issues when running this workflow, [report template issue here](https://github.com/Comfy-Org/workflow_templates/issues)
## Model links

**text_encoders**


**diffusion_models**


**vae**



Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 text_encoders/
│   ├── 📂 diffusion_models/
│   └── 📂 vae/
```

---

EasyCache can speed up this workflow, but it will also sacrifice the video quality. If you need it, use Ctrl+B to enable.

---

Use the VAE Decode (Tiled) if it takes too long to get the final video.

---

Split at matching sigma to the noise scale
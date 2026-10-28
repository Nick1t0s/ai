Download the style LoRAs used in this workflow from [Comfy-Org/Krea-2/loras](https://huggingface.co/Comfy-Org/Krea-2/tree/main/loras). Place the `.safetensors` files in `ComfyUI/models/loras/`.

| LoRA                   | Trigger Words                        | Recommended Strength |
|------------------------|--------------------------------------|-------|
| `krea2_darkbrush`      | `monochrome ink wash style`          | `1.0` |
| `krea2_dotmatrix`      | `monochrome stippling style`         | `1.0` |
| `krea2_kidsdrawing`    | `naive expressive sketch style`      | `1.0` |
| `krea2_neondrip`       | `textured abstract style`            | `1.0` |
| `krea2_rainywindow`    | `rainy window style`                 | `1.0` |
| `krea2_retroanime`     | `purple retro anime style`           | `1.0` |
| `krea2_softwatercolor` | `art deco watercolor style`          | `1.0` |
| `krea2_sunsetblur`     | `ethereal motion blur style`         | `1.0` |
| `krea2_vintagetarot`   | `vintage tarot style`                | `1.0` |

---

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**diffusion_models**


**text_encoders**


**vae**


**loras**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   ├── 📂 text_encoders/
│   ├── 📂 vae/
│   └── 📂 loras/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/comfyanonymous/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

Guide: [krea-2](https://docs.comfy.org/tutorials/image/krea/krea-2)

This workflow generates images with **Krea-2 Turbo**, a fast distilled text-to-image model. The workflow is organized into a few parts: each handles a different step so you can generate quickly without digging through every node.

## Text to Image (Krea-2 Turbo) Subgraph

Double-click this node to open the full pipeline. Inside, the canvas is grouped into several areas:

**Models**: Loads the diffusion model, text encoder, VAE, and optional style LoRA (`LoraLoaderModelOnly`).

**Prompt**: Enter your image description in **Text String (User Prompt)**.

**Prompt Enhancement**: Expands your prompt before generation. Enabled by default (`prompt_enhance`). You can turn it off to use your prompt as-is, or replace the built-in module with **OpenAI** or **Gemini** API nodes.

**Feature Switch**: Quick toggles on the left side of the subgraph:
- `prompt_enhance`: enable or disable prompt expansion
- `enable_lora?`: enable or disable the style LoRA

**Image Generation**: Handles latent sizing, sampling (8 steps), and VAE decode to produce the final image.

When using a LoRA, set `enable_lora?` to true, select the matching file in **LoraLoaderModelOnly**, and adjust `lora_strength` as needed.

## LoRA & Trigger Word (CustomCombo)

On the main canvas, the **CustomCombo** node is where you choose which style LoRA you are using (e.g. `krea2_coolblue`, `krea2_darkbrush`). The workflow uses your selection to automatically append the correct **trigger word** to your prompt.

- Download LoRA files from [Comfy-Org/Krea-2/loras](https://huggingface.co/Comfy-Org/Krea-2/tree/main/loras) and place them in `ComfyUI/models/loras/`
- Select the LoRA name that matches the file loaded inside the subgraph
- The trigger word is applied for you: no need to type it manually
- For trigger words and recommended strength values, see the **LoRA Trigger Words and Settings** note beside this workflow
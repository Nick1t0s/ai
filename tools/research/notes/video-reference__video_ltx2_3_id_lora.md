- Github: [LTX-2](https://github.com/Lightricks/LTX-2)
- [ID LoRA](https://github.com/ID-LoRA/ID-LoRA/tree/main)
## Report LTX-2.3 Issues
To report any issues when running this workflow, [go to GitHub](https://github.com/Lightricks/ComfyUI-LTXVideo/issues)

## Model Links

**checkpoints**


**loras**


**text_encoders**


**latent_upscale_models**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 checkpoints/
│   ├── 📂 loras/
│   ├── 📂 text_encoders/
│   └── 📂 latent_upscale_models/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud updates follow stable releases, so some nightly-supported models may not be available yet.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/Comfy-Org/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

ID-LoRA uses a structured prompt with three tagged sections:

```
[VISUAL]: <scene and appearance description>
[SPEECH]: <exact words the person should say>
[SOUNDS]: <speaker vocal style + ambient/environmental sounds>
```

| Section | What to write | Example |
|---------|--------------|---------|
| `[VISUAL]` | Shot type, subject appearance, clothing, setting, lighting, actions | *A medium shot of a woman with short black hair wearing a white blouse, standing in a modern kitchen with warm lighting and speaking calmly.* |
| `[SPEECH]` | The literal words to be spoken | *Hello everyone, welcome to our channel.* |
| `[SOUNDS]` | Speaker vocal qualities (volume, tone, distance from mic) and background sounds | *The speaker has a calm, conversational tone at moderate volume, close to the microphone. Soft birds chirping in the background.* |

**Full example:**

```
[VISUAL]: A medium shot features a young man with curly brown hair and light blue eyes, sitting on a beige couch. He is wearing a light blue shirt and a red patterned tie. His mouth is slightly open as he speaks. In the background, there is a blurry room with warm lighting.
[SPEECH]: We are proud to introduce ID-LoRA.
[SOUNDS]: The speaker has a moderate volume and a conversational tone, sounding engaged and natural. They are close to the microphone. Light, instrumental background music plays softly, creating a calm atmosphere.
```

**Tips:**
- Be descriptive in `[VISUAL]` — shot type, colors, clothing, and background details all help, mention that the person is speaking to avoid voice-overs.
- `[SPEECH]` should contain the exact transcript, not a summary.
- `[SOUNDS]` controls both the speaking style (tone, volume, mic proximity) and ambient sounds (music, nature, room noise). Describing these steers the audio generation.

---

Record your own voice and use it as the reference audio.
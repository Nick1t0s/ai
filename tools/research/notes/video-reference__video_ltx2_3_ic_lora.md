- Github: [LTX-2](https://github.com/Lightricks/LTX-2)

## LTX-2.3 Prompting Tips

1. **Core Actions**: Describe events and actions as they occur over time  
2. **Visual Details**: Describe all visual details you want to appear in the video  
3. **Audio**: Describe sounds and dialogue needed for the scene

## Report LTX-2.3 Issues
To report any issues when running this workflow, [go to GitHub](https://github.com/Lightricks/ComfyUI-LTXVideo/issues)

Guide: [Subgraph](https://docs.comfy.org/interface/features/subgraph)

## Model Links

**checkpoints**


**text_encoders**


**loras**


**geometry_estimation**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 checkpoints/
│   ├── 📂 text_encoders/
│   ├── 📂 loras/
│   └── 📂 geometry_estimation/
```

---

## IC-LoRA

### What This Model Is

### What It Can Do
- Guide generation with aligned control frames while still following the text prompt.
- Preserve the structure and motion hinted by the control sequence.
- Work well for reference-driven video generation where timing matters.

### Inputs Used In This Workflow
- `first_frame`: sets the starting appearance and composition.
- `control_images`: the aligned control sequence used by IC-LoRA guidance.
- `prompt`: describes the subject, motion, and scene.
- `prompt_enhance`: rewrites or expands the prompt text before sampling.
- `ckpt_name`: selects the base LTX-2.3 checkpoint.
- `ic_lora`: selects the IC-LoRA weights.
- `lora_strength`: controls how strongly the IC-LoRA guide is followed.
- `fps`: controls output playback rate.

### Workflow Usage Notes
- In this workflow, `control_images` comes from the video preprocessing branch and is used as the IC-LoRA guide.
- This depth-guided setup is only one example. Users can swap in other preprocessors and other control types as long as they produce frame-aligned `control_images`.
- Different preprocessors emphasize different guidance signals, for example depth for structure, pose for body motion, or edge-based controls for contours.
- Keep `control_images` temporally aligned with the motion you want to generate.
- `lora_strength` higher: stronger guide following. Lower: more freedom from the guide.
- `prompt_enhance` changes the prompt text only. It does not change guide timing or frame count.
- All model download links are listed in the `Model Links` note.

### Length Control
- The generated video length is controlled by the video node branch, especially the `LoadVideo` / `Video Slice` path that provides the control sequence.
- To change the generated duration, change the source control video or the slice length in that video branch.
- Changing `ic_lora`, `lora_strength`, or `prompt_enhance` will not change the number of guided frames.
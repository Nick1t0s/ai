Each **Video Extend** group will extend 81/25=3.24s

So, if you want the output video to match the length of the input audio. For example, if your input audio is 9 seconds in total.

1. You need to manually box-select this Video Extend group. 
2. Press Ctrl-C, then Ctrl-Shift-V, to duplicate a new extend module.
3. Then linking the Previous `InfiniteTalk (Base Generation)`'s IMAGE output to the new **WanInfiniteTalkToVideo** node's `previous_frames`
4. Linking the Batch Images node's IMAGE output to the new Batch Images node's image1

---

## Model Links

**diffusion_models**


**text_encoders**


**model_patches**


**audio_encoders**


**vae**


**loras**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   ├── 📂 text_encoders/
│   ├── 📂 model_patches/
│   ├── 📂 audio_encoders/
│   ├── 📂 vae/
│   ├── 📂 loras/
```

## Report Issue

Note: Please update ComfyUI first ([guide](https://docs.comfy.org/installation/update_comfyui)) and prepare required models. Desktop/Cloud will be updated after the stable release; nightly-supported models may not be included yet, please wait for the next stable release.

- Cannot run / runtime errors: [ComfyUI/issues](https://github.com/Comfy-Org/ComfyUI/issues)
- UI / frontend issues: [ComfyUI_frontend/issues](https://github.com/Comfy-Org/ComfyUI_frontend/issues)
- Workflow issues: [workflow_templates/issues](https://github.com/Comfy-Org/workflow_templates/issues)

---

- Upload the start frame, then right - click on the Load Image node and choose **[Open in MaskEditor](https://docs.comfy.org/interface/maskeditor)**.
- Use the brush to draw the mask for Character 1.
- For Character 2, you need to do the same thing: upload the first frame and draw a mask.
## LTX-2 Prompting Tips

1. **Core Actions**: Describe events and actions as they occur over time  
2. **Visual Details**: Describe all visual details you want to appear in the video  
3. **Audio**: Describe sounds and dialogue needed for the scene

## Report LTX-2 Issues
To report any issues when running this workflow, [go to GitHub](https://github.com/Lightricks/ComfyUI-LTXVideo/issues)

## Model Links

**checkpoints**


**text_encoders**


**loras**



## Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 checkpoints/
│   ├── 📂 text_encoders/
│   └── 📂 loras/
```

---

# Trigger Word
zhuanchang

If needed, place the trigger word near the end of the prompt so the base prompt still clearly describes:
- subject
- scene
- camera movement
- transformation behavior
- atmosphere

# Prompting Guide
For best results, prompts should usually contain:
1. Shot description
   Example: close-up, medium shot, wide shot, low-angle, tracking shot.
2. Subject and environment
   Describe the character, object, or scene as clearly as possible.
3. Motion or transformation process
   Explain what changes over time: identity, style, object form, scene layout, or camera trajectory.
4. Visual details
   Add texture, lighting, color, material, and spatial cues.
5. Ending trigger
   Add zhuanchang when you want the LoRA behavior to activate more strongly.
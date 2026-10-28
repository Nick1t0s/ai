Stupid hack to fix the first frame being overbaked by the VAE, double the first frame and remove it after decoding.

---

## Batch sizes
Batch sizes depend on how many Video S2V Extend subgraphs you have added to the workflow.

Each Video S2V Extend subgraph will add 77 frames to the final output.

Example:

If you added 1 Video S2V Extend subgraph, you should set the batch size to 2.

We added 2 Video S2V Extend subgraphs, so the batch size value is 3.

## Chunk length

77 is the default length from the WAN2.2S2V official code. This model needs at least 73 frames. If you set the value too high, it might cause an out-of-memory issue.

So you can just leave 77 as it is.

---

If you need longer video output, just select one subgraph below, then use Ctrl+C and Ctrl+Shift+V to copy and paste the Video S2V Extend subgraph. Each of them will extend the other frames you set to the chunk length; by default, it's 77 frames.

---

Stupid hack to fix the first frame being overbaked by the VAE, double the first frame and remove it after decoding.

---

## Batch sizes
Batch sizes depend on how many Video S2V Extend subgraphs you have added to the workflow.

Each Video S2V Extend subgraph will add 77 frames to the final output.

Example:

If you added 1 Video S2V Extend subgraph, you should set the batch size to 2.

We added 2 Video S2V Extend subgraphs, so the batch size value is 3.

## Chunk length

77 is the default length from the WAN2.2S2V official code. This model needs at least 73 frames. If you set the value too high, it might cause an out-of-memory issue.

So you can just leave 77 as it is.

---

| model            | Steps | cfg |
|---------------------|---------------|---------------|
| With 4 steps lightning LoRA            | 4                | 1.0               |
| Without 4 Steps lightning LoRA    | 20               | 6.0               |

---

| model            | Steps | cfg |
|---------------------|---------------|---------------|
| With 4 steps lightning LoRA            | 4                | 1.0               |
| Without 4 Steps lightning LoRA    | 20               | 6.0               |

---

This is the 20-step workflow. We put it here in case some users don't know how to modify the workflow that with Wan2.2 lightning LoRA. If you want to enable it, box-select the workflow and then use Ctrl+B to enable it.

---

Tested all wan2.2 lightning LoRAs; all worked, but many keys didn't match. However, because it reduces generation time a lot, we added this lightning model. If you find the output quality is too bad, you can try the 20 steps workflow without lightning LoRA.

---

[Tutorial](https://docs.comfy.org/tutorials/video/wan/wan2-2-s2v
) 

**diffusion_models**       

**audio_encoders**

**vae**

**text_encoders**   


```
ComfyUI/
├───📂 models/
│   ├───📂 diffusion_models/
│   ├───📂 text_encoders/
│   ├───📂 audio_encoders/ # Create one if you can't find this folder
│   └───📂 vae/
```
## 🎤 Achieving High-Quality Voice Clones

To achieve the best voice cloning results, providing an accurate `prompt_text` is **critical**. This text acts as a transcript that aligns the sound of the `prompt_audio` with the words being spoken, teaching the model the speaker's unique vocal characteristics.

### How to Use `prompt_text` Effectively

#### 1. **Provide a Verbatim Transcript**
The `prompt_text` must be a word-for-word transcript of the `prompt_audio`. Do not summarize or describe the audio.

✅ **Correct:** `The quick brown fox jumps over the lazy dog.`

❌ **Incorrect:** `A person saying a sentence about a fox.`

#### 2. **Punctuation is Important**
Use accurate punctuation to capture the speaker's intonation. The model learns how the speaker ends sentences, asks questions, or shows excitement.

-   **For a statement:** `This is a great example.`
-   **For a question:** `Is this a great example?`
-   **For excitement:** `This is a great example!`

#### 3. **Match Audio and Text Length**
The audio clip should be long enough to capture the speaker's natural pacing and rhythm.

👍 **Good:** A 5-15 second clip of continuous, clear speech.

👌 **Okay:** A 3-5 second clip.

⚠️ **Warning:** Very short clips (< 3 seconds) may result in a less stable or robotic-sounding clone.


> **Note:**
> For the best results, use a clean, high-quality `prompt_audio` with minimal background noise, reverb, or music. The model will try to clone the *entire* acoustic environment, not just the voice.

---

# ComfyUI-VoxCPM

**VoxCPM**  a novel tokenizer-free TTS system for context-aware speech generation and true-to-life voice cloning.

## Models
This node automatically downloads the required model files.

| Model | Parameters | Sampling Rate | Languages | Description | Hugging Face Link |
|:---|:---:|:---:|:---:|:---|:---|
| **VoxCPM2** | 2B | 48kHz | 30+ | **New!** Voice design, reference cloning, multilingual | [openbmb/VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) |
| **VoxCPM1.5** | 800M | 44.1kHz | 2 | Recommended for v1. LoRA support, improved fidelity | [openbmb/VoxCPM1.5](https://huggingface.co/openbmb/VoxCPM1.5) |
| VoxCPM-0.5B | 640M | 16kHz | 2 | Original version | [openbmb/VoxCPM-0.5B](https://huggingface.co/openbmb/VoxCPM-0.5B) |


---

### Check TG for more interesting stuff: [TokenDiffusion](https://t.me/TokenDiff)

---

## VoxCPM2 (48 кГц, 30+ языков)

- Просто текст → речь: пиши в `text`, голос выбирается моделью сам.
- **Голос по описанию:** опиши его в `voice_design` (например, «молодая женщина, тёплый спокойный голос»).
- **Клон голоса:** узлы LoadAudio и VoxCPM Voice Cloning выключены. Загрузи образец, впиши его точный текст в `prompt_text`, включи оба узла (Ctrl+B).

cfg 2, steps 10. Модель: `models/tts/VoxCPM/VoxCPM2/`.
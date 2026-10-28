# VoxCPM LoRA Training Guide

This guide explains the parameters for fine-tuning VoxCPM v1.5 models using LoRA (Low-Rank Adaptation) within ComfyUI.

## 1. Data Preparation (Dataset Maker)
*   **Audio Directory**: Path to a folder containing pairs of `.wav` audio files and `.txt` transcripts (filenames must match, e.g., `001.wav` & `001.txt`).
*   **Output Filename**: Name of the generated manifest (default: `train.jsonl`).

## 2. Configuration (Train Config)

### Core Parameters
*   **Learning Rate**: Controls how fast the model learns. Default `1e-4`. Lower values (e.g., `5e-5`) are safer for small datasets; higher values (e.g., `2e-4`) learn faster but may be unstable.
*   **LoRA Rank (r)**: The "capacity" of the fine-tune.
    *   `32` (Default): Good balance for voice cloning.
    *   `64-128`: Higher fidelity but uses more VRAM and disk space.
    *   `8-16`: Lower VRAM, sufficient for simple style changes.
*   **LoRA Alpha**: Scaling factor. Usually set to `Rank / 2` or `Rank`. Higher alpha = stronger LoRA influence.
*   **Batch Size (Max Tokens)**: Instead of a fixed batch size, VoxCPM uses `Max Batch Tokens` (default `8192`) to dynamically batch audio of varying lengths. Reduce to `4096` if hitting OOM.

### Architecture Targeting
*   **Enable LM LoRA**: (Default: True) Adapts the Language Model (semantic understanding/prosody). Critical for text adherence.
*   **Enable DiT LoRA**: (Default: True) Adapts the Diffusion Transformer (acoustic details/timbre). Critical for voice likeness.
*   **Enable Proj LoRA**: (Default: False) Adapts projection layers. Generally not needed unless the base model and target voice are extremely different.

### Optimization
*   **Grad Accum Steps**: Simulates a larger batch size. `1` is standard. Increase (e.g., `4`) if training is unstable.
*   **Warmup Steps**: Number of steps to ramp up learning rate. `100` is standard. Prevents early "shock" to the model.

## 3. Training Execution (LoRA Trainer)
*   **Max Steps**: Total training duration.
    *   `1000-2000`: Often sufficient for single-speaker cloning (10-20 mins of data).
    *   `5000+`: For larger datasets or complex styles.
*   **Save Every Steps**: Frequency of saving checkpoints.
*   **Num Workers**: Data loading threads. Set to `0` if experiencing crashes; `2-4` speeds up data loading.
*   **Output Name**: Subfolder name in `models/loras` where results will be saved.

## Tips for Success
1.  **Dataset Quality**: 15-30 minutes of clean, high-quality audio is better than hours of noisy audio.
2.  **Transcripts**: Ensure text matches audio exactly. Mismatches confuse the model.
3.  **Monitoring**: Watch the Loss in the console. It should generally decrease. If it stays at `0.000`, something is wrong (check console for `grad_fn` warnings). If it explodes (NaN), lower the Learning Rate.
# Qwen3-TTS-0.6/1.7 Fine-Tuning
- audio_folder: Path to audio dataset
- output_dir: Path to save fine-tuned model
- speaker_name: Speaker name (similar to built-in voices like custom_voice)
- test_text: Sample audio text content (currently not implemented for training samples)
- learning_rate: Learning rate, recommended 2e-5/2e-6
- num_epochs: Number of training epochs
- batch_size: Default 1 (16G test may cause OOM)
- gradient_accumulation_steps: Gradient accumulation, trading time for space
- validate_every: Validation frequency, saving model and generating test audio every X epochs (currently not implemented)

---

# Qwen3-TTS-0.6/1.7微调
- audio_folder: 音频数据集路径
- output_dir: 微调模型保存路径
- speaker_name: speaker名字(类似custom_voice的内置语音)
- test_text: 采样音频文本内容(目前训练采样未实现)|
- learning_rate: 学习率,推荐2e-5/2e-6
- num_epochs: 训练轮数
- batch_size: 默认1(16G测试2会OOM)
- gradient_accumulation_steps: 梯度累积,时间换空间
- validate_every: 验证频率,每训练多少个 Epoch 就保存一次模型并生成一次测试音频(当前未实装)

---

```
从custom_model_path和custom_speaker_name输出微调的模型路径和speaker_name即可生成音频,但是目前不支持指令控制,官方未放出相关训练代码
```
```
Output the fine-tuned model path and speaker_name from custom_model_path and custom_speaker_name to generate audio. However, command control is currently unsupported, and the official training code has not been released.
```
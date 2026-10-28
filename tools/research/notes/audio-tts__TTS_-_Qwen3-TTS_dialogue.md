## Диалог (Qwen3-TTS)

Три **Voice Design** создают голоса (Анна, Максим, Рассказчик), **Voice Clone Prompt** делает из них образцы, **Role Bank** связывает имя роли с голосом. В сценарии каждая строка — `Имя: реплика`, имена как в Role Bank.

- `pause_linebreak` — пауза после каждой строки;
- `period_pause`, `comma_pause`, `question_pause`, `hyphen_pause` — после «.», «,», «?», «-».

Вместо Voice Design можно подать сохранённые голоса: узлы **Load Speaker** выключены, включи их (Ctrl+B) после сохранения голоса в workflow «TTS - Qwen3-TTS save voice».
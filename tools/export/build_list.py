"""Список на экспорт: готовые шаблоны + свои workflow + примеры из репозиториев нод, с категорией и именем файла."""
import json, os, re, sys

ROOT = os.path.expanduser('~/ai/comfyui')
TPL = ROOT + '/venv/lib/python3.11/site-packages/comfyui_workflow_templates_json/templates'
WF = ROOT + '/user/default/workflows'
CN = ROOT + '/custom_nodes'
OUT = sys.argv[1]

CAT = {
    'image-photo': """image_z_image_turbo image_z_image_turbo_fun_union_controlnet image_z_image_turbo_int8 image_z_image
        image_krea2_turbo_t2i_int8 image_krea2_turbo_int8_image_style_reference image_qwen_Image_2512
        image_qwen_image_2512_with_2steps_lora template_qwen_Image_2512_360_lora image_qwen_Image_2512_controlnet
        flux1_krea_dev image_chroma_text_to_image image_ideogram4_t2i_int8 image_mage_flow_t2i_int8
        image_mage_flow_turbo_t2i_int8 image_kandinsky5_t2i image_flux2_klein_text_to_image""",
    'image-anime': """image_anima_base_v1 image_anima_lllite_any_control_to_image image_anima_lllite_depth_control_to_image
        image_netayume_lumina_t2i image_newbieimage_exp0_1-t2i template_qwen_image_illustration_lora""",
    'image-edit': """image_qwen_image_edit_2511 image_qwen_image_edit_2509 templates-1_click_multiple_scene_angles-v1.0
        templates-image_to_real templates_rob_portrait_light_migration.app templates-portrait_light_migration
        image_qwen_image_edit_2509_relight flux_kontext_dev_basic image_flux2_klein_image_edit_4b_base
        image_flux2_klein_image_edit_4b_distilled image_mage_flow_edit_int8 image_mage_flow_edit_turbo_int8
        image_anima_lllite_image_inpainting video_bernini_r_image_editing""",
    'video': """video_wan2_2_14B_i2v video_wan2_2_14B_t2v video_wan2_2_14B_flf2v templates-6-key-frames
        video_ltx2_3_i2v video_ltx2_3_t2v video_ltx2_3_flf2v video_ltx2_3_ia2v template_ltx2_3_style_transition
        video_minimax_h3_i2v video_minimax_h3_t2v video_minimax_h3_i2v_continuation
        video_hunyuan_video_1.5_720p_i2v video_hunyuan_video_1.5_720p_t2v video_wan2_2_5B_ti2v
        video_kandinsky5_t2v video_kandinsky5_i2v""",
    'video-reference': """video_minimax_h3_r2v video_wan_animate2 video_wan21_scail2_character_replacement_int8
        video_wan2_2_14B_s2v video_wan2_1_infinitetalk video_bernini_r_video_editing utility_void_video_inpainting
        template_ltx2_3_ic_lora_ingredients video_ltx2_3_id_lora video_ltx2_3_ic_lora""",
    'audio-music': 'audio_ace_step1_5_xl_turbo audio_ace_step1_5_xl_sft audio_minimax_music_3',
    'audio-sound': 'audio_stable_audio_3_medium',
    'utility': """utility_seedvr2_3b_int8_upscale_video utility_seedvr2_7b_int8_upscale_image utility_seedvr2_3b_int8_upscale_image
        utility_video_frame_interpolation utility_image_segment_sam3 utility_video_segment_sam3
        utility_birefnet_remove_background utility_sdpose_ood_image_to_pose utility_sdpose_ood_video_to_pose_map
        utility-gan_upscaler utility_depth_anything3_image_depth_estimation utility_depth_anything3_video_depth_estimation
        utility_image_stitch utility_interpolation_image_upscale utility_moge_depth_estimation
        utility_z_image_turbo_2k_upscaler.app basic_datatype_conversion basic_image_color_adjustment
        basic_mask_operations_and_compositing""",
    'llm': 'llm_qwen3_5_text_gen llm_qwen3_text_gen llm_qwen3vl_text_gen',
    '3d': """3d_pixal3d_trellis2_image_to_model 3d_hunyuan3d-v2.1 3d_hunyuan3d_image_to_model
        3d_hunyuan3d_multiview_to_model 3d_hunyuan3d_multiview_to_model_turbo
        3d_triposplat_image_to_gaussian_splat 3d_moge_panorama_to_mesh 3d_moge_perspective_to_mesh""",
}
OWN = {
    'AnimeGen-I2V (Wan 2.2).json': 'video',
    'NoobAI-XL V-pred (anime).json': 'image-anime',
    'SDXL Anime (Illustrious - NoobAI - Animagine).json': 'image-anime',
    'SDXL Photo (RealVis - Juggernaut).json': 'image-photo',
    'Qwen Edit 2511 - INFL8 Inflation (fp8).json': 'image-edit',
    'Qwen Edit 2511 - Multiple Character Angles (fp8).json': 'image-edit',
    'Qwen Edit 2511 - SYSTMS Action (fp8).json': 'image-edit',
    'TTS - Fish Audio S2 Pro.json': 'audio-tts',
    'TTS - Qwen3-TTS (clone, design, custom).json': 'audio-tts',
    'TTS - Qwen3-TTS dialogue.json': 'audio-tts',
    'TTS - Qwen3-TTS save voice.json': 'audio-tts',
    'TTS - VoxCPM2.json': 'audio-tts',
    'TTS - Chatterbox Multilingual (RU).json': 'audio-tts',
    'Music - HeartMuLa 3B.json': 'audio-music',
    'Video to Audio - HunyuanVideo-Foley.json': 'audio-sound',
    'Video to Audio - MMAudio.json': 'audio-sound',
    'Upscale - SeedVR2 7B Sharp fp16 (фото).json': 'utility',
    'Upscale - SeedVR2 7B (видео).json': 'utility',
    'Upscale - Фото 4K (Z-Image + SeedVR2 7B).json': 'utility',
    'Upscale - Аниме hires-fix (Illustrious).json': 'utility',
}
# Примеры из репозиториев нод, у которых нет моей исправленной копии
UPSTREAM = [
    ('HeartMuLa_ComfyUI/example workflows/Lyrics Transcriber.json', 'audio-music', 'HeartMuLa - распознавание текста песни'),
    ('ComfyUI-Qwen-TTS/example/Model Fine-Tuning and Workflow Usage.json', 'training', 'Qwen3-TTS - дообучение голоса'),
    ('ComfyUI-VoxCPM/example_workflows/VoxCPM-lora-training.json', 'training', 'VoxCPM - обучение LoRA'),
]

titles = {}
for c in json.load(open(TPL + '/index.ru.json')):
    for t in c['templates']:
        titles[t['name']] = t.get('title') or t['name']
# там, где перевод в индексе неудачный или без имени модели
titles.update({
    'image_qwen_Image_2512_controlnet': 'Qwen-Image 2512 Fun Union ControlNet',
    'video_minimax_h3_i2v_continuation': 'MiniMax H3 продолжение видео',
    'templates-6-key-frames': 'Wan 2.2 14B ключевые кадры (склейка FLF-сегментов)',
    'templates-1_click_multiple_scene_angles-v1.0': 'Qwen Edit 2509 - ракурсы сцены одним кликом',
    'templates-image_to_real': 'Qwen Edit 2509 - иллюстрация в реализм',
    'templates_rob_portrait_light_migration.app': 'Qwen Edit 2509 - переосвещение портрета (app)',
    'templates-portrait_light_migration': 'Qwen Edit 2509 - перенос освещения на портрет',
    'image_qwen_image_edit_2509_relight': 'Qwen Edit 2509 - переосвещение фото',
    'image_qwen_image_edit_2509': 'Qwen Edit 2509 - редактирование изображения',
    'image_qwen_image_edit_2511': 'Qwen Edit 2511 - замена материала',
    'image_flux2_klein_image_edit_4b_base': 'Flux.2 Klein 4B - редактор изображений',
    'image_flux2_klein_image_edit_4b_distilled': 'Flux.2 Klein 4B Distilled - редактор изображений',
    'image_flux2_klein_text_to_image': 'Flux.2 Klein 4B - текст в изображение',
    'utility_video_frame_interpolation': 'Интерполяция кадров видео',
    'utility-gan_upscaler': 'GAN-апскейлер видео (быстрый)',
    'utility_interpolation_image_upscale': 'Апскейл изображения интерполяцией (без нейросети)',
    'utility_image_stitch': 'Сшивание изображений в сетку 2x2',
    'basic_image_color_adjustment': 'Основы - коррекция цвета',
    'basic_datatype_conversion': 'Основы - преобразование типов данных',
    'basic_mask_operations_and_compositing': 'Основы - маски и композитинг',
    'llm_qwen3_text_gen': 'Qwen3 Генерация текста',
})


def clean(s):
    s = re.sub(r'[\\/:*?"<>|]', ' ', s).replace('\n', ' ')
    return re.sub(r'\s+', ' ', s).strip().rstrip('.')


items, seen = [], set()
for cat, names in CAT.items():
    for n in names.split():
        assert os.path.exists(f'{TPL}/{n}.json'), n
        assert n not in seen, n
        seen.add(n)
        items.append({'src': f'{TPL}/{n}.json', 'cat': cat, 'kind': 'template', 'id': n, 'name': clean(titles.get(n, n))})
for f, cat in OWN.items():
    assert os.path.exists(f'{WF}/{f}'), f
    items.append({'src': f'{WF}/{f}', 'cat': cat, 'kind': 'own', 'id': f[:-5], 'name': clean(f[:-5])})
FIXED = os.path.join(os.path.dirname(OUT), 'fixed')
os.makedirs(FIXED, exist_ok=True)
for rel, cat, name in UPSTREAM:
    w = json.load(open(f'{CN}/{rel}'))
    # ноды вывода текста из неустановленных паков -> встроенный PreviewAny
    for n in w['nodes']:
        if n['type'] in ('ShowText|pysssss', 'easy showAnything'):
            n['type'] = 'PreviewAny'
            n['inputs'][0].update(name='source', type='*')
            n['outputs'] = []
            n['properties'] = {'cnr_id': 'comfy-core', 'Node name for S&R': 'PreviewAny'}
            n['widgets_values'] = []
    src = os.path.join(FIXED, os.path.basename(rel))
    json.dump(w, open(src, 'w'), ensure_ascii=False, indent=1)
    it = {'src': src, 'cat': cat, 'kind': 'upstream', 'id': rel, 'name': clean(name)}
    if all(n.get('mode') == 4 or n['type'] in ('MarkdownNote', 'Note') for n in w['nodes']):
        # пример целиком выключен (bypass); в API-копии ноды включены, иначе она пустая
        for n in w['nodes']:
            n['mode'] = 0
        it['api_src'] = src[:-5] + '.enabled.json'
        json.dump(w, open(it['api_src'], 'w'), ensure_ascii=False, indent=1)
    items.append(it)

# одинаковые русские названия внутри категории различаем id шаблона
by = {}
for it in items:
    by.setdefault((it['cat'], it['name'].lower()), []).append(it)
for group in by.values():
    if len(group) > 1:
        for it in group:
            it['name'] = f"{it['name']} ({it['id']})"
# авторский workflow NetaYume (Tensor.Art) под локальный чекпоинт
items.append({'src': os.path.join(FIXED, 'netayume_tensorart.json'), 'cat': 'image-anime', 'kind': 'external',
              'id': 'duongve/NetaYume-Lumina-Image-2.0/Lumina_image_v2_tensorart_workflow.json',
              'name': 'NetaYume Lumina - авторские настройки (Tensor.Art)'})
json.dump(items, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(items), {c: sum(i['cat'] == c for i in items) for c in dict.fromkeys(i['cat'] for i in items)})

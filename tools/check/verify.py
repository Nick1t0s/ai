"""Проверка: у каждого выбранного шаблона и своего workflow все модели на месте; файлы манифестов докачаны."""
import json, os, glob, sys

TPL = os.path.expanduser('~/ai/comfyui/venv/lib/python3.11/site-packages/comfyui_workflow_templates_json/templates')
MD = os.path.expanduser('~/ai/comfyui/models')
WF = os.path.expanduser('~/ai/comfyui/user/default/workflows')
DL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manifests')
ALIAS = {'clip': 'text_encoders', 'unet': 'diffusion_models'}

have = set()
for root, _, files in os.walk(MD, followlinks=True):
    for f in files:
        top, _, rest = os.path.relpath(os.path.join(root, f), MD).partition('/')
        have.add((ALIAS.get(top, top), rest))

TEMPLATES = """image_z_image_turbo utility_z_image_turbo_2k_upscaler.app image_z_image_turbo_fun_union_controlnet image_z_image_turbo_int8
image_krea2_turbo_t2i_int8 image_krea2_turbo_int8_image_style_reference image_qwen_Image_2512 image_qwen_image_edit_2511
image_anima_base_v1 image_anima_lllite_any_control_to_image image_anima_lllite_image_inpainting image_anima_lllite_depth_control_to_image
image_netayume_lumina_t2i video_wan2_2_14B_i2v video_wan2_2_14B_t2v video_wan2_2_14B_flf2v templates-6-key-frames
video_ltx2_3_i2v video_ltx2_3_t2v video_ltx2_3_flf2v video_ltx2_3_ia2v template_ltx2_3_ic_lora_ingredients video_ltx2_3_id_lora
video_ltx2_3_ic_lora template_ltx2_3_style_transition video_wan_animate2 video_minimax_h3_i2v video_minimax_h3_t2v video_minimax_h3_r2v
utility_seedvr2_3b_int8_upscale_video utility_seedvr2_7b_int8_upscale_image utility_seedvr2_3b_int8_upscale_image utility_video_frame_interpolation
audio_ace_step1_5_xl_turbo audio_ace_step1_5_xl_sft audio_minimax_music_3 audio_stable_audio_3_medium
flux1_krea_dev image_chroma_text_to_image image_z_image image_ideogram4_t2i_int8 image_mage_flow_t2i_int8 image_mage_flow_turbo_t2i_int8
image_kandinsky5_t2i image_qwen_image_2512_with_2steps_lora template_qwen_Image_2512_360_lora image_qwen_Image_2512_controlnet
flux_kontext_dev_basic image_qwen_image_edit_2509 templates-1_click_multiple_scene_angles-v1.0 templates-image_to_real
templates_rob_portrait_light_migration.app templates-portrait_light_migration image_qwen_image_edit_2509_relight
image_flux2_klein_image_edit_4b_base image_flux2_klein_image_edit_4b_distilled image_flux2_klein_text_to_image
image_mage_flow_edit_int8 image_mage_flow_edit_turbo_int8 image_newbieimage_exp0_1-t2i
video_hunyuan_video_1.5_720p_i2v video_hunyuan_video_1.5_720p_t2v video_wan2_2_5B_ti2v video_wan21_scail2_character_replacement_int8
video_wan2_2_14B_s2v video_kandinsky5_t2v video_kandinsky5_i2v video_bernini_r_video_editing video_bernini_r_image_editing
utility_void_video_inpainting video_wan2_1_infinitetalk
utility_image_segment_sam3 utility_video_segment_sam3 utility_birefnet_remove_background utility_sdpose_ood_image_to_pose llm_qwen3_5_text_gen""".split()


def models(w):
    nodes = w.get('nodes', []) + [n for sg in (w.get('definitions') or {}).get('subgraphs', []) for n in sg['nodes']]
    out = set()
    for n in nodes:
        for m in (n.get('properties') or {}).get('models') or []:
            out.add((ALIAS.get(m['directory'], m['directory']), m['name']))
        if n['type'] == 'CheckpointLoaderSimple' and n.get('widgets_values'):
            out.add(('checkpoints', n['widgets_values'][0]))
    return out


bad = 0
for name in TEMPLATES:
    miss = [m for m in models(json.load(open(os.path.join(TPL, name + '.json')))) if m not in have]
    print('OK  ' if not miss else 'MISS', name, *miss)
    bad += bool(miss)
for p in sorted(glob.glob(os.path.join(WF, '*.json'))):
    miss = [m for m in models(json.load(open(p))) if m not in have]
    print('OK  ' if not miss else 'MISS', '[workflow]', os.path.basename(p), *miss)
    bad += bool(miss)
# файлы custom nodes и всё из манифестов: размер совпадает
for mf in ('manifest.json', 'manifest_repos.json', 'manifest3.json', 'manifest3_repos.json'):
    for x in json.load(open(os.path.join(DL, mf))):
        p = os.path.join(MD, x['rel'])
        if not x.get('present') and (not os.path.exists(p) or os.path.getsize(p) != x['size']):
            print('MISS file', x['rel']); bad += 1
left = glob.glob(MD + '/**/*.part', recursive=True) + glob.glob(MD + '/**/*.badsha', recursive=True)
print('недокачанные/битые:', left)
print('ИТОГО проблем:', bad + len(left))

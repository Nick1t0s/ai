import os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

MODELS_DIR = '/home/nik/ai/comfyui/models'

DOWNLOADS = [
    # TripoSplat
    ('vae', 'triposplat_vae_decoder_fp16.safetensors',
     'https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/triposplat_vae_decoder_fp16.safetensors'),
    ('diffusion_models', 'triposplat_fp16.safetensors',
     'https://huggingface.co/VAST-AI/TripoSplat/resolve/main/diffusion_models/triposplat_fp16.safetensors'),
    ('clip_vision', 'dino_v3_vit_h.safetensors',
     'https://huggingface.co/VAST-AI/TripoSplat/resolve/main/clip_vision/dino_v3_vit_h.safetensors'),

    # Hunyuan3D v2.1
    ('checkpoints', 'hunyuan_3d_v2.1.safetensors',
     'https://huggingface.co/Comfy-Org/hunyuan3D_2.1_repackaged/resolve/main/hunyuan_3d_v2.1.safetensors'),

    # Hunyuan3D v2.0
    ('checkpoints', 'hunyuan3d-dit-v2_fp16.safetensors',
     'https://huggingface.co/Comfy-Org/hunyuan3D_2.0_repackaged/resolve/main/split_files/hunyuan3d-dit-v2_fp16.safetensors'),
    ('checkpoints', 'hunyuan3d-dit-v2-mv_fp16.safetensors',
     'https://huggingface.co/Comfy-Org/hunyuan3D_2.0_repackaged/resolve/main/split_files/hunyuan3d-dit-v2-mv_fp16.safetensors'),
    ('checkpoints', 'hunyuan3d-dit-v2-mv-turbo_fp16.safetensors',
     'https://huggingface.co/Comfy-Org/hunyuan3D_2.0_repackaged/resolve/main/split_files/hunyuan3d-dit-v2-mv-turbo_fp16.safetensors'),
]


def download_file(item):
    dir_name, filename, url = item
    target_dir = os.path.join(MODELS_DIR, dir_name)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, filename)
    part_path = target_path + '.part'

    req = urllib.request.Request(url, method='HEAD')
    with urllib.request.urlopen(req) as resp:
        remote_size = int(resp.headers.get('Content-Length', 0))

    if os.path.exists(target_path):
        local_size = os.path.getsize(target_path)
        if local_size == remote_size and remote_size > 0:
            print(f'[EXISTS] {dir_name}/{filename} ({local_size / 1e9:.2f} GB)', flush=True)
            return filename

    existing_bytes = 0
    if os.path.exists(part_path):
        existing_bytes = os.path.getsize(part_path)
        if existing_bytes > remote_size:
            existing_bytes = 0
            os.remove(part_path)

    headers = {}
    if existing_bytes > 0:
        headers['Range'] = f'bytes={existing_bytes}-'
        print(f'[RESUME] {dir_name}/{filename} from {existing_bytes / 1e9:.2f}/{remote_size / 1e9:.2f} GB', flush=True)
    else:
        print(f'[START] {dir_name}/{filename} ({remote_size / 1e9:.2f} GB)', flush=True)

    req = urllib.request.Request(url, headers=headers)
    mode = 'ab' if existing_bytes > 0 else 'wb'

    start_time = time.time()
    last_print = start_time
    downloaded = existing_bytes

    with urllib.request.urlopen(req) as resp, open(part_path, mode) as fp:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            fp.write(chunk)
            downloaded += len(chunk)
            now = time.time()
            if now - last_print >= 10:
                speed = (downloaded - existing_bytes) / (now - start_time) / 1e6
                pct = (downloaded / remote_size * 100) if remote_size else 0
                print(f'  [{filename[:25]}] {downloaded / 1e9:.2f}/{remote_size / 1e9:.2f} GB ({pct:.1f}%) @ {speed:.1f} MB/s', flush=True)
                last_print = now

    final_size = os.path.getsize(part_path)
    if remote_size > 0 and final_size != remote_size:
        raise RuntimeError(f'Downloaded size mismatch: {final_size} != {remote_size}')

    os.rename(part_path, target_path)
    total_time = time.time() - start_time
    print(f'[DONE] {dir_name}/{filename} in {total_time:.1f}s ({remote_size / 1e9:.2f} GB)', flush=True)
    return filename


def main():
    print(f'Starting parallel download (3 workers) of {len(DOWNLOADS)} models...', flush=True)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(download_file, item): item for item in DOWNLOADS}
        for f in as_completed(futures):
            item = futures[f]
            try:
                res = f.result()
            except Exception as e:
                print(f'[ERROR] {item[1]}: {e}', flush=True)
    print('All downloads finished!', flush=True)


if __name__ == '__main__':
    main()

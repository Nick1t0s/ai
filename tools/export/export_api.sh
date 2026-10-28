#!/bin/bash
# API-копии workflow через настоящий фронтенд ComfyUI (app.graphToPrompt): временный сервер на 8199 + headless Chromium.
# Генерацию не запускает и модели не грузит.
#
#   ./export_api.sh            — все workflow из build_list.py
#   ./export_api.sh "Upscale"  — только те, где «категория/имя» содержит строку
#
# Дальше: проверка всех API-копий по /object_info (validate_api.py) и пересборка ~/ai/workflows/README.md.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
HERE=$PWD
COMFY=$HOME/ai/comfyui
NODE=$HOME/.nvm/versions/node/v24.20.0/bin/node
RUN=$HERE/.run                                   # user/input/output временного сервера, логи
PROFILE=$HOME/snap/chromium/common/comfy-export  # snap-Chromium может писать только в ~/snap
FILTER=${1:-}

for port in 8199 9333; do
    if ss -ltnH "sport = :$port" | grep -q .; then
        echo "порт $port занят — останови то, что его слушает" >&2
        exit 1
    fi
done

# список заново, чтобы подхватить новые свои workflow из build_list.py
"$COMFY/venv/bin/python" -I build_list.py list.json
python3 -I - "$FILTER" <<'EOF'
import json, sys
f = sys.argv[1]
items = [i for i in json.load(open('list.json')) if f in f"{i['cat']}/{i['name']}"]
json.dump(items, open('.run-list.json', 'w'), ensure_ascii=False, indent=1)
print('на экспорт:', len(items))
if not items:
    sys.exit(1)
EOF

mkdir -p "$RUN"/{user,input,output,temp}
SERVER= BROWSER=
cleanup() {
    # setsid сделал оба процесса лидерами своих групп: убиваем группы целиком (Chromium плодит дочерние процессы)
    [ -n "$SERVER" ] && kill -- -"$SERVER" 2>/dev/null || true
    [ -n "$BROWSER" ] && kill -- -"$BROWSER" 2>/dev/null || true
    [ -n "$SERVER" ] && timeout 30 tail --pid="$SERVER" -f /dev/null 2>/dev/null || true
    [ -n "$BROWSER" ] && timeout 30 tail --pid="$BROWSER" -f /dev/null 2>/dev/null || true
    rm -rf "$PROFILE" "$HERE/.run-list.json"
    if ss -ltnH '( sport = :8199 or sport = :9333 )' | grep -q .; then
        echo "ВНИМАНИЕ: порт 8199 или 9333 всё ещё занят: $(ss -ltnpH '( sport = :8199 or sport = :9333 )')" >&2
    fi
}
trap cleanup EXIT

(cd "$COMFY" && exec setsid env -u ALL_PROXY -u all_proxy NO_PROXY='*' venv/bin/python main.py \
    --port 8199 --listen 127.0.0.1 --user-directory "$RUN/user" --input-directory "$RUN/input" \
    --output-directory "$RUN/output" --temp-directory "$RUN/temp") > "$RUN/server.log" 2>&1 &
SERVER=$!
setsid chromium --headless=new --remote-debugging-port=9333 --user-data-dir="$PROFILE" --no-first-run about:blank \
    > "$RUN/chromium.log" 2>&1 &
BROWSER=$!

curl --noproxy '*' -sf --retry 90 --retry-delay 2 --retry-connrefused -o /dev/null http://127.0.0.1:8199/system_stats
curl --noproxy '*' -sf --retry 30 --retry-delay 1 --retry-connrefused -o /dev/null http://127.0.0.1:9333/json/version

env -u ALL_PROXY -u all_proxy NO_PROXY='*' "$NODE" export.mjs .run-list.json "$HOME/ai/workflows" "$RUN/report.json"
curl --noproxy '*' -sf http://127.0.0.1:8199/object_info -o "$RUN/object_info.json"

python3 -I validate_api.py "$RUN/object_info.json" "$HOME/ai/workflows" placeholders.json
python3 -I make_readme.py

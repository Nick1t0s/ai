#!/bin/bash
# Просмотр результатов теста (скилл /comfy-test). Временные файлы — в $TMPDIR (ставь scratchpad).
#   look.sh grid   out.png f1 f2 …             — сетка с подписями (TILE=4x, SIZE=512x512)
#   look.sh crop   out.png file WxH+X+Y [zoom%] — кроп 1:1, с zoom — увеличение без сглаживания
#   look.sh frames out.png video [n]           — лист из n кадров (по умолчанию 9) с таймкодами + ffprobe и громкость
#   look.sh audio  out.png file                — спектрограмма + громкость (ebur128), тишина, длительность
set -euo pipefail
export LC_ALL=C
cmd=${1:?grid|crop|frames|audio}; shift

loud() {
    ffmpeg -nostats -hide_banner -i "$1" -af ebur128=peak=true -f null - 2>&1 |
        awk '/Summary:/{s=1} s && /I:|LRA:|Peak:/{gsub(/^ +/,""); printf "%s  ", $0} END{print ""}'
}

case $cmd in
grid)
    out=$1; shift
    magick montage -label '%t' "$@" -tile "${TILE:-4x}" -geometry "${SIZE:-512x512}+4+4" -pointsize 18 -background white "$out"
    ;;
crop)
    out=$1 file=$2 geo=$3 zoom=${4:-}
    if [ -n "$zoom" ]; then
        magick "$file" -crop "$geo" +repage -filter point -resize "$zoom%" "$out"
    else
        magick "$file" -crop "$geo" +repage "$out"
    fi
    ;;
frames)
    out=$1 video=$2 n=${3:-9}
    d=$(mktemp -d "${TMPDIR:-/tmp}/look.XXXXXX")
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$video")
    ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,nb_frames,sample_rate,channels -of compact=p=0 "$video"
    echo "duration=$dur"
    for i in $(seq 0 $((n - 1))); do
        t=$(awk -v d="$dur" -v i="$i" -v n="$n" 'BEGIN{printf "%.2f", (n == 1 ? 0 : i * (d - 0.1) / (n - 1))}')
        f=$d/$(printf %02d "$i").png
        ffmpeg -v error -ss "$t" -i "$video" -frames:v 1 -y "$f"
        magick "$f" -set comment "t=${t}s" "$f"
    done
    magick montage -label '%c' "$d"/*.png -tile 3x -geometry 640x+4+4 -pointsize 22 -background white "$out"
    rm -rf "$d"
    if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$video" | grep -q .; then
        echo "audio: $(loud "$video")"
    else
        echo "audio: нет дорожки"
    fi
    ;;
audio)
    out=$1 file=$2
    ffmpeg -v error -i "$file" -lavfi showspectrumpic=s=1400x500:legend=1:scale=log -y "$out"
    echo "duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$file")"
    echo "loudness: $(loud "$file")"
    ffmpeg -nostats -hide_banner -i "$file" -af silencedetect=n=-45dB:d=0.5 -f null - 2>&1 | grep -o 'silence_\(start\|end\): [0-9.]*' | paste -sd' ' || true
    ;;
*)
    echo "неизвестная команда: $cmd" >&2; exit 2
    ;;
esac

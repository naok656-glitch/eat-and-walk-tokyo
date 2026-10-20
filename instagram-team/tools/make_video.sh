#!/bin/sh
# スライド画像から縦型リール動画(1080x1920, 30fps)を作る。秒数は spec.json の durations。音声は無音(BGMは投稿時にInstagram内の音源を付ける)。
# 使い方: sh make_video.sh <reelDir>
set -e
R=$1
DUR=$(node -e "console.log(require('$R/spec.json').durations.join(' '))")
LIST=$(mktemp)
i=1
for d in $DUR; do
  printf "file '%s/slides/slide%s.png'\nduration %s\n" "$R" "$i" "$d" >> "$LIST"
  i=$((i+1))
done
printf "file '%s/slides/slide%s.png'\n" "$R" "$((i-1))" >> "$LIST"
ffmpeg -loglevel error -y -f concat -safe 0 -i "$LIST" \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -vf "fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 18 -movflags +faststart \
  -c:a aac -b:a 128k -shortest "$R/reel.mp4"
rm -f "$LIST"

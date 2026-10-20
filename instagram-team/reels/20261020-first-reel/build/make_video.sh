#!/bin/sh
# スライド画像から縦型リール動画(1080x1920, 30fps, 約30秒)を作る。音声は無音(BGMは投稿時にInstagram内の音源を付ける)。
# 使い方: sh build/make_video.sh(このリールのフォルダで実行)
set -e
DUR="3 3 4 4 4 4 5 3"
: > build/list.txt
i=1
for d in $DUR; do
  printf "file '../slides/slide%s.png'\nduration %s\n" "$i" "$d" >> build/list.txt
  i=$((i+1))
done
printf "file '../slides/slide8.png'\n" >> build/list.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i build/list.txt \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -vf "fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 18 -movflags +faststart \
  -c:a aac -b:a 128k -shortest reel.mp4

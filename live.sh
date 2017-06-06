#!/bin/bash
while true
do
  ffmpeg -re -f concat -safe 0 -i playlist.txt -vcodec copy -acodec aac -b:a 192k -f flv "rtmp://txy.live-send.acg.tv/live-txy/?streamname="
  ffmpeg -re -f concat -safe 0 -i playlist1.txt -vcodec copy -acodec aac -b:a 192k -f flv "rtmp://txy.live-send.acg.tv/live-txy/?streamname="
  ffmpeg -re -f concat -safe 0 -i playlist2.txt -vcodec copy -acodec aac -b:a 192k -f flv "rtmp://txy.live-send.acg.tv/live-txy/?streamname="
  ffmpeg -re -f concat -safe 0 -i playlist3.txt -vcodec copy -acodec aac -b:a 192k -f flv "rtmp://txy.live-send.acg.tv/live-txy/?streamname="
done

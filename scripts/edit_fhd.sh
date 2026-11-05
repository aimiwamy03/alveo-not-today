#!/bin/bash
# usage: edit.sh src.mp4 out.mp4
SRC=$1; OUT=$2; T=/tmp/edit_seg; rm -rf $T; mkdir -p $T
W=$(ffprobe -v error -select_streams v -show_entries stream=width -of csv=p=0 $SRC); H=$(ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 $SRC)
MI="minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
ENC="-an -c:v libx264 -crf 12 -preset fast -pix_fmt yuv420p -r 24"
seg(){ # name start end filter
 ffmpeg -v error -y -i $SRC -vf "trim=$2:$3,setpts=PTS-STARTPTS${4:+,$4},settb=1/24,fps=24,format=yuv420p" $ENC $T/$1.mp4 || exit 1; }
seg s1 0 1.25 "setpts=PTS*1.6,$MI,trim=0:2.0,setpts=PTS-STARTPTS"
seg s2a 2.15 2.70 "setpts=PTS*1.82,$MI,trim=0:1.0,setpts=PTS-STARTPTS"
seg s2b 3.0 3.92
seg s3a 3.92 5.0
seg s3b 5.0 5.58
seg s4a 5.60 7.32 "zoompan=z='1+0.12*on/41':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=${W}x${H}:fps=24,setpts=N/24/TB"
seg s4b 7.34 8.16
seg s5a 8.17 9.0 "fade=in:st=0:d=0.12:color=white"
seg s5b 9.17 10.04 "setpts=PTS*1.42,$MI,trim=0:1.24,setpts=PTS-STARTPTS"
for s in s1 s2a s2b s3a s3b s4a s4b s5a s5b; do printf "%s %s\n" $s $(ffprobe -v error -show_entries format=duration -of csv=p=0 $T/$s.mp4); done
ffmpeg -v error -y -i $T/s1.mp4 -i $T/s2a.mp4 -i $T/s2b.mp4 -i $T/s3a.mp4 -i $T/s3b.mp4 -i $T/s4a.mp4 -i $T/s4b.mp4 -i $T/s5a.mp4 -i $T/s5b.mp4 -filter_complex "
[0][1][2][3][4]concat=n=5:v=1:a=0,settb=1/24,fps=24[pre];
[5]settb=1/24,fps=24[p4];
[pre][p4]xfade=transition=slideup:duration=0.2:offset=5.38[mid];
[mid][6][7][8]concat=n=4:v=1:a=0,format=yuv420p[v]" -map "[v]" $ENC /tmp/edit_v.mp4 || exit 1
VD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/edit_v.mp4); echo "video dur $VD"
ffmpeg -v error -y -i $SRC -filter_complex "
[0:a]asplit=3[a1][a2][a3];
[a1]atrim=0:7.25,asetpts=PTS-STARTPTS,afade=t=out:st=7.1:d=0.15[x1];
[a2]atrim=6.0:6.67,asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st=0.6:d=0.07[x2];
[a3]atrim=7.3:9.4,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st=1.9:d=0.2[x3];
[x1][x2][x3]concat=n=3:v=0:a=1,atrim=0:10[a]" -map "[a]" -c:a aac -b:a 192k /tmp/edit_a.m4a || exit 1
echo "audio dur $(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/edit_a.m4a)"
ffmpeg -v error -y -i /tmp/edit_v.mp4 -i /tmp/edit_a.m4a -map 0:v -map 1:a -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -profile:v high -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $OUT && ffprobe -v error -show_entries stream=codec_name,width,height,pix_fmt -show_entries format=duration -of compact $OUT

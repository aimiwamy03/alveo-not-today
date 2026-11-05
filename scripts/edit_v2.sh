#!/bin/bash
# Final edit: FHD render (full2_fhd.mp4) + one shot (chest-pocket macro) from the HD draft (draft2.mp4), upscaled.
F=/workspace/preview/full2_fhd.mp4; D=/workspace/preview/draft2.mp4; P=/workspace/preview/v2/pocket_edit.mp4; C=/workspace/preview/v2/click1.mp4; OUT=$1; T=/tmp/edit_v2; rm -rf $T; mkdir -p $T
W=1088; H=1920
MI="minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
ENC="-an -c:v libx264 -crf 12 -preset fast -pix_fmt yuv420p -r 24"
seg(){ # name src start end [filter]
 ffmpeg -v error -y -i $2 -vf "trim=$3:$4,setpts=PTS-STARTPTS${5:+,$5},scale=${W}:${H}:flags=lanczos,setsar=1,settb=1/24,fps=24,format=yuv420p" $ENC $T/$1.mp4 || exit 1; }
seg s1  $F 0 1.25 "setpts=PTS*1.72,$MI,trim=0:2.09,setpts=PTS-STARTPTS"
seg s2a $P 0 0.86 "setpts=PTS*1.69,$MI,trim=end_frame=33,setpts=PTS-STARTPTS"
seg s2b $F 3.55 3.92
seg s3a $F 3.92 5.0
seg s3b $F 5.0 5.58 "setpts=PTS*1.3,$MI,trim=0:0.75,setpts=PTS-STARTPTS"
seg s4a $F 5.60 7.32 "zoompan=z='1+0.12*on/41':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=${W}x${H}:fps=24,setpts=N/24/TB"
seg s4b $F 7.34 8.12
seg s5a $C 0 0.3 "setpts=PTS*2,$MI,fade=in:st=0:d=0.08:color=white"
seg s5d $C 0.3 0.7
seg s5c $C 1.17 1.67
seg s5b $C 1.67 2.17
tot=0; for s in s1 s2a s2b s3a s3b s4a s4b s5a s5d s5c s5b; do d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $T/$s.mp4); echo "$s $d"; done
PRE=$(python3 -c "
import subprocess
d=sum(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','$T/'+s+'.mp4'])) for s in ['s1','s2a','s2b','s3a','s3b']); print(round(d-0.2,4))")
echo "xfade offset $PRE"
ffmpeg -v error -y -i $T/s1.mp4 -i $T/s2a.mp4 -i $T/s2b.mp4 -i $T/s3a.mp4 -i $T/s3b.mp4 -i $T/s4a.mp4 -i $T/s4b.mp4 -i $T/s5a.mp4 -i $T/s5d.mp4 -i $T/s5c.mp4 -i $T/s5b.mp4 -filter_complex "
[0][1][2][3][4]concat=n=5:v=1:a=0,settb=1/24,fps=24[pre];
[5]settb=1/24,fps=24[p4];
[pre][p4]xfade=transition=slideup:duration=0.2:offset=$PRE[mid];
[mid][6][7][8][9][10]concat=n=6:v=1:a=0,format=yuv420p[v]" -map "[v]" $ENC /tmp/v2_v.mp4 || exit 1
VD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/v2_v.mp4); echo "video dur $VD"
ffmpeg -v error -y -i /tmp/v2_v.mp4 -i $F -map 0:v -map 1:a -t 10 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -profile:v high -c:a aac -b:a 192k -ar 48000 -af "afade=t=out:st=9.8:d=0.2" -movflags +faststart $OUT && ffprobe -v error -show_entries stream=codec_name,width,height,pix_fmt,r_frame_rate -show_entries format=duration,size -of compact $OUT

import sys, json, time, base64, os, urllib.request
# Requires a small BFL helper (post/get) that reads BFL_API_KEY from the environment.
# from bfl import post, get
K='/workspace/preview/kfjpg/'
def b(f): return base64.b64encode(open(K+f,'rb').read()).decode()
PROMPT = """Vertical 9:16 premium outdoor-apparel social film, photoreal, shot on 35mm, cool bright minimal alpine palette (white snow, cool greys, pale blue) with one saturated color: the young woman's alpine orange #CE5426 hardshell jacket. Same young woman (early 20s, dark hair in a low ponytail), same orange jacket, black gloves, black trousers, grey-white trail boots in every shot. Exactly five shots of two seconds each on a strict 2-second grid (cuts at 2.0s, 4.0s, 6.0s and 8.0s); do not add any extra shots or cutaways. Edited rhythmically with designed transitions. No on-screen text, no voiceover, no dialogue.

SHOT 1 (0.0-2.0s): Cold blue-grey dawn in a quiet chalet hallway. Close-up of her black-gloved hand resting on the front door handle, the orange cuff the only color. She pauses and does NOT turn the handle; tiny hesitant finger movement. TRANSITION: match cut on the hand: the hand lifts off the handle and the cut continues the same hand motion into shot 2.

SHOT 2 (2.0-4.0s): Macro on her chest in the dim hallway: the same gloved hand moves in and pats the left chest pocket where the inhaler sits, the center zip half open; she takes a small step back, the fabric creasing. TRANSITION at 3.8s: a snowball flies straight into the lens and smashes across the camera, a burst of white powder fills the whole frame and wipes into shot 3.

SHOT 3 (4.0-6.0s): Bright snowy alpine village square, dark wooden chalets, white peaks. Friends in the background have a laughing snowball fight, powder in the air. She stands at the edge of the frame, hand on her chest, and steps back away from them. At 5.2s the camera is low on her boots stepping back in the snow, then in ONE continuous move tilts up from the boots to the bright mountain beyond, and the mountain slope carries straight into shot 4 at 6.0s.

SHOT 4 (6.0-8.0s): Wide: she stands small at the bottom of a steep snowy switchback trail, stops and looks up the slope. At 7.0s a quick push-in to an extreme close-up of her eyes, steady and calm; she lets out one slow visible breath of cold vapor. A single beat of near-silence.

SHOT 5 (8.0-10.0s), THE CLICK: hard cut exactly on the beat drop at 8.0s. The same wooden front door flies open, blinding bright sunlit snow floods in, and she bursts out running into the bright snow; camera tracking alongside her as she zips her high collar up to her chin mid-stride, determined and free, snow kicking up from her boots. High energy.

AUDIO: muffled cold room tone and a low, slow heartbeat-like kick drum under shots 1-2; a soft whoomp and crunch as the snowball hits the lens; distant laughter and wind in the village; wind over snow and one slow exhale, then near-silence from 7.0s to 8.0s; exactly at 8.0s (not earlier) a punchy modern electronic beat drops and drives to the end with footsteps crunching in snow. No speech."""
kf=[[0,b('k00_door_hand.jpg')],[2.4,b('k02_chest_pocket.jpg')],[4.5,b('k04_village.jpg')],[5.4,b('k05_boots.jpg')],[6.5,b('k06_path.jpg')],[7.6,b('k07_eyes.jpg')],[8.4,b('k08_door_burst.jpg')],[10,b('k10_run_zip.jpg')]]
draft = sys.argv[1]=='draft'
d=dict(mode='i2v',prompt=PROMPT,keyframes=kf,duration=10,aspect_ratio='9:16',generate_audio=True)
if draft: d['draft']=True
else: d['resolution']='fhd'
j=post('https://api.bfl.ai/v1/flux-3-video',d)
print(j, flush=True)
pu=j['polling_url']; t0=time.time()
while True:
    time.sleep(5); s=get(pu)
    if s['status']=='Ready':
        r=s['result']; out=sys.argv[2]
        urllib.request.urlretrieve(r['sample'],out)
        print('READY',round(time.time()-t0),'s', out, flush=True)
        if r.get('draft_cache'):
            urllib.request.urlretrieve(r['draft_cache'],out+'.draft_cache.bin'); print('draft cache saved')
        print({k:(v if not isinstance(v,str) or len(v)<120 else v[:60]+'...') for k,v in r.items()})
        break
    if s['status'] in ('Error','Failed','Request Moderated','Content Moderated'):
        print('FAIL', str(s)[:500]); break
    print(s['status'], round(time.time()-t0), flush=True)

import os,json,time,urllib.request,concurrent.futures as cf
KEY=os.environ['BFL_API_KEY']
STYLE=("Rough storyboard sketch, loose black ink and pencil lines on plain white paper, quick hand-drawn film storyboard frame, "
 "monochrome grayscale linework with a single bright color accent: only the jacket is colored {c}, everything else black and white. "
 "Minimal alpine setting. No text, no letters, no logos, no captions, no frame borders. Scene: ")
OR="vivid orange"; CO="vivid cobalt blue"
P_NT="a young woman with shoulder-length dark hair wearing a bright orange hooded alpine shell jacket"
P_C="a young woman with dark hair in a ponytail wearing a cobalt blue hooded alpine shell jacket"
shots={
'A01':(OR,f"close-up of a gloved hand resting on a front door handle, orange jacket cuff and zip pull visible, frosted door glass, cold dawn, {P_NT} hesitating"),
'A02':(OR,f"macro close-up of fingers patting the chest pocket of an orange jacket, outline of a small inhaler under the fabric, zipper pull, {P_NT}"),
'A03':(OR,f"medium shot of friends having a snowball fight in a snowy village square, {P_NT} standing at the edge of the frame, hand on her chest, stepping back"),
'A04':(OR,f"wide shot, {P_NT} tiny at the bottom of a long steep zigzag mountain path in snow, looking up the slope, hood down"),
'A05':(OR,f"extreme close-up of the eyes of {P_NT}, a soft cloud of breath vapor in cold air, orange collar edge at bottom of frame"),
'A06':(OR,f"dynamic medium tracking shot, {P_NT} bursting out of an open front door mid-stride into snow, arms swinging, zipping her orange collar up, energetic motion lines"),
'A07':(OR,f"medium shot, {P_NT} in the center of a snowball fight mid-throw, laughing, snow flying, friends around her, motion lines"),
'A08':(OR,f"low angle shot from a steep snowy zigzag mountain path, {P_NT} climbing toward the camera with her orange hood up, steady stride"),
'A09':(OR,f"close-up profile of {P_NT} smiling at a mountain summit, hand resting calmly on her orange chest, breath vapor, wide sky"),
'A10':(OR,f"very wide minimal snowy ridge with lots of empty sky, one small figure, {P_NT}, walking along the ridge"),
'B01':(OR,f"very wide shot of a huge white alpine ridge with one tiny figure, {P_NT}, climbing, lots of sky"),
'B02':(OR,f"low close-up of hiking boots stepping up through snow, orange jacket hem at the top of frame, {P_NT}"),
'B03':(OR,f"close-up profile of {P_NT} under her orange hood, collar zipped to the chin, wind lines, focused eyes"),
'B04':(OR,f"medium shot of the torso of {P_NT}, gloved hand pulling an underarm vent zipper on the orange jacket, snowy ridge behind"),
'B05':(OR,f"medium wide shot, {P_NT} standing on a mountain summit, arms opening wide, laughing in surprise, sky behind"),
'B06':(OR,f"wide aerial view of a snowy ridge with one small figure, {P_NT}, clean empty space"),
'C01':(CO,"wide shot of soft fog layers rolling over a mountain ridge line, a tiny distant figure in a cobalt blue jacket"),
'C02':(CO,f"macro of wind lifting spindrift snow off a crest beside the rippling fabric folds of a cobalt blue jacket sleeve, {P_C}"),
'C03':(CO,f"side tracking medium shot, {P_C} striding across a snowy slope, arms swinging, wind lines"),
'C04':(CO,f"close-up of the calm face of {P_C}, framed by her cobalt blue hood and high collar, eyes looking ahead"),
'C05':(CO,f"macro close-up of a soft calm breath cloud in front of the lips of {P_C} while moving fast, motion blur behind, cobalt collar edge"),
'C06':(CO,f"wide shot, {P_C} walking away into fog on a snowy ridge, figure fading, empty space"),
}
def post(url,data):
    r=urllib.request.Request(url,data=json.dumps(data).encode(),headers={'x-key':KEY,'Content-Type':'application/json','accept':'application/json'})
    return json.load(urllib.request.urlopen(r,timeout=60))
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'x-key':KEY,'accept':'application/json'}),timeout=60))
def run(k):
    c,scene=shots[k]
    if os.path.exists(f'{k}.jpg'): return k,'exists'
    for attempt in range(3):
        try:
            j=post('https://api.bfl.ai/v1/flux-pro-1.1',{'prompt':STYLE.format(c=c)+scene,'width':1024,'height':576,'seed':4242,'output_format':'jpeg','safety_tolerance':2})
            pu=j['polling_url']
            for _ in range(120):
                time.sleep(2); s=get(pu)
                if s['status']=='Ready':
                    urllib.request.urlretrieve(s['result']['sample'],f'{k}.jpg'); return k,'ok'
                if s['status'] not in ('Pending','Processing','Queued','Task not found'): raise Exception(str(s)[:200])
        except Exception as e: err=str(e)[:200]
    return k,'FAIL '+err
with cf.ThreadPoolExecutor(6) as ex:
    for k,r in ex.map(run,sorted(shots)): print(k,r,flush=True)

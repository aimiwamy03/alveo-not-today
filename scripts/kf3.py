exec(open('kf.py').read().split('jobs=[')[0])
FB=" Full-bleed vertical image filling the entire frame edge to edge, no black bars, no borders."
B='/workspace/vizard_assets/raw/prop_boots.png'
jobs=[dict(out='k05_boots.png',refs=[C,B,VIL],w=W,h=Hh,seed=3005,prompt=f"Low close-up of the grey and white trail boots from image 2 and the black technical trousers of the woman from image 1, standing still in fresh trampled snow in the bright alpine village square from image 3, the boots take a small step backward. The bottom hem of her alpine orange #CE5426 jacket is just visible at the very top of the frame. Bright overcast snow light, soft snow powder in the air. {LOOK}{FB}")]
run_all(jobs)

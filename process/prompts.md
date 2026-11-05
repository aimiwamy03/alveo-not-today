# Key prompts (exact quotes)

Source: figma bro session, Friday Oct 9, 2026 (PDT). No API keys or secrets.

## 1. Moodboard brief (Amy)

> add this somewhere also so im trying to creat a moodboard for an outdoors wear brand shoot very cool stylish trendy vibe think moncler and on cloud and solamen, bright colors + minialist alpine feel are you able to gather ref photos and assemble

(Pin included: https://www.pinterest.com/pin/887912882823084950/)

## 2. Film concept brief (Amy)

> lets do a social short 30s film. help brainstorm what this could be , the essence, we wnat this outdoor jacket to be for ppl with astham, the core is that it should improve their confidence in their body's capcity to movement, trust in it more and feel better able to move!!! it shold prob have a click when the emotional part resonates iwth audience

## 3. The insight (figma bro)

> for people with asthma, the fear of being out of breath is often what holds them back, more than the breath itself.

## 4. Direction pick (Amy)

> i like this more 2. "Not Today." Rhythmic and a bit defiant. Quick cuts of everything asthma has made someone skip: the cold run, the snowball fight, the steep path. Each one has a little "not today" moment, like a glance at an inhaler or stepping back. Then the same shots replay, and this time they go. The click is the hard cut from hesitating to running, timed to the beat. End card: Today.

## 5. Preview request (Amy)

> now generate 10 seconds of the final video in susessive 2 econd shots to preview the final work. this way i can check if you are going in the right direction. use black forect lab api for the vieo. the person is a girl. make sure to focus on the transitions

## 6. FLUX video preview prompt (from `scripts/vid2.py`, used for the 10s cut)

```
Vertical 9:16 premium outdoor-apparel social film, photoreal, shot on 35mm, cool bright minimal alpine palette (white snow, cool greys, pale blue) with one saturated color: the young woman's alpine orange #CE5426 hardshell jacket. Same young woman (early 20s, dark hair in a low ponytail), same orange jacket, black gloves, black trousers, grey-white trail boots in every shot. Exactly five shots of two seconds each on a strict 2-second grid (cuts at 2.0s, 4.0s, 6.0s and 8.0s); do not add any extra shots or cutaways. Edited rhythmically with designed transitions. No on-screen text, no voiceover, no dialogue.

SHOT 1 (0.0-2.0s): Cold blue-grey dawn in a quiet chalet hallway. Close-up of her black-gloved hand resting on the front door handle, the orange cuff the only color. She pauses and does NOT turn the handle; tiny hesitant finger movement. TRANSITION: match cut on the hand: the hand lifts off the handle and the cut continues the same hand motion into shot 2.

SHOT 2 (2.0-4.0s): Macro on her chest in the dim hallway: the same gloved hand moves in and pats the left chest pocket where the inhaler sits, the center zip half open; she takes a small step back, the fabric creasing. TRANSITION at 3.8s: a snowball flies straight into the lens and smashes across the camera, a burst of white powder fills the whole frame and wipes into shot 3.

SHOT 3 (4.0-6.0s): Bright snowy alpine village square, dark wooden chalets, white peaks. Friends in the background have a laughing snowball fight, powder in the air. She stands at the edge of the frame, hand on her chest, and steps back away from them. At 5.2s the camera is low on her boots stepping back in the snow, then in ONE continuous move tilts up from the boots to the bright mountain beyond, and the mountain slope carries straight into shot 4 at 6.0s.

SHOT 4 (6.0-8.0s): Wide: she stands small at the bottom of a steep snowy switchback trail, stops and looks up the slope. At 7.0s a quick push-in to an extreme close-up of her eyes, steady and calm; she lets out one slow visible breath of cold vapor. A single beat of near-silence.

SHOT 5 (8.0-10.0s), THE CLICK: hard cut exactly on the beat drop at 8.0s. The same wooden front door flies open, blinding bright sunlit snow floods in, and she bursts out running into the bright snow; camera tracking alongside her as she zips her high collar up to her chin mid-stride, determined and free, snow kicking up from her boots. High energy.

AUDIO: muffled cold room tone and a low, slow heartbeat-like kick drum under shots 1-2; a soft whoomp and crunch as the snowball hits the lens; distant laughter and wind in the village; wind over snow and one slow exhale, then near-silence from 7.0s to 8.0s; exactly at 8.0s (not earlier) a punchy modern electronic beat drops and drives to the end with footsteps crunching in snow. No speech.
```

## 7. Vizard prompt (workflow comparison)

Amy asked for a prompt that keeps the Vizard flow and the direct BFL flow comparable:

> perfect now write the perfect prompt so i can plug it in. esentially i am trying to test what workflow is better. you arehelping me with both the vizard flow and the direct BFL flow.

The prompt written for Vizard (same shot plan as the BFL preview). One mid-line in shot 2/3 was truncated in the saved transcript; the reconstructed line for shot 3 matches the storyboard card and the BFL preview shot list used for the fair test:

```
Make a 30-second vertical (9:16) social ad for "alveo", an outdoor jacket brand for people with asthma. The film is called "Not Today". Core idea: asthma taught her to say "not today"; this jacket gives her the confidence to trust her body and move. Photoreal, premium, minimal alpine look in the style of Moncler, On and Salomon campaigns. Bright Alpine orange jacket (#CE5426) popping against snow, grey and blue sky. No voiceover. Music-driven edit.

CONSISTENCY (strict): use the uploaded assets as the only reference for the protagonist and product. She is the same young woman in every shot (face_front, face_34, face_smile, character_front, character_34_front, character_side, character_34_back, character_back). The jacket must match jacket_front, jacket_back, jacket_side_left, jacket_side_right, jacket_front_open and jacket_hood_up exactly: same orange, high zip collar, single LEFT chest pocket, no logos. Use detail_* images for close-ups, prop_inhaler / prop_gloves / prop_boots for props, and location_hallway, location_village_square, location_switchback_path, location_summit_ridge for settings.

STRUCTURE: Act 1 "Not Today" (0:00-0:11): three moments where she holds back. Act 2 "Today" (0:11-0:30): the same three moments replay and this time she goes. The emotional "click" is the hard cut on the beat drop at 0:11.

SHOTS:
1. 0:00-0:03 | Close | location_hallway, cold dawn. Her gloved hand rests on the wooden front door handle; she pauses and doesn't turn it. Orange cuff is the only color in a grey hallway. (refs: hands_gloves, detail_cuff) -> MATCH CUT on the hand.
2. 0:03-0:05 | Macro | The same hand pats her left chest pocket; the inhaler outline shows.
3. 0:05-0:08 | Medium | location_village_square. Snowball fight; she stands at the edge, hand on chest, and steps back. Super: "not today." -> TILT UP from her boots to the mountains.
4. 0:08-0:10 | Wide | location_switchback_path. She stops at the bottom and looks up the steep slope. Tiny orange figure on a huge white mountain.
5. 0:10-0:11 | Extreme close | Her eyes and one slow, calm breath of vapor. (refs: face_front, pose_breathe_out) -> one beat of silence, then a HARD CUT.
6. 0:11-0:14 | Medium tracking | THE CLICK. The beat drops: the same door flies open and she runs out into bright snow, zipping her collar up mid-stride. (refs: pose_running, detail_collar_zipped) Super: "Today."
7. 0:14-0:17 | Medium | Snowball fight replay: she runs in, throws, gets hit, and laughs. (ref: pose_laughing)
8. 0:17-0:22 | Wide to low angle | Path replay: hood up, she climbs past the point where she stopped. (refs: jacket_hood_up, detail_hood, prop_boots)
9. 0:22-0:26 | Close | location_summit_ridge. Hand on chest again, now calm; she smiles, breath vapor visible. (ref: face_smile)
10. 0:26-0:30 | Wide | She walks the ridge, small and bright against the snow. End card: "Today." then the alveo logo.

EDIT AND SOUND: Act 1 is quiet and tense, with muffled room tone, a low heartbeat-like kick, wind and a hi-hat building. Act 2 is energetic and on the beat. Cut every shot on the beat. Transitions must be motivated (match cuts, the snowball wipe, the tilt), not generic crossfades. Supers in a small, clean, lowercase sans-serif, white. No other text, no brand logos besides alveo, no subtitles.
```

Fair-test note that went with it:

> For a fair test, keep a few things identical across both flows. Use the same assets, the same 9:16 format, and a 10-second cut of shots 1 to 6 (0:00 to 0:14) if you're comparing against my BFL preview. Then score each one on four things: whether the girl and jacket stay consistent, whether the transitions land, whether the click hits, and how much time and cost it took.

## 8. Story upgrade request (Amy)

> ok now that we have this what shoudl we do to making it so much better in terms of the story line i think we need more shots, more shot ideas like  2x maybe and more brand coseup shots

## 9. Story upgrade response (turning point)

> Add a turning point. Give her one small private moment before the click: her hand finds the inhaler in the chest pocket, she breathes, and she zips the collar up like putting on armor. Then the beat drops. That turns the jacket into the reason she goes, not just what she's wearing.

> The visual thread through the whole film is her hand on her chest. It shows up three times: as fear, then as resolve on the zip, then as calm.


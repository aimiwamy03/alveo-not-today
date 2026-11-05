# Scripts

Generation and edit scripts from the Oct 9, 2026 Alveo session.

- `storyboard_gen.py`: FLUX stills for storyboard frames A01 to A10 (and B/C).
- `kf*.py`: keyframe stills for the 10-second FLUX video preview.
- `vid.py` / `vid2.py`: FLUX 3 video jobs with pinned keyframes (draft then full HD).
- `edit*.sh`: ffmpeg assembly of the hybrid preview cut.

All API access uses `BFL_API_KEY` from the environment. No secrets are stored in this repo.

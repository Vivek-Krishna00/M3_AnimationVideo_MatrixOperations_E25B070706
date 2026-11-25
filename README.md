# What does a matrix do? (Matrices and matrix operations)
Vivek Krishna, E25B070706. M3 Internal Assessment, Animation Video.

- `_Video.mp4`: final video
- `_Code/`: Manim source (`scenes.py`, `common.py`), narration, build script, maths checks
- `Storyboard.pdf`: six-scene storyboard
- `Recording_Script.txt`: narration text

## Rebuild
Needs Python 3.12, FFmpeg, whisper.cpp (`whisper-cli` with `ggml-small.en.bin` in `~/.cache/whisper`) and the STIX Two Text font (included with macOS). `pip install manim`, then run `python _Code/my_voice.py`. (`setup_voice.sh` and `make_voice.py` build an optional AI-voice version.)

## References and disclosure
- Visual style inspired by 3Blue1Brown, *Essence of Linear Algebra* (YouTube). No footage or code reused.
- Manim Community, Python, NumPy, FFmpeg.
- AI: script, storyboard, visuals, music and code generated with Claude (Anthropic), directed and reviewed by the student. Narration recorded by the student (noise-reduced and levelled with FFmpeg; aligned with whisper.cpp).
- Music: original instrumental synthesised with NumPy (`_Code/music.py`, code written with Claude).

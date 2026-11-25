"""Voice every line, then build the video around the exact line lengths.
python make_voice.py kokoro af_heart   final: ../_Video.mp4 (neural voice, runs locally)
python make_voice.py say Tara          preview: ../Preview_with_voice.mp4"""
import json, os, subprocess, sys
from narration import NARRATION
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
engine, voice = (sys.argv[1:] + ["say", "Tara"])[:2] if len(sys.argv) < 2 else sys.argv[1:3]
D = f"{HERE}/media/voice_{engine}"
os.makedirs(D, exist_ok=True)
def run(*c): subprocess.run(c, check=True)
def length(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))

jobs = [(f"{D}/raw{n}_{k}." + ("wav" if engine == "kokoro" else "aiff"), text)
        for n, beats in NARRATION.items() for k, text in enumerate(beats)]
if engine == "kokoro":            # kokoro lives in its own environment
    run(f"{ROOT}/.ttsvenv/bin/python", f"{HERE}/kokoro_say.py", f"{ROOT}/.ttsmodel", voice, json.dumps(jobs))
else:
    for f, text in jobs:
        run("say", "-v", voice, "-r", "118", "-o", f, text)

files = iter(f for f, _ in jobs)
for n, beats in NARRATION.items():
    ends, t, parts = [], 0, []
    for k in range(len(beats)):
        out = f"{D}/beat{n}_{k}.wav"
        run("ffmpeg", "-y", "-v", "error", "-i", next(files), "-af", "apad=pad_dur=0.6", "-ar", "48000", "-ac", "1", out)
        t += length(out); ends.append(t); parts.append(out)
    open(f"{D}/l.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    run("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{D}/l.txt", "-c", "copy", f"{D}/scene{n}.wav")
    json.dump(ends, open(f"{D}/scene{n}.json", "w"))
env = {**os.environ, "VOICE_DIR": D}
if engine == "kokoro":
    env["VOICE_CREDIT"] = f"Narration: AI voice (Kokoro, {voice}), script read as written."
subprocess.run([sys.executable, f"{HERE}/build.py"], check=True, env=env)

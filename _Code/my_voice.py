"""Use recordings/scene1..6.m4a: clean them, find where each line starts (whisper-cli),
and build the video around those times."""
import difflib, json, os, re, subprocess, sys, wave
import numpy as np
from narration import NARRATION
HERE = os.path.dirname(os.path.abspath(__file__))
D = f"{HERE}/media/voice_me"; os.makedirs(D, exist_ok=True)
MODEL = os.path.expanduser("~/.cache/whisper/ggml-small.en.bin")
run = lambda *c: subprocess.run(c, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
MUTE = {4: [(77.98, 78.54)]}      # seconds in the cleaned clip: a repeated "two"
NUM = dict(zip("0123456789", "zero one two three four five six seven eight nine".split()))
def words(s):
    s = re.sub(r"\d", lambda m: f" {NUM[m[0]]} ", s.lower())
    return re.findall(r"[a-z]+", s)

for n, beats in NARRATION.items():
    clean = f"{D}/clean{n}.wav"
    run("ffmpeg", "-y", "-i", f"{HERE}/recordings/scene{n}.m4a", "-af",
        "highpass=f=85,volume=12dB,alimiter=limit=0.95", "-ar", "48000", "-ac", "1", f"{D}/noisy{n}.wav")
    run(sys.executable, f"{HERE}/denoise.py", f"{D}/noisy{n}.wav", clean)
    for a, b in MUTE.get(n, []):
        run("ffmpeg", "-y", "-i", clean, "-af", f"volume=0:enable='between(t,{a},{b})'", f"{D}/m.wav"); os.replace(f"{D}/m.wav", clean)
    run("ffmpeg", "-y", "-i", clean, "-ar", "16000", f"{D}/w.wav")
    run("whisper-cli", "-t", "2", "-m", MODEL, "-f", f"{D}/w.wav", "-np", "-ml", "1", "-sow", "-oj", "-of", f"{D}/w{n}")
    heard = [(w, s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000)
             for s in json.load(open(f"{D}/w{n}.json"))["transcription"] for w in words(s["text"])]
    script, owner = [], []
    for k, b in enumerate(beats):
        for w in words(b): script.append(w); owner.append(k)
    sm = difflib.SequenceMatcher(None, script, [h[0] for h in heard], autojunk=False)
    pair = {a + i: b + i for a, b, l in sm.get_matching_blocks() for i in range(l)}
    starts = []
    for k in range(len(beats)):
        idx = [i for i, o in enumerate(owner) if o == k]
        first = next(i for i in idx if i in pair)
        starts.append(max(0, heard[pair[first]][1] - .25 * (first - idx[0])))
    with wave.open(clean) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float)
    sr = 48000
    win = sr // 10
    rms = np.sqrt(np.convolve(x * x, np.ones(win) / win, "same"))
    def quiet(t, before, after):                   # quietest moment near t
        a, b = int(max(0, t - before) * sr), int(min(len(x) / sr - .05, t + after) * sr)
        return (a + int(np.argmin(rms[a:b]))) / sr
    cuts = [quiet(t, .7, .25) for t in starts]
    end = min(len(x) / sr, heard[-1][2] + .5)
    run("ffmpeg", "-y", "-ss", str(cuts[0]), "-to", str(end), "-i", clean, "-af", "apad=pad_dur=0.5", f"{D}/scene{n}.wav")
    total = end - cuts[0] + .5
    ends = [c - cuts[0] for c in cuts[1:]] + [total]
    json.dump(ends, open(f"{D}/scene{n}.json", "w"))
    print(f"scene {n}: match {sm.ratio():.0%}, starts at {cuts[0]:.1f}s, line ends {[round(e, 1) for e in ends]}")
subprocess.run([sys.executable, f"{HERE}/build.py"], check=True,
               env={**os.environ, "VOICE_DIR": D, "VOICE_CREDIT": "Narration recorded by the student."})

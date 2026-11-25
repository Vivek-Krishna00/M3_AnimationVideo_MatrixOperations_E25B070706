"""Render all scenes, add recordings (or silence), and join into ../_Video.mp4.
Usage: python build.py            full 1080p60
       python build.py -ql        quick preview"""
import os, re, subprocess, sys
from common import HERE, TEMP_VOICE, clip_for, seconds
q = sys.argv[1] if len(sys.argv) > 1 else "-qh"
os.chdir(HERE)
def gain_to(path, target):
    """Constant gain (dB) that brings a file to the target loudness, so pauses are not boosted."""
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return target - float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])
def run(*c):
    if c[0] == "ffmpeg": c = ("ffmpeg", "-nostdin", "-threads", "2") + c[1:]
    subprocess.run(c, check=True)
run(sys.executable, "check_math.py")
names = [f"S{i}" for i in range(1, 7)]
run(sys.executable, "-m", "manim", q, "--disable_caching", "--progress_bar", "none", "-v", "WARNING", "scenes.py", *(os.environ["ONLY"].split() if "ONLY" in os.environ else names))
folder = {"-ql": "480p15", "-qm": "720p30", "-qh": "1080p60"}[q]
parts = []
for i, n in enumerate(names, 1):
    src, out, clip = f"media/videos/scenes/{folder}/{n}.mp4", f"media/part{i}.mp4", clip_for(i)
    audio = ["-i", clip] if clip else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    run("ffmpeg", "-y", "-v", "error", "-i", src, *audio, "-map", "0:v", "-map", "1:a", "-af",
        (f"volume={gain_to(clip, -16):.2f}dB,alimiter=limit=0.8:level=0,apad" if clip else "apad"),
        "-t", str(seconds(src)), "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "-ac", "2", out)
    parts.append(out)
open("media/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
final = "media/full.mp4" if TEMP_VOICE else "../_Video.mp4" if q == "-qh" else "media/preview.mp4"
run("ffmpeg", "-y", "-v", "error", "-f", "concat", "-i", "media/list.txt", "-c", "copy", "media/nomusic.mp4")
# background music: well under the voice, and ducked further while the voice speaks
run(sys.executable, "music.py", str(seconds("media/nomusic.mp4")), "media/music.wav")
music = gain_to("media/music.wav", -31.4)
run("ffmpeg", "-y", "-v", "error", "-i", "media/nomusic.mp4", "-i", "media/music.wav", "-filter_complex",
    f"[1:a]volume={music:.2f}dB,aresample=48000[m];[0:a]asplit[v][key];"
    "[m][key]sidechaincompress=threshold=0.02:ratio=3:attack=60:release=700[duck];"
    "[v][duck]amix=inputs=2:duration=first:normalize=0[a]",
    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final)
if TEMP_VOICE:
    os.replace(final, "../Preview_with_voice.mp4"); final = "../Preview_with_voice.mp4"
t = seconds(final)
print(f"{final}: {int(t//60)}:{t%60:04.1f}", "(OVER 7 MINUTES!)" if t > 420 else "")

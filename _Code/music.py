"""Original instrumental (piano, bass, soft drums, strings). Usage: music.py SECONDS OUT.wav"""
import sys, wave
import numpy as np
R, BPM = 48000, 76
BEAT = 60 / BPM; BAR = 4 * BEAT
rng = np.random.default_rng(7)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
#          bass, chord tones
CHORDS = [(36, (60, 64, 67, 71)), (43, (59, 62, 67, 69)), (45, (60, 64, 67, 69)), (41, (60, 65, 67, 69)),
          (38, (60, 62, 65, 69)), (43, (59, 62, 65, 67)), (40, (59, 62, 64, 67)), (41, (60, 64, 65, 69))]
# 8-bar melody: (beat, midi, length in beats)
TUNE = [(0, 76, 1.5), (1.5, 74, .5), (2, 72, 2), (4, 71, 1.5), (5.5, 72, .5), (6, 74, 2), (8, 72, 1), (9, 76, 1),
        (10, 79, 2), (12, 77, 1.5), (13.5, 76, .5), (14, 72, 2), (16, 74, 1.5), (17.5, 77, .5), (18, 81, 2),
        (20, 79, 1.5), (21.5, 77, .5), (22, 74, 2), (24, 76, 2), (26, 71, 2), (28, 72, 3)]

def piano(m, dur):
    t = np.arange(int((dur + 1.6) * R)) / R; f = hz(m); s = 0
    for k, a in enumerate((1, .5, .22, .12, .06), 1):
        s = s + a * np.sin(2 * np.pi * f * k * np.sqrt(1 + 4e-4 * k * k) * t) * np.exp(-(1.1 + .5 * k) * t)
    return s * np.clip(t / .006, 0, 1) * np.clip((dur + 1.6 - t) / .5, 0, 1)
def bass(m, dur):
    t = np.arange(int(dur * R)) / R; f = hz(m)
    return (np.sin(2*np.pi*f*t) + .35*np.sin(4*np.pi*f*t)) * np.exp(-.9*t) * np.clip(t/.02, 0, 1) * np.clip((dur-t)/.15, 0, 1)
def strings(m, dur):
    t = np.arange(int((dur + 1) * R)) / R; f = hz(m)
    s = sum(np.sin(2*np.pi*f*d*t) + .3*np.sin(4*np.pi*f*d*t) for d in (.997, 1, 1.003))
    return s * np.sin(np.clip(t/1.2, 0, 1)*np.pi/2)**2 * np.sin(np.clip((dur+1-t)/1.2, 0, 1)*np.pi/2)**2
def kick():
    t = np.arange(int(.28*R))/R
    return np.sin(2*np.pi*(48*t + 4*(1-np.exp(-30*t)))) * np.exp(-12*t) * np.clip(t/.004, 0, 1)
def brush():
    n = np.diff(rng.standard_normal(int(.14*R)+1)); t = np.arange(len(n))/R
    return n * np.exp(-32*t) * np.clip(t/.01, 0, 1)

def make(total):
    n = int(total * R); dry = np.zeros((n, 2))
    def add(s, at, vol, pan=.5):
        i = int(at * R)
        if i >= n: return
        s = s[:n - i] * vol
        dry[i:i+len(s), 0] += s * (1 - pan); dry[i:i+len(s), 1] += s * pan
    K, Bz = kick(), None
    for b in range(int(total / BAR) + 1):
        t0 = b * BAR; root, ch = CHORDS[b % 8]; section = (b // 8) % 4   # 0 piano, 1 +bass/drums, 2 +melody, 3 +strings
        for q, j in enumerate((0, 1, 2, 3, 2, 1, 2, 3)):
            add(piano(ch[j], .5), t0 + q*BEAT/2 + rng.uniform(0, .012), .20 + .06*(q % 4 == 0), .40 + .05*j)
        add(piano(root + 12, 2), t0, .22, .45)
        if section >= 1:
            add(bass(root, 2*BEAT), t0, .42); add(bass(root, 1.9*BEAT), t0 + 2*BEAT, .34)
            for q in (0, 2): add(K, t0 + q*BEAT, .38)
            for q in range(8): add(brush(), t0 + q*BEAT/2, .035 if q % 2 else .02, .62)
        if section == 3:
            for j, m in enumerate(ch[:3]): add(strings(m, BAR), t0, .055, .25 + .25*j)
    for p in range(int(total / (8*BAR)) + 1):
        if p % 4 >= 2:
            for beat, m, d in TUNE: add(piano(m, d*BEAT), p*8*BAR + beat*BEAT, .30, .55)
    m = int(1.8 * R); ir = rng.standard_normal((m, 2)) * np.exp(-np.arange(m)/R*3.2)[:, None]
    ir = np.cumsum(ir - np.roll(ir, 12, axis=0), axis=0); ir /= np.sqrt((ir**2).sum(0))   # softened reverb tail
    L = 2 ** int(np.ceil(np.log2(n + m)))
    wet = np.stack([np.fft.irfft(np.fft.rfft(dry[:, c], L) * np.fft.rfft(ir[:, c], L), L)[:n] for c in (0, 1)], 1)
    e = np.arange(n) / R
    out = (dry + .16 * wet) * (np.clip(e/2.5, 0, 1) * np.clip((total - e)/4, 0, 1))[:, None]
    return out / np.abs(out).max() * .8

if __name__ == "__main__":
    x = make(float(sys.argv[1]))
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(R)
        w.writeframes((x * 32767).astype("<i2").tobytes())

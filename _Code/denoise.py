"""Removes steady background noise (a fan). Usage: denoise.py IN.wav OUT.wav (48 kHz mono)
The noise spectrum is learned from the quietest frames; each frequency is then turned
down (Wiener filter) when it is not clearly above that noise."""
import sys, wave
import numpy as np
N, H = 2048, 512
def clean(x):
    win = np.hanning(N + 1)[:-1]
    x = np.pad(x, (N, N + H))
    frames = np.array([np.fft.rfft(win * x[i:i + N]) for i in range(0, len(x) - N, H)])
    power = np.abs(frames) ** 2
    level = power[:, 8:170].sum(1)                        # speech band energy
    active = level > 1e-9 * level.max()                   # ignore digital silence
    quiet = active & (level <= np.percentile(level[active], 12))
    noise = power[quiet].mean(0) * 1.2 + 1e-12            # noise profile, with a margin
    prev, gains = np.ones(power.shape[1]), np.empty_like(power)
    for i, p in enumerate(power):                         # decision-directed Wiener gain
        post = p / noise
        prio = .97 * prev + .03 * np.maximum(post - 1, 0)
        prio = np.maximum(prio, .25 * np.maximum(post - 1, 0))   # fast attack for consonants
        g = prio / (1 + prio)
        prev = g ** 2 * post
        gains[i] = np.maximum(g, .07)
    # expander: turn pauses down further, with smooth edges
    snr = 10 * np.log10(level / level[quiet].mean() + 1e-9)
    gate = np.clip((snr - 3) / 7, 0, 1)
    k = 14                                                # hold about 0.15 s either side
    gate = np.array([gate[max(0, i - k):i + k + 1].max() for i in range(len(gate))])
    gate = np.convolve(np.pad(gate, 6, mode="edge"), np.ones(13) / 13, "valid")
    gains *= (.10 + .90 * gate)[:, None]
    out, norm = np.zeros(len(x)), np.zeros(len(x))
    for i, f in enumerate(frames * gains):
        out[i * H:i * H + N] += np.fft.irfft(f) * win
        norm[i * H:i * H + N] += win ** 2
    return (out / np.maximum(norm, 1e-6))[N:-(N + H)]
if __name__ == "__main__":
    with wave.open(sys.argv[1]) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2") / 32768
    y = np.clip(clean(x), -1, 1)
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
        w.writeframes((y * 32767).astype("<i2").tobytes())

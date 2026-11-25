import json, re, sys
import soundfile as sf
from kokoro_onnx import Kokoro
folder, voice, jobs = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
k = Kokoro(f"{folder}/kokoro-v1.0.onnx", f"{folder}/voices-v1.0.bin")
def spoken(text):
    # say the matrix name A as the letter, not as the article "a"
    return re.sub(r"\bA\b(?! matrix)", "eigh", text)
for path, text in jobs:
    text = spoken(text)
    audio, rate = k.create(text, voice=voice, speed=0.92, lang="en-us")
    sf.write(path, audio, rate)

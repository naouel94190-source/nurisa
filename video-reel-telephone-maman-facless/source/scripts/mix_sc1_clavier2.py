import json, subprocess, wave, numpy as np, os
SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
TOT = json.load(open(os.path.join(HERE, 'sc1_timing.json')))['total'] + 0.5
def load_wav(p):
    with wave.open(p, 'rb') as w:
        return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
def notif():
    raw = subprocess.run(['ffmpeg','-v','error','-i',os.path.join(HERE,'sfx','notif_message.mp3'),'-ac','1','-ar',str(SR),'-f','f32le','-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    return x / max(1e-6, np.max(np.abs(x))) * 0.6

def key_clips():
    raw = subprocess.run(['ffmpeg','-v','error','-i',os.path.join(HERE,'sfx','clavier_iphone.mp3'),'-ac','1','-ar',str(SR),'-f','f32le','-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    fr = int(0.005*SR); n = len(x)//fr
    db = 20*np.log10(np.sqrt((x[:n*fr].reshape(n,fr)**2).mean(1))+1e-9)
    ons = [i*0.005 for i in range(1,n) if db[i] > db[i-1] + 8 and db[i] > db.max() - 30]
    groups = []
    for t in ons:
        if groups and t - groups[-1][-1] < 0.12: groups[-1].append(t)
        else: groups.append([t])
    clips = []
    for g in groups:
        t = g[-1]  # on garde le dernier claquement de chaque frappe
        seg = x[int(t*SR):int((t+0.10)*SR)].copy()
        if len(seg) < int(0.05*SR): continue
        f = int(0.003*SR); seg[:f] *= np.linspace(0,1,f); seg[-f:] *= np.linspace(1,0,f)
        clips.append(seg / max(1e-6, np.max(np.abs(seg))) * 0.5)
    return clips
KEYS = key_clips()
CL = {'chime': notif(), 'key1': load_wav(os.path.join(HERE,'key1.wav')), 'key2': load_wav(os.path.join(HERE,'key2.wav')), 'key3': load_wav(os.path.join(HERE,'key3.wav'))}
ev = json.load(open(os.path.join(HERE, 'sfx.json')))
kc = 0
n = int(TOT * SR)
out = np.zeros(n, np.float32)
for at, name, vol in ev:
    if name.startswith('key'):
        x = KEYS[(kc * 7) % len(KEYS)] * vol; kc += 1
    else:
        x = CL[name] * vol
    s0 = int(at * SR)
    if s0 >= n: continue
    e = min(n, s0 + len(x)); out[s0:e] += x[:e - s0]
pk = np.max(np.abs(out))
if pk > 0.89: out = out / pk * 0.89
pcm = (np.clip(out, -1, 1) * 32767).astype('<i2')
with wave.open(os.path.join(HERE, 'audio_sc1_clavier2.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('audio', round(TOT, 2), 's events', len(ev), 'peak', round(float(pk), 3))

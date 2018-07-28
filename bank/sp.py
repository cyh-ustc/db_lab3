import numpy as np
import soundfile
from numpy.lib.stride_tricks import as_strided
step = 10
window = 20
sound_file = soundfile.SoundFile('1.wav')
audio = sound_file.read(dtype='float32')
sample_rate = sound_file.samplerate
if audio.ndim >= 2:
    audio = np.mean(audio, 1)
	
if step > window:
    raise ValueError("step size must not be greater than window size")
hop_length = int(0.001 * step * sample_rate)
fft_length = int(0.001 * window * sample_rate)
samples = audio
assert not np.iscomplexobj(samples), "Must not pass in complex numbers"
window = np.hanning(fft_length)[:, None]
window_norm = np.sum(window ** 2)
scale = window_norm * sample_rate

trunc = (len(samples) - fft_length) % hop_length
x = samples[:len(samples) - trunc]

# "stride trick" reshape to include overlap
nshape = (fft_length, (len(x) - fft_length) // hop_length + 1)
nstrides = (x.strides[0], x.strides[0] * hop_length)

print(nshape)

print(nstrides)

print(x.shape)
x = as_strided(x, shape=nshape, strides=nstrides)

print(x.shape)

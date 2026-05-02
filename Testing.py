import numpy as np

samples = np.frombuffer(audio_data, dtype=np.int16)

num_samples = len(samples)

sample_rate = 16000

duration = num_samples / sample_rate

print(f"Duration: {duration:.2f} seconds")
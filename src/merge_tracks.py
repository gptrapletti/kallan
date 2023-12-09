import os
from pydub import AudioSegment
from tqdm import tqdm
import yaml

with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

combined = AudioSegment.empty() # empty audio

print('Merging audio tracks...')
for filename in tqdm(sorted(os.listdir(cfg['audiotrack_path']))):
    if filename.endswith('.mp3'):
        audio = AudioSegment.from_mp3(os.path.join(cfg['audiotrack_path'], filename))
        combined += audio

print('Saving file...')
combined.export(cfg['audiobook_path'], format="mp3")

print('Completed!')
import os
from pydub import AudioSegment
import yaml

with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

combined = AudioSegment.empty() # empty audio

for filename in sorted(os.listdir(cfg['audiotrack_path'])):
    if filename.endswith('.mp3'):
        audio = AudioSegment.from_mp3(os.path.join(cfg['audiotrack_path'], filename))
        combined += audio

combined.export(cfg['audiobook_path'], format="mp3")
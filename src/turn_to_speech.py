from openai import OpenAI
import json
from pydub import AudioSegment
import os
import yaml
import time
import dotenv
from src.utils import from_str_to_mp3

_ = dotenv.load_dotenv(dotenv.find_dotenv())

with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)
    
with open(cfg['translated_chunks_path'], 'r') as f:
    chapter_chunks = json.load(f)
    
client = OpenAI()

silent = AudioSegment.silent(duration=1000)

done_chapter_intros = []
for chapter, chunks in chapter_chunks.items():
    print(f'chapter {chapter}/{len(chapter_chunks.keys())}')
    chap_str = f'{chapter}'.zfill(2)
    if chapter not in done_chapter_intros:
        # First silent track
        silent.export(
            out_f=os.path.join(cfg['audiotrack_path'], f'chapter_{chap_str}_track_000.mp3'), 
            format='mp3'
        )
        # Chapter intro
        from_str_to_mp3(
            client=client, 
            text=f'Chapter {chapter}', 
            dst=os.path.join(cfg['audiotrack_path'], f'chapter_{chap_str}_track_001.mp3')
        )
        # Second silent intro
        silent.export(
            out_f=os.path.join(cfg['audiotrack_path'], f'chapter_{chap_str}_track_002.mp3'), 
            format='mp3'
        )
        done_chapter_intros.append(chapter)

    for i, chunk in enumerate(chunks):
        print(f'chunk {i + 1}/{len(chunks)}')
        chunk_str = f'{i + 3}'.zfill(3) # +3 to follow the intro files
        time.sleep(3)
        from_str_to_mp3(
            client=client, 
            text=chunk, 
            dst=os.path.join(cfg['audiotrack_path'], f'chapter_{chap_str}_track_{chunk_str}.mp3')
        )

print('Text-to-speech completed!')
import fitz
import yaml
import re
import json
from src.utils import count_tokens, merge_sentences

with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)
    
pdf = fitz.open(cfg['pdf_path'])
print(f'PDF loaded, {pdf.page_count} pages found.')

watermark = "\nTack för att du köpt den här boken! Order: 50231419 - 2023-11-27 Butik:\n759. \
All kopiering, utöver för ditt privata bruk, och otillbörlig\nvidarespridning är förbjuden."

pdf_text = ''
for i, page in enumerate(pdf):
    if i not in cfg['pages_to_exclude']:
        page_text = page.get_text()
        # Remove disclaimer watermark
        if watermark in page_text:
            page_text = page_text.replace(watermark, '')
        pdf_text += page_text
        
# Split in chapters
pattern = r'\d+\n'
chapters_ls = re.split(pattern, pdf_text)
chapters_ls = [chapter for chapter in chapters_ls if chapter != '']
chapters = {i + 1: chapter for i, chapter in enumerate(chapters_ls)}

# Split in sentences
sentences = {}
for chapter_id, chapter_text in chapters.items():
    sentences[chapter_id] = chapter_text.split('.')
    
# Merge sentences to create chunks for translation
chapter_chunks = {}
for chapter_id, sentence_ls in sentences.items():
    chapter_chunks[chapter_id] = merge_sentences(sentence_ls, n=cfg['translation_chunk_size'])
    
# Stats
n_chunks = 0
for chapter, chunks in chapter_chunks.items():
    n_chunks += len(chunks)
    
chunk_tokens = []
chunk_characters = []
for chapter, chunks in chapter_chunks.items():
    for i, chunk in enumerate(chunks):
        chunk_tokens.append(count_tokens(chunk))
        chunk_characters.append(len(chunk))
    
print(f'''PDF processed: 
    Chunks extracted: {n_chunks}
    Mean chunk size in tokens: {round(sum(chunk_tokens) / len(chunk_tokens))}
    Min chunk size in tokens: {round(min(chunk_tokens))}
    Max chunk size in tokens: {round(max(chunk_tokens))}
    Mean chunk size in characters: {round(sum(chunk_characters) / len(chunk_characters))}
    Min chunk size in characters: {round(min(chunk_characters))}
    Max chunk size in characters: {round(max(chunk_characters))}''')

with open(cfg['original_chunks_path'], 'w') as f:
    json.dump(chapter_chunks, f)
    
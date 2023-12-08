import yaml
from langchain.prompts import PromptTemplate
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import LLMChain
import json
from tqdm import tqdm
import dotenv
import time

_ = dotenv.load_dotenv(dotenv.find_dotenv())

with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)
    
with open(cfg['original_chunks_path'], 'r') as f:
    chapter_chunks = json.load(f)
    
prompt_template = '''Please translate the following excerpt from a novel into English. 
Aim to preserve the author's original style and word choice as closely as possible.
You must answer with just the translated text and nothing else.
Here is the excerpt: {text}'''

chat = ChatOpenAI(model_name=cfg['model_name'], temperature=0, max_tokens=None)
prompt = PromptTemplate.from_template(prompt_template)
llm_chain = LLMChain(llm=chat, prompt=prompt)

chapter_translations = {}

print('Translating...')
for chapter, chunks in tqdm(chapter_chunks.items()):
    translations = []
    for chunk in chunks:
        time.sleep(3)
        output = llm_chain(inputs={'text': chunk})
        translations.append(output['text'])
        
    chapter_translations[chapter] = translations
    with open(cfg['translated_chunks_path'], 'w') as f:
        json.dump(chapter_translations, f)
    
print('Translation compleyed!')
        
# with open(cfg['translated_chunks_path'], 'w') as f:
#     json.dump(chapter_translations, f)
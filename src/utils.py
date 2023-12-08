import tiktoken

def count_tokens(text):
    '''Takes a text and returns the number of tokens in it.'''
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(text)
    return len(tokens)

def merge_sentences(sentences, n):
    '''Takes a list of sentences and returns a list of chunks, where each chunk is obtained
    by merging `n` sentences.'''
    # List of lists, each sublist having `n` sentences
    sentences_groups = [sentences[i:i + n] for i in range(0, len(sentences), n)]
    # List of strings, by merging the sentences in each sublist into a single string
    chunks = []
    for sentences_group in sentences_groups:
        sentences_group_text = ''
        for sentence in sentences_group:
            sentences_group_text += sentence + '.' + ' '
        
        chunks.append(sentences_group_text)   
        
    return chunks

def from_str_to_mp3(client, text, dst):
    '''Takes a strings and does text-to-speech to save a MP3 file.'''
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )    
    response.stream_to_file(dst)

# def is_chapter_start(page_text):
#     '''Check is a page is the starting of a chapter.
    
#     Args:
#         page_text (str): The text of the page.
    
#     Returns:
#         bool: True if the page is the starting of a chapter.
#         int: The chapter number.
#     '''
#     if page_text[:2].isdigit():
#         chapter = int(page_text[:2])
#         return (True, chapter)
#     elif page_text[0].isdigit():
#         chapter = int(page_text[0])
#         return (True, chapter)
#     else:
#         return (False, None)
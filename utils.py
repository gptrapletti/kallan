import tiktoken

def count_tokens(text):
    '''Takes a text and returns the number of tokens in it.'''
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(text)
    return len(tokens)
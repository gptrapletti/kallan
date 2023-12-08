# Källan: from Swedish book to English audiobook
![](cover_kallan_small.jpg)

This project focuses on transforming a Swedish book, previously untranslated into any other language, into an English audiobook. The process begins by translating the book into English using an OpenAI GPT model. Subsequently, a Text-To-Speech (TTS) model, also from OpenAI, is employed to convert the translated text into an audio format.

_Set in the diverse landscapes of central Sweden, the novel spiritualizes nature and intertwines it with reflections on human enigma and childhood memories. The narrative, marked by mysticism and a sensitive, meandering style, portrays the complexity of human endeavors and the inherent ambiguity in our continuous pursuit of understanding._

## Notes
- Both `gpt-3.5-turbo-1106` and `gpt-4-1106-preview` have output token limit equal to 4096, so it's not possible to get the translation of a longer text.
- Text for the TTS model needs to be shorter than 4096 characters.

## Improvements
- Split in chunks within each chapter: so each chunk belongs to only one chapter.
- Add the chapter name at the beginning to each chapter.
- Use a lower number of sentences per chunk (like 10), to stay within TTS limit (4096 characters).
- Use GPT4.

## Todo
- requirements
- notebooks for costs
- write process on readme, with context limits etc
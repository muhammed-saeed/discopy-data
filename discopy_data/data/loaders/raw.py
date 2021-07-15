from typing import List

import spacy

from discopy_data.data.doc import Document
from discopy_data.data.sentence import Sentence
from discopy_data.data.token import Token


def load_texts(texts: List[str], simple_tags=False, nlp=None) -> List[Document]:
    nlp = nlp or spacy.load('en')
    docs = []
    for raw_text in texts:
        words = []
        token_offset = 0
        offset = 0
        sentences = []
        lines = [line.strip() for line in raw_text.splitlines(keepends=True)
                 if line.strip() and len(line.split(' ')) > 1]
        for doc in nlp.pipe(lines):
            sents = list(doc.sents)
            for sent_i, sent in enumerate(sents):
                sent_words = [
                    Token(token_offset + w_i, sent_i, w_i, t.idx + offset, t.idx + len(t.text) + offset,
                          t.text,
                          t.pos_ if simple_tags else t.tag_)
                    for w_i, t in enumerate(sent)
                ]
                words.extend(sent_words)
                token_offset += len(sent_words)
                sentences.append(Sentence(sent_words))
            offset += sum(len(sent.string) for sent in sents) + 1
        docs.append(Document(doc_id=hash(raw_text), sentences=sentences, relations=[]))
    return docs

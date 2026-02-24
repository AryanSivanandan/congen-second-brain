import re
import nltk
from nltk.tokenize import sent_tokenize

def paragraph_chunking(text, max_chunk_size=1000):
    """Split text at paragraph boundaries"""
    # Split by paragraph breaks (double newlines)
    paragraphs = re.split(r'\n\s*\n', text)

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        test_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph

        if len(test_chunk) <= max_chunk_size:
            current_chunk = test_chunk
        else:
            # If current chunk has content, save it
            if current_chunk:
                chunks.append(current_chunk)

            # If single paragraph is too large, split it further
            if len(paragraph) > max_chunk_size:
                # Split long paragraph at sentence boundaries
                sentences = sent_tokenize(paragraph)
                temp_chunk = ""
                for sentence in sentences:
                    if len(temp_chunk + sentence) <= max_chunk_size:
                        temp_chunk += sentence + " "
                    else:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = sentence + " "
                if temp_chunk:
                    chunks.append(temp_chunk.strip())
                current_chunk = ""
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
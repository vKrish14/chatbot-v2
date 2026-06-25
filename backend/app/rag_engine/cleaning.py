import re

class TextCleaner:
    def clean(self, text: str) -> str:
        # Basic text sanitization
        text = text.replace('\x00', '') # remove null bytes
        text = re.sub(r'\s+', ' ', text) # replace multiple spaces/newlines with single space
        return text.strip()

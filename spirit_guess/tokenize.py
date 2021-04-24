
import re

WORD_RE = re.compile(r"(?:[^\W\d_]|['’])+", re.U)

def regex_tokenize(text: str, max_length=4096):
    return WORD_RE.findall(text[:max_length].replace("’", "'"))


from functools import lru_cache
from collections import Counter

import enchant

from spirit_guess.languages import SUPPORTED_LANGUAGES
from spirit_guess.tokenize import regex_tokenize
from spirit_guess.orthography import count_chars_in_blocks
from spirit_guess.ngram_detect import NgramDetect
from spirit_guess.ngram_model import TRIGRAM_MODEL

class EnchantDetect:
    def __init__(self):
        self._languages = set(enchant.list_languages()) & SUPPORTED_LANGUAGES.keys()
        self.enchant_dict = {}
        self._ngrammer = NgramDetect()

    @lru_cache(maxsize=10000)
    def enchant_check(self, token, lang):
        # Fetch the enchant dictionary.
        _edict = self.enchant_dict.get(lang, enchant.Dict(lang))
        return _edict.check(token)

    def detect(self, text, n_best=1, threshold=0.1, lang_set=None):
        tokens = regex_tokenize(text)
        score_per_token = 1 / len(tokens) # Normalize the overall score by len.
        scores = Counter()

        # Try to find a smaller subset of language using `count_chars_in_blocks`
        if not lang_set:
            lang_set = count_chars_in_blocks(text, remove_unknown=True).keys()
        # Filter down the languages to loop through.
        _languages = lang_set & self._languages
        # If there's only one language, just return 100%
        if len(_languages) == 1:
            scores[next(iter(_languages))] = 1.0
        else:  # Iterate through all languages and token.
            for lang in _languages:
                for token in set(tokens):
                    if self.enchant_check(token, lang):
                        scores[lang] += score_per_token
        # If best score, i.e. scores.most_common(1)[0][1] is less than threshold,
        # or no scores, return 'unknown' with 0 prob.
        result = scores.most_common(n_best)
        print(result)
        if not scores or result[0][1] < threshold:
            return ('un', 0.0) if n_best == 1 else [('un', 0.0)]
        else:  # Otherwise return best results.
            return result[0] if n_best == 1 else result

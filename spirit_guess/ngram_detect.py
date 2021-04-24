
import math
from collections import Counter
from functools import lru_cache

from spirit_guess.languages import SUPPORTED_LANGUAGES
from spirit_guess.tokenize import regex_tokenize
from spirit_guess.ngram_model import TRIGRAM_MODEL

class NgramDetect:
    def __init__(self):
        self._languages = TRIGRAM_MODEL.keys() & SUPPORTED_LANGUAGES

    @lru_cache(maxsize=10000)
    def ngram_count(self, text, n=3):
        return Counter(zip(*[text[i:] for i in range(n)]))

    @lru_cache(maxsize=10000)
    def ngram_check(self, trigram, lang, i, max_ngrams=300):
        try:
            return abs(i - TRIGRAM_MODEL[lang].index(list(trigram)))
        except (ValueError, IndexError):
            return max_ngrams

    def detect(self, text, n_best=1, threshold=0.7, lang_set=None, min_len=20, max_ngrams=300):
        # When text is too short, return unknown.
        if len(text) <= min_len:
            return ('un', 0.0) if n_best == 1 else [('un', 0.0)]
        # Compute trigrams.
        trigram_counts = self.ngram_count(text)
        # Filter down the languages to loop through.
        _languages = lang_set & self._languages if lang_set else self._languages
        scores = Counter()
        for lang in _languages:
            for i, (ng, count) in enumerate(trigram_counts.most_common(max_ngrams)):
                scores[lang] += self.ngram_check(ng, lang, i, max_ngrams)

        # If best score is the lowest, i.e. scores.most_common(1)[1] is less than threshold,
        # or no scores, return 'unknown' with 0 prob.
        if not scores:
            return 'un', 0.0 if n_best == 1 else [('un', 0.0)]
        else:  # Otherwise return best results.
            nbest_results = list(reversed(scores.most_common()))[:n_best]
            return nbest_results[0] if n_best == 1 else nbest_results

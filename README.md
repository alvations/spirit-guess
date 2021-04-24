# Spirit Guess

Rewrite of https://pypi.org/project/guess-language/

# Install

To enjoy the benefits of the spellchecker, please install `pyenchant` accordingly http://pyenchant.github.io/pyenchant/install.html

# Usage

```python
from spirit_guess.enchant_detect import EnchantDetect
from spirit_guess.ngram_detect import NgramDetect

fr_en_Latn = """\
France is the largest country in Western Europe and the third-largest in Europe as a whole.
A accès aux chiens et aux frontaux qui lui ont été il peut consulter et modifier ses collections
et exporter Cet article concerne le pays européen aujourd’hui appelé République française.
Pour d’autres usages du nom France, Pour une aide rapide et effective, veuiller trouver votre aide
dans le menu ci-dessus.
Motoring events began soon after the construction of the first successful gasoline-fueled automobiles.
The quick brown fox jumped over the lazy dog."""

```

##  EnchantDetect

Uses spell-checker dicitionary and check it against the words in the dictionary.

```python
>>> enchanter = EnchantDetect()  # Higher score is better.

>>> enchanter.detect(fr_en_Latn)
('fr', 0.5824175824175823)

>>> enchanter.detect(fr_en_Latn, threshold=0.7, n_best=5)
[('un', 0.0)]

>>> enchanter.detect(fr_en_Latn, threshold=0.5, n_best=5)
[('fr', 0.5824175824175823),
 ('en', 0.49450549450549475),
 ('da', 0.23076923076923067),
 ('it', 0.17582417582417578),
 ('af', 0.17582417582417578)]
```

## NgramDetect

Uses the ngram model from the original [https://code.google.com/p/guess-language](https://web.archive.org/web/20120226211749/https://code.google.com/p/guess-language) to detect the text's trigram distance from the ngram model.

```python
>>> ngrammer = NgramDetect()  # Lowest score is better.

>>> ngrammer.detect(fr_en_Latn, n_best=10)
('fr', 68364)

>>> ngrammer.detect(fr_en_Latn, n_best=10)
[('fr', 68364),
('en', 70742),
('ca', 75113),
('la', 75319),
('it', 75917),
('pt', 76059),
('ro', 76652),
('es', 77139),
('da', 77411),
('af', 78301)]
```

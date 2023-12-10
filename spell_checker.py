import re
from collections import Counter


class SpellChecker:
    def __init__(self, dictionary_path):
        """Read the english dictionary"""
        self._words = Counter(self._extract_words(open(dictionary_path, 'r').read()))

    def _extract_words(self, text):
        return re.findall("\w+", text.lower())

    def _frequency_of_word(self, word):
        return self._words[word]/sum(self._words.values())

    def correction(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self._frequency_of_word)

    def candidates(self, word):
        "Generate possible spelling corrections for word."
        return (self._known([word]) or self._known(self._all_edits(word)) or self._known(self._all_edits_2(word)) or [word])

    def _known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self._words)

    def _all_edits(self, word):
        """All words that require one edit only"""
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _all_edits_2(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self._all_edits(word) for e2 in self._all_edits(e1))

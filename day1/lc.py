class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        freq_dict = {}
        for word in strs:
            word_freq = [0] * 26
            for letter in word:
                word_freq[ord(letter) - ord("a")] += 1

            freq_dict.setdefault(tuple(word_freq), []).append(word)

        return [word for word in freq_dict.values()]


# time ~10mins , solved alone: yes, idea: use the frequency of char as key, store all the words with same ferq which are anagrams.

# follow up: if the string is very long, i will use this method since forming the key takes o(k) time and o(1) space, where as normal approach that hashing the wholle sorted letter is o(klogk + k) and hasing takes o(k) space

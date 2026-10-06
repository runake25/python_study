def decodeRunes(runes):
    if not runes:
        return []

    clusters = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }

    words = []
    prefix = []

    def branch(index):
        if index == len(runes):
            words.append("".join(prefix))
            return
        for letter in clusters[runes[index]]:
            prefix.append(letter)
            branch(index + 1)
            prefix.pop()
            print(words)

    branch(0)
    return words




(decodeRunes("23"))
filter
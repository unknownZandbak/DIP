import numpy as np
# import the texts as strings
from data.booknl import textNL
from data.booken import textEN

index_lookup = {
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
    "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
    "t": 19,"u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26, "&": 27
}

textEN = textEN.casefold()
textEN = textEN.replace("\n", "")

textNL = textNL.casefold()
textNL = textNL.replace("\n", "")

def pre_procces() -> str:
    pass

def frequentie(text) -> dict:
    freq = {}

    for i in range(len(text)-1):
        bigramm = f"{text[i]}{text[i+1]}"
        freq[f"{bigramm}"] = freq[f"{bigramm}"]+1 if bigramm in freq else 1
    return freq

def to_freq_matrix(ferqdict: dict) -> np.array():
    pass

if __name__ == "__main__" :
    freqEN = frequentie(textEN)
    freqNL = frequentie(textNL)
    print(freqEN)
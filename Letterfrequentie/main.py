from optparse import Values
import numpy as np
# import the texts as strings
from data.booknl import textNL
from data.booken import textEN

index_lookup = {
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
    "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
    "t": 19,"u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26, "&": 27
}

unique_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "@", ":", "-",
"!", "/", ".", ",", "(", ")", "[", "]", "{", "}", ";", "?", "'", '"', "*", "#", ]

def pre_procces(text: str) -> str:

    text = text.casefold()
    text = text.replace("_", "")
    text = text.replace(u"\n", "")
    text = text.replace(u"\xa0", "")

    for char in unique_characters:
        text = text.replace(char, "&")    
    
    return text

def frequency(text: str) -> dict:
    freq = {}

    for i in range(len(text)-1):
        bigramm = f"{text[i]}{text[i+1]}"
        freq[f"{bigramm}"] = freq[f"{bigramm}"]+1 if bigramm in freq else 1

    return freq

def to_freq_matrix(freqdict: dict) -> np.array:
    freqmatrix = np.zeros((28, 28), dtype=int)
    for bigramm in freqdict:
        char1, char2 = bigramm
        freqmatrix[index_lookup[char1 if char1 in index_lookup else "&"]][index_lookup[char2 if char2 in index_lookup else "&"]] = freqdict[bigramm]
    return freqmatrix

if __name__ == "__main__" :
    textEN = pre_procces(textEN)
    freqEN = frequency(textEN)
    freq_matrixEN = to_freq_matrix(freqEN)

    # textNL = pre_procces(textNL)
    # freqNL = frequency(textNL)
    # freq_matrixNL = to_freq_matrix(freqNL)

    print(freq_matrixEN)
import numpy as np
# import the texts as strings
from data.booknl import bookNL
from data.booken import bookEN

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

def getFreqMatrix(text: str) -> np.array:
    freq = {}

    for i in range(len(text)-1):
        bigramm = f"{text[i]}{text[i+1]}"
        freq[f"{bigramm}"] = freq[f"{bigramm}"]+1 if bigramm in freq else 1
        matrix = to_freq_matrix(freq)
    return matrix

def to_freq_matrix(freqdict: dict) -> np.array:
    freqmatrix = np.zeros((28, 28), dtype=int)
    for bigramm in freqdict:
        char1, char2 = bigramm
        freqmatrix[index_lookup[char1 if char1 in index_lookup else "&"]][index_lookup[char2 if char2 in index_lookup else "&"]] = freqdict[bigramm]
    return freqmatrix

def predict_language(sentence: str):
    """ prediction model of with language the given sentence is writen in.
    Predicts between English and Dutch. 

    Args:
        sentence (str): Given sentence to predict the language of.
    """
    # generate matrix for sentence
    matrix_sentence = getFreqMatrix(sentence)

    diff_score_nl = sum(matrix_bookNL * matrix_sentence)
    diff_score_en = sum(matrix_bookEN * matrix_sentence)

    print(diff_score_en, diff_score_nl)


if __name__ == "__main__" :
    # procces the english book and generate a freq matrix for it
    bookEN = pre_procces(bookEN)
    print(f"Pre-proccesing done on english book")
    print("generating Matrix")
    matrix_bookEN = getFreqMatrix(bookEN)
    print("Done")

    # procces the dutch book and generate a freq matrix for it
    bookNL = pre_procces(bookNL)
    print(f"Pre-proccesing done on dutch book")
    print("generating Matrix")
    matrix_bookNL = getFreqMatrix(bookNL)
    print("Done")

    predict_language("""And so it was indeed! She was now only ten inches high, and her face
                        brightened up at the thought that she was now the right size for going
                        through the little door into that lovely garden.""")

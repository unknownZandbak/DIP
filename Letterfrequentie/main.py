import numpy as np

with open("data/nl/book1.txt") as file:
    bookNL = file.read()

with open("data/en/book2.txt",) as file:
    bookEN = file.read()

index_lookup = {
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
    "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
    "t": 19,"u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26, "&": 27
}

unique_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "@", ":", "-",
"!", "/", ",", "(", ")", "[", "]", "{", "}", ";", "?", "'", '"', "*", "#", ]



def pre_procces(text: str) -> str:
    """pre-procces the text so that weird symbols and unwanted unicode is removed.

    Args:
        text (str): text to preprocces.

    Returns:
        str: proccesed text.
    """
    text = text.casefold()
    text = text.replace("_", "")
    text = text.replace(u"\n", "")
    text = text.replace(u"\xa0", "")

    return text

def getFreqMatrix(text: str) -> np.array:
    """generate and return a frequency matrix for the given text.

    Args:
        text (str): The given piece of text for wich a frequency matrix is generated.

    Returns:
        np.array: The frequency matrix of the given input.
    """
    freq = {}

    for i in range(len(text)-1):
        bigramm = f"{text[i]}{text[i+1]}"
        freq[f"{bigramm}"] = freq[f"{bigramm}"]+1 if bigramm in freq else 1

    # turn the generated dict to a np matrix
    matrix = np.zeros((28, 28), dtype=int)
    for bigramm in freq:
        char1, char2 = bigramm
        matrix[index_lookup[char1 if char1 in index_lookup else "&"]][index_lookup[char2 if char2 in index_lookup else "&"]] = freq[bigramm]
        
    return matrix

def predict_language(sentence: str, matrixNL, matrixEN) -> int:
    """ prediction model of with language the given sentence is writen in.
    Predicts between English and Dutch. 

    Args:
        sentence (str): Given sentence to predict the language of.

    Return:
        predicted language(int): 0(English) or 1(Dutch)
    """
    # generate matrix for sentence
    sentence = pre_procces(sentence)
    matrix_sentence = getFreqMatrix(sentence)

    diff_score_nl = (matrixNL * matrix_sentence).sum()
    diff_score_en = (matrixEN * matrix_sentence).sum()

    if diff_score_en > diff_score_nl:
        return 0
    else: return 1

def genMatrix(book: str):
    """Intermidiate function to create a frequency matrix form a raw piece of text;
    Typically use for larger pieces of text like entire books to use as a model for future predictions.

    Args:
        book (str): The given piece of text for wich a frequency matrix is generated.

    Returns:
        _type_: A frequency matrix of the given input.
    """
    # procces the  book and generate a freq matrix for it
    book = pre_procces(book)

    print("generating Matrix")
    matrix_book = getFreqMatrix(book)

    print("Normalizing Matrix")
    matrix_book = np.divide(matrix_book, matrix_book.sum())

    print("Done")
    return matrix_book

def test_model(test_set: list, matrixNL, matrixEN) -> float:
    """This function tests the model with a set of unseen sentences.

    Args:
        test_set (list): list of sentences in dtring format with a target value.

    Returns:
        float: returns the avg accuracy of the predictions over the entire test set.
    """
    accuracy = []
    for sentence_set in test_set:
        if len(sentence_set[0]) > 10:
            target = sentence_set[1]
            output = predict_language(sentence_set[0], matrixNL, matrixEN)
            if output == target:
                accuracy.append(1)
            else: accuracy.append(0)
        
    return (sum(accuracy)/len(accuracy))*100

def gen_test_set(file_path: str, target: int, delimiter=".")-> list:
    """generate a test set from a given text file.

    Args:
        file_path (str): Path to the you wish to make a test set for.
        target (int): The target value to give the data set.

    Returns:
        list: Return the data set with target values attached to each record.
    """
    test_set = ""
    # generate a test set
    with open(file_path) as file:
        test_set = file.read()
        test_set = pre_procces(test_set)
        test_set = test_set.split(delimiter)
        test_set = list(zip(test_set, [target]*len(test_set)))

    return test_set


if __name__ == "__main__" :
    # procces the dutch book and generate a freq matrix for it
    print("\nProccesing Dutch book")
    matrix_bookNL = genMatrix(bookNL)

    print("\nProccesing English book")
    # procces the english book and generate a freq matrix for it
    matrix_bookEN = genMatrix(bookEN)

    # test the models
    test_set_nl = gen_test_set("data/nl/book3.txt", 1)
    print(f"===========\nTesting Dutch sentences\n--")
    print(f"Lenght of data set (NL):\t{len(test_set_nl)}")
    print(f"Accuracy Score:\t{test_model(test_set_nl, matrix_bookNL, matrix_bookEN)}%")

    test_set_en = gen_test_set("data/en/book1.txt", 0)
    print(f"===========\nTesting English sentences\n--")
    print(f"Lenght of data set:\t{len(test_set_en)}")
    print(f"Accuracy Score:\t{test_model(test_set_en, matrix_bookNL, matrix_bookEN)}%")

    # testing a given file to seperate english and dutch words
    print("\nRunning word sepration task")
    with open("data/sentences-nl-en.txt") as file:
        nl_enSentences = file.read()
    print(f"")
    nl_enSentences = nl_enSentences.replace("."," ")
    nl_enSentences = pre_procces(nl_enSentences)
    nl_enSentences = nl_enSentences.split(" ")
    print(f"===========\nTesting English sentences\n--")
    en_col = []
    nl_col = []
    for word in nl_enSentences:
        result = predict_language(word, matrix_bookNL, matrix_bookEN)
        if result == 0:
            en_col.append(word)
        elif result == 1:
            nl_col.append(word)
    print(f"English collectio: {en_col}")
    print(f"Dutch collection: {nl_col}")

    print(f"lenght en: {len(en_col)}")
    print(f"lenght nl: {len(nl_col)}")


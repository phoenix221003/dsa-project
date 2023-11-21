import re
import string    



def getWordsFromLineList(sentences):
    wordsList = []
    for sentence in sentences:
        wordsList += re.sub('['+string.punctuation+']', '', sentence).split()
    return wordsList

def countFrequency(wordsList):
    wordsWithFrequencies = {}
    for word in wordsList:
        wordsWithFrequencies[word] = wordsWithFrequencies.get(word, 0) + 1
    return list(wordsWithFrequencies.items())

def countFrequencyLength(wordsWithFrequencies):
    frequencies = {}
    for word, frequency in wordsWithFrequencies:
        frequencies[frequency] = frequencies.get(frequency, 0) + 1
    return list(frequencies.items())

def bubble_sort(lst):
    if len(lst) == 1:
        return print(lst)
        
    for i in range(len(lst) - 1): 
        for j in range(0, len(lst) - i -1): 
            if lst[j][1] < lst[j + 1][1]: 
                lst[j], lst[j + 1] = lst[j + 1], lst[j] 
    return lst

def replaceWords(words, maximumFrequencyOccurence, key):
    replacements = {}
    for word, frequency in words:
        if frequency == maximumFrequencyOccurence:
            wordASCII = ""
            for letter in word:
                wordASCII += "{0:03d}".format(ord(letter))
            newWord = "{0:03d}".format(ord(key[0])) + key[:len(key) // 2] + str(wordASCII) + key[len(key) // 2:] + "{0:03d}".format(ord(key[-1]))
            replacements[word] = newWord
    return replacements
    
def replaceInput(words, replacedWords):
    for word, replacement in replacedWords.items():
        if word in words:
            index = words.index(word)
            words[index] = replacement
    return words

def returnEncryptedData(encryptedWords):
    return " ".join(encryptedWords)


def init(data, key):
    print(data)
    if type(data) == list:
        data = "".join(data)

    if not key:
        key = generateKey()
    
    sentences = data.lower().split(".")[:-1]

    words = getWordsFromLineList(sentences)
    wordsWithFrequencies = countFrequency(words)
    frequencies = countFrequencyLength(wordsWithFrequencies)
    maximumFrequencyOccurence = bubble_sort(frequencies)[0][0]
    replacedWords = replaceWords(wordsWithFrequencies, maximumFrequencyOccurence, key)
    encryptedWords = replaceInput(words, replacedWords)
    encryptedData = returnEncryptedData(encryptedWords)

    return encryptedData

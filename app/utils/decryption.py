def replace(word, replacements):
    word = word[:3].replace(replacements[0], "") + word[3:-3] +  word[-3:].replace(replacements[-1], "")
    for replacement in replacements[1:-1]:
        word = word.replace(replacement, "")
    return word

def enQueue(queue, item, priority = 0):
    queue.append((item, priority))


def removeKey(words, key):
    keyLessWords = []
    key0 = str(ord(key[0]))
    key1 = key[:len(key) // 2]
    key2 = key[len(key) // 2:]
    key3 = str(ord(key[-1]))
    for word in words:
        priority = 0
        if word[:3] == key0:
            word = replace(word, [key0, key1, key2, key3])
            priority = 1
        enQueue(keyLessWords, word, priority)
    return keyLessWords
    
def convertEncryptedToWords(encrypted):
    words = []
    for word, level in encrypted:
        if level == 1:
            word = "".join([str(chr(int(word[i:i+3]))) for i in range(0, len(word), 3)])
        words.append(word)
    return words
        
def wordsToFile(words):
    return " ".join(words)

def init(encrypted, key):
    print(key)
    words = encrypted.lower().split(" ")[:-1]
    keyLessWords = removeKey(words, key)
    replacedWords = convertEncryptedToWords(keyLessWords)  
    print(replacedWords)
    result = wordsToFile(replacedWords)
    print(result) 
    return

    
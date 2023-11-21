# ? imports ( Flask )
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import string    
import random
import re
from flask_mail import Mail, Message

# Setting constansts
UPLOAD_FOLDER = 'uploads'
KEY_LENGTH = 12
FILENAME = "test.txt"

# ? Creating app with Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# setting smtp sever variables
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'travellingdiaries2019@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Travel1234'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

# Genrating a random key if user donot provide key
def generateKey():
    ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k = KEY_LENGTH))    
    key = str(ran)
    return key

#  removing punctutation from the file
def removePunctuation(data):
    data = re.sub(r"[,.;@#?!&$]+\ *", " ", data)
    return data

#  Converting file to words
def getWordsFromLineList(data):
    return data.split(" ")

# counting frequency of words
def countFrequency(wordsList):
    wordsWithFrequencies = {}
    for word in wordsList:
        wordsWithFrequencies[word] = wordsWithFrequencies.get(word, 0) + 1
    return list(wordsWithFrequencies.items())

# counting frequency occurenece 
def countFrequencyLength(wordsWithFrequencies):
    frequencies = {}
    for word, frequency in wordsWithFrequencies:
        frequencies[frequency] = frequencies.get(frequency, 0) + 1
    return list(frequencies.items())

# sorting algorithm
def mergeSort(arr):
    if len(arr) > 1:
 
         # Finding the mid of the array
        mid = len(arr)//2
 
        # Dividing the array elements
        L = arr[:mid]
 
        # into 2 halves
        R = arr[mid:]
 
        # Sorting the first half
        mergeSort(L)
 
        # Sorting the second half
        mergeSort(R)
 
        i = j = k = 0
 
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

## turning words into encrypted words
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

# replacing words with encrypted words 
def replaceInput(words, replacedWords):
    for word, replacement in replacedWords.items():
        if word in words:
            index = words.index(word)
            words[index] = replacement
    return words

# joining words to build paragraph again
def returnEncryptedData(encryptedWords):
    return " ".join(encryptedWords)


# initliazing encryption
def initEncryption(data, key):
    # converting data from list to str
    if type(data) == list:
        data = "".join(data)

    # checking if key is empty or not
    if not key:
         # generatting key if it is empty
        key = generateKey()
    # remving footer of our app from the file
    data = removeDetails(data, "Decryption")
    print(data)
    # applying all the functions made above
    
    data = removePunctuation(data)
    words = getWordsFromLineList(data)
    wordsWithFrequencies = countFrequency(words)
    print(wordsWithFrequencies)
    frequencies = countFrequencyLength(wordsWithFrequencies)
    maximumFrequencyOccurence = mergeSort(frequencies)[0][0]
    replacedWords = replaceWords(wordsWithFrequencies, maximumFrequencyOccurence, key)
    encryptedWords = replaceInput(words, replacedWords)
    encryptedData = returnEncryptedData(encryptedWords)
    
    # finally returing encrypted data
    return encryptedData

# replacing ids from words
def replace(word, replacements):
    word = word[:3].replace(replacements[0], "") + word[3:-3] +  word[-3:].replace(replacements[-1], "")
    for replacement in replacements[1:-1]:
        word = word.replace(replacement, "")
    return word

# initalized a queue for handling encrypted and non-encrypted textx
def enQueue(queue, item, priority = 0):
    queue.append((item, priority))

# removing keey from encrypted text
def removeKey(words, key):
    if len(key) < 12:
        return None
    keyLessWords = []
    key0 = "{0:03d}".format(ord(key[0]))
    key1 = key[:len(key) // 2]
    key2 = key[len(key) // 2:]
    key3 = "{0:03d}".format(ord(key[-1]))
    print(key1, key2)
    
    for word in words:
        priority = 0
        if word[:3] == key0 and key1 == word[3:9]:
            word = replace(word, [key0, key1, key2, key3])
            priority = 1
        enQueue(keyLessWords, word, priority)
    return keyLessWords
    
# checking if key is correct or not 
def checkDecryption(keyLessWords):
    keyError = True
    for word, level in keyLessWords:
        if level == 1:
            keyError = False
    return keyError

# convert encrypted words to words
def convertEncryptedToWords(encrypted):
    if checkDecryption(encrypted):
        return None
    words = []
    for word, level in encrypted:
        if level == 1:
            word = "".join([str(chr(int(word[i:i+3]))) if word[i:i+3].isdigit() else word[i:i+3] for i in range(0, len(word), 3)])
        words.append(word)
    return words
        
# Converting words to file
def wordsToFile(words):
    return " ".join(words)

# initializing decryption
def initDecryption(encrypted, key):
    encrypted = removeDetails(encrypted, "Encryption")
    words = encrypted.lower().split(" ")[:-1]
    keyLessWords = removeKey(words, key)
    print(keyLessWords)
    if keyLessWords:
        print(keyLessWords, "0000000000000")
        replacedWords = convertEncryptedToWords(keyLessWords)  
        if replacedWords:
            result = wordsToFile(replacedWords)
            return result
    return None

# removing footer
def removeDetails(result, type):
    copyrightLine = f"  {type} by Encryptor - project from Harikrishna, Mohit, Nikhil and Aalay "
    result = result.replace(copyrightLine, "")
    return result

# ADding footer
def addDetails(result, type):
    copyrightLine = f"  {type} by Encryptor -  project from Harikrishna, Mohit, Nikhil and Aalay "
    return result + copyrightLine


# Routes

# Index route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        _type = request.form.get("type")
        print(_type) 

        # Encryption
        if _type == "encryption":
            uploaded_file = request.files['eFile']
            key = request.form.get("key")
            if key == "" or not key:
                key = generateKey()
            print(key)
            if uploaded_file.filename != '':
                # saving file in uploads dir
                file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], file))
                encrypted = ""
                path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER']) + f"/{file}"
                # reading file
                with open(path, "r") as fileReader:
                    # applying encryption
                    encrypted = initEncryption(fileReader.read(), key)
                    # adding footer of our app
                if encrypted:
                    encrypted = addDetails(encrypted, "Encryption")
                    # re-writting file
                with open(path, "w") as fileWriter:
                    fileWriter.write(encrypted)
                    # return result route with key and filename
                return redirect(url_for("result", key=key, filename=file))
        
        # Decryption
        else:
            uploaded_file = request.files['dFile']
            key = request.form.get("dKey")
            if uploaded_file.filename != '':
                file = secure_filename(uploaded_file.filename)
                print(file)
                # saving file in uploads dir
                uploaded_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], file))
                decrypted = ""
                path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER']) + f"/{file}"
                # print(path, "-------------------------------------")
                # reading file
                with open(path, "r") as fileReader:
                    decrypted = initDecryption(fileReader.read(), key)
                    # adding footer of our app
                if decrypted:
                    decrypted = addDetails(decrypted, "Decryption")
                    # checking if key is right or wrong
                if decrypted == "" or not decrypted:
                    # return error route
                    return redirect(url_for('error'))
                    # re-writting file
                with open(path, "w") as fileWriter:
                    fileWriter.write(decrypted)
                    # return result route with key and filename
                return redirect(url_for("result", key=key, filename=file))  
        return redirect(url_for('index'))
    return render_template('index.htm')

# Result route
@app.route("/result", methods=["GET"])
def result():
    key = request.args.get("key")
    filename = request.args.get("filename")
    if key == "" or not key:
        # if not key return to index
        return redirect(url_for('index'))
    # return result page with key and filename
    return render_template("result.htm",  key=key, filename=filename)

# Download route
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER']) + f"/{filename}"
    # download file 
    return send_file(uploads, as_attachment=True)

# Error route
@app.route("/error", methods=["GET"])
def error():
    # render error page
    return render_template("error.htm")

# Mailing route
# @app.route("/sendMail")
# def sendMail():
#     # sending mail with smtp server

#     key = request.args.get("key")
#     filename = request.args.get("filename")
#     email = request.args.get("email")
#     msg = Message('Your file is ready', sender = 'travellingdiaries2019@gmail.com', recipients = [email])
#     msg.body = f"Key = {key} Enjoy !!"
#     uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER']) + f"/{filename}"
#     print(uploads)
#     with app.open_resource(uploads) as fp:        
#         msg.attach("file.txt", "text/txt", fp.read())
#     mail.send(msg)
#     return redirect(url_for('index'))
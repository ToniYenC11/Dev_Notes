def casesar_v2(message,cipherKey,alphabet):
    encrypted_message = ""
    upper_message = message.upper()
    
    for letter in upper_message:
        position = alphabet.find(letter)
        new_position = position + cipherKey
        if letter in alphabet:
            encrypted_message = encrypted_message + alphabet[new_position]
        else:
            encrypted_message = encrypted_message + letter
        
    return encrypted_message

def decrypt_caesar(message,cipherKey,alphabet):
    decryptKey = -1 * cipherKey
    return casesar_v2(message, decryptKey, alphabet).title()

def getMessage():
    message = input("Enter your message here: ")
    return message
def getCipherKey():
    CipherKey = int(input("Enter whole number between 1-25: "))
    return CipherKey
    
def runCaesarCipherProgram():
    myAlphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(f'Alphabet: {myAlphabet}')
    myAlphabet2 = myAlphabet*2
    print(f'Alphabet2: {myAlphabet2}')
    myMessage = getMessage()
    print(myMessage)
    myCipherKey = getCipherKey()
    print(myCipherKey)
    myEncryptedMessage = casesar_v2(myMessage, myCipherKey, myAlphabet2)
    print(f'Encrypted Message: {myEncryptedMessage}')
    myDecryptedMessage = decrypt_caesar(myEncryptedMessage, myCipherKey, myAlphabet2)
    print(f'Decypted Message: {myDecryptedMessage}')

runCaesarCipherProgram()
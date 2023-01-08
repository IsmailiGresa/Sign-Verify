import sys
import random
import math
from pathlib import Path

def generatePrime():	
	p = random.randint(100, 1000) #Generating a random number between 100 and 1000
	while not isPrime(p): #Checking if the number is prime or not
		p = random.randint(100, 1000) #Generating again if it is not prime
	return p

def isPrime(n): #Defining function to check if a number is prime or not
	for i in range(2, int(math.sqrt(n)) + 1): #Looping over numbers from 2 to the square root of n
		if n % i == 0: #Returning false if n is divisible by i
			return False
	return True #Returning true if n is not divisible by any number

def generatePubKey(): #Defining function to generate private and public keys
    p = generatePrime() #Generating two prime numbers
    q = generatePrime()
    n = p * q #Calculating n and phi
    phi = (p - 1) * (q - 1)
    e = random.randint(1, phi)#Generating a random number between 1 and phi
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi) #Generating again if they are not coprime
    for d in range(1, phi): #Calculating d such that (d * e) % phi = 1
    	if (d * e) % phi == 1:
            break
    return (e, n) #Returning the public and private keys

def generatePrivKey(): #Defining function to generate private and public keys
    p = generatePrime() #Generating two prime numbers
    q = generatePrime()
    n = p * q #Calculating n and phi
    phi = (p - 1) * (q - 1)
    e = random.randint(1, phi)#Generating a random number between 1 and phi
    while math.gcd(e, phi) != 1:
        e = random.randint(1, phi) #Generating again if they are not coprime
    for d in range(1, phi): #Calculating d such that (d * e) % phi = 1
    	if (d * e) % phi == 1:
            break
    return (d, n) #Returning the public and private keys

def createUser(name):
	print("User " + name + " has been created!")
	publicKey = generatePubKey()
	privateKey= generatePrivKey()
	f = open("keys/" + name + ".priv.json", "w")
	f.write(str(publicKey))
	f1 = open("keys/" + name + ".pub.json", "w")
	f1.write(str(privateKey))
	f2 = open(name + ".json", "x")

def encryptMessage(message, name):
    e, n = getpubKeyFromFile(name)
    message = int(message)
    k = random.randint(1, (n - 1))
    a = pow(k, e, n)
    b = (message * pow(a, e, n)) % n
    return (a, b)

def decryptMessage(cipher, name):
    d, n = getprivKeyFromFile(name)
    cipher = getMsgFromFile(name)
    a, b = cipher
    plaintxt = (b * pow(a, d, n)) % n
    return plaintxt

def signMessage(message, name): #Defining function to sign message using ElGamal
    d, n = getprivKeyFromFile(name)
    messageHash = hash(message) #Calculating the hash of the message
    k = random.randint(2, n - 1) #Generating k such that 1 < k < n
    r = pow(k, d, n) #Calculating r and s
    s = (messageHash - (d * r)) * (n**(k-1)) % n
    return (r, s) #Returning the signature

def verifySignature(message, signature, name): #Defining function to verify the signed message
    e, n = getpubKeyFromFile(name)
    messageHash = hash(message) #Calculating the hash of the message
    r, s = getSgnFromFile(name) #Unpacking the signature
    r, s = signature
    v = pow(s, e, n) * r % n #Calculating v
    if v == messageHash: #Checking if v and the hash of the message are equal
        return True
    else:
    	return False

def writeMessage(message, sender, receiver):
    signature = signMessage(message, sender)
    message = encryptMessage(message, receiver)
    my_file = Path("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + sender + ".json")
    if my_file.is_file():
        print("Sender: " + sender)
        print("Receiver: " + receiver)
        f =  open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json", 'w')
        data = f.write(str(message))
        print("Message written in file: " + "C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json")
        f = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json", "a")
        f1 =  open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + sender + ".sign.json", 'x')
        f1.write(str(signature))
        print("Signature written in file: " + "C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".sign.json")

def readMessage(cipher, receiver, sender):
    cipher = getMsgFromFile(receiver)
    message = decryptMessage(cipher, sender)
    signature = getSgnFromFile(receiver)
    verify = verifySignature(message, signature, sender)
    print("Receiver: " + receiver)
    print("Sender: " + sender)
    my_file = Path("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json")
    if my_file.is_file():
        f =  open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json", 'r')
        data = f.read() 
    if(message == cipher):
       print("Message: " + cipher)
    else:
        print("Message decryption failed!")
    if verify == True:
        print("Signature: Verified successfully!")
    else:
    	print("Signature: Verification failed!")

def getpubKeyFromFile(name):
    filePath = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/keys/" + name + ".pub.json", "r")
    pubKey = filePath.readline()
    if pubKey is not None:
        pub = str(pubKey).strip('( )')
        e = pub.split(",")[0]
        n = pub.split(", ")[1]
        return (int(e), int(n))

def getprivKeyFromFile(name):
    filePath = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/keys/" + name + ".priv.json", "r")
    privKey = filePath.readline()
    if privKey is not None:
        priv = str(privKey).strip('( )')
        d = priv.split(",")[0]
        n = priv.split(", ")[1]
        return (int(d), int(n))

def getMsgFromFile(name):
    filePath = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + name + ".json", "r")
    msg = filePath.readline()
    if msg is not None:
        message = str(msg).strip('( )')
        a = message.strip(" ").split(",")[0]
        b = message.split(", ")[1]
        return (int(a), int(b))

def getSgnFromFile(name):
    filePath = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + name + ".sign.json", "r")
    sign = filePath.readline()
    if sign is not None:
        signature = str(sign).strip('( )')
        r = signature.strip(" ").split(",")[0]
        s = signature.split(", ")[1]
        return (int(r), int(s))

if(sys.argv[1] == "create-user"):
    createUser(sys.argv[2])
elif(sys.argv[1] == "write-message"):
    writeMessage(sys.argv[2], sys.argv[3], sys.argv[4])
elif(sys.argv[1] == "read-message"):
    readMessage(sys.argv[2], sys.argv[3], sys.argv[4])
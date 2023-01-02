import sys
import random
import math
from pathlib import Path
import ast

def generate_prime():	
	p = random.randint(100, 1000) #Generating a random number between 100 and 1000
	while not is_prime(p): #Checking if the number is prime or not
		p = random.randint(100, 1000) #Generating again if it is not prime
	return p

def is_prime(n): #Defining function to check if a number is prime or not
	for i in range(2, int(math.sqrt(n)) + 1): #Looping over numbers from 2 to the square root of n
		if n % i == 0: #Returning false if n is divisible by i
			return False
	return True #Returning true if n is not divisible by any number

def generatePubKey(): #Defining function to generate private and public keys
    p = generate_prime() #Generating two prime numbers
    q = generate_prime()
    n = p * q #Calculating n and phi
    phi = (p - 1) * (q - 1)
    e = random.randint(1, phi)#Generating a random number between 1 and phi
    while math.gcd(e, phi) != 1:
        e = random.randint(1, phi) #Generating again if they are not coprime
    for d in range(1, phi): #Calculating d such that (d * e) % phi = 1
    	if (d * e) % phi == 1:
            break
    return (e, n) #Returning the public and private keys

def generatePrivKey(): #Defining function to generate private and public keys
    p = generate_prime() #Generating two prime numbers
    q = generate_prime()
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

def signMessage(message, name): #Defining function to sign message using ElGamal
    privateKey = getprivKeyFromFile(name) 
    messageHash = hash(message) #Calculating the hash of the message
    d, n = generatePrivKey() #Unpacking the private key
    k = random.randint(1, n - 1) #Generating k such that 1 < k < n
    r = pow(k, d, n) #Calculating r and s
    s = (messageHash - (d * r)) * (n**(k-1)) % n
    return (r, s) #Returning the signature

def verifySignature(message, signature, name): #Defining function to verify the signed message
    publicKey = getprivKeyFromFile(name) 
    signature = signMessage(message, name)
    messageHash = hash(message) #Calculating the hash of the message
    r, s = signature #Unpacking the signature
    e, n = generatePubKey() #Unpacking the public key
    v = pow(s, e, n) * r % n #Calculating v
    if v == messageHash: #Checking if v and the hash of the message are equal
        return True
    else:
    	return False

def writeMessage(message, sender, receiver):
    signature = signMessage(message, sender)
    my_file = Path("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + sender + ".json")
    if my_file.is_file():
        print("Sender: " + sender)
        f =  open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json", 'w')
        f.write(message + "\n")
        print("Message written in file: " + "C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json")
        f = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json", "a")
        print("Receiver: " + receiver)
        f = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json", "a", encoding="utf-8")
        f.write(str(signature))

def readMessage(message, receiver, sender):
    signature = signMessage(message, sender)
    verify = verifySignature(message, signature, sender)
    print("Receiver: " + receiver)
    print("Sender: " + sender)
    my_file = Path("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json")
    if my_file.is_file():
        f =  open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/" + receiver + ".json", 'r')
        data = f.read() 
        data_list = data.split() 
        integers = [int(x) for x in data_list if x.isdigit()] # to access the integers
        strings = [x for x in data_list if not x.isdigit()] # to access the strings
    if verifySignature(message, signature, sender):
        print("Signature: Verified successfully!")
    else:
    	print("Signature: Verification failed!")

def getpubKeyFromFile(name):
    try:
        filePath = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/keys/" + name + ".pub.json", "r")
        pubKey = filePath.readline()
        return pubKey
    except Exception as e:
        return None

def getprivKeyFromFile(name):
    try:
        filePath = open("C:/Users/IFES Yoga/Documents/GitHub/Sign-Verify/keys/" + name + ".priv.json", "r")
        privKey = filePath.readline()
        return privKey
    except Exception as e:
        return None

if(sys.argv[1] == "create-user"):
    createUser(sys.argv[2])
elif(sys.argv[1] == "write-message"):
    writeMessage(sys.argv[2], sys.argv[3], sys.argv[4])
elif(sys.argv[1] == "read-message"):
    readMessage(sys.argv[2], sys.argv[3], sys.argv[4])
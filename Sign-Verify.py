import sys
import random
import math
import pickle

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
	f = open(name+".json", "wb")
	pickle.dump(publicKey, f)
	f1 = open(name+".pub.json", "wb")
	pickle.dump(privateKey, f1)


def writeMessage(message, sender, reciever):
    print("Message was saved in file")

def readMessage(message, receiver, sender):
    print("Veq diqka me dal")

if(sys.argv[1] == "create-user"):
    createUser(sys.argv[2])
elif(sys.argv[1] == "write-message"):
    writeMessage(sys.argv[2], sys.argv[3], sys.argv[4])
elif(sys.argv[1] == "read-message"):
    readMessage(sys.argv[2], sys.argv[3], sys.argv[4])



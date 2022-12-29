import sys

def createUser(name):
    print("User " + name + " has been created!")
    f = open(name+".xml", "x")



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


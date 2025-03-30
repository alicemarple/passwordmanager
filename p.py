import pymongo
import base64
import random
import sys
from dotenv import dotenv_values



# configuring and loading the .env file
config = dotenv_values(".env")
usernameDB = config["USERNAME"]
passwordDB = config["PASSWORD"]



# function for generate the password

uppercaseLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercaseLetters = uppercaseLetters.lower()
digits = "1234567890"
symbols = "!#$&*()+=-?[]{}"

def generatePassword():
    allstr = uppercaseLetters + lowercaseLetters + digits + symbols
    lengthOfPassword = 10
    password = "".join(random.sample(allstr, lengthOfPassword))
    return password



print("hola!")
# connect the database
client = pymongo.MongoClient(f"mongodb+srv://{usernameDB}:{passwordDB}@pass.9xxj1.mongodb.net/?retryWrites=true&w=majority&appName=pass")
db = client["passwords"]
collection = db["all"]
operation = sys.argv[1]

# creating the password in database
def createData():
    username = input("Enter your username : ")
    password = generatePassword()
    # encoding 
    encode_bytes = base64.b64encode(password.encode())
    x = collection.insert_one({"username": f"{username}", "password":encode_bytes})
    print(x) 
    print(f"your password is {password}.")  


# reading data from the database
def readData():
    requsername = input("Enter which password you want : ")
    x = collection.find_one({"username":f"{requsername}"})
    # decode
    y = x["password"].decode()
    finalpassword = base64.b64decode(y)
    print(f"your password of the {requsername} is {finalpassword}.")

# update data in database

def updateData():
    usernameForUpdate = input("Enter username of which password you want update : ")
    newpassword = generatePassword()
    newEncodeBytes = base64.b64encode(newpassword.encode())
    x = collection.update_one({"name":usernameForUpdate}, {"$set":{"password":newEncodeBytes}})
    print(x)
    print(f"your upadated password is {newpassword}.")



# delete data from the database

def deleteData():
    usernameForDelete = input("Enter a username of which password you want to delete : ")
    x =  collection.delete_one({"name":usernameForDelete})
    print(x)



# conditions for the inputs 
if (operation == "-c"):
    createData()
elif(operation == "-r"):
    readData()
elif(operation == "-u"):
    updateData()
elif(operation == "-d"):
    deleteData()
else:
    print("Enter valid option!")



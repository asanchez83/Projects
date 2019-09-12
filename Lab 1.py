#Written by: Adrian Sanchez
#Prof: Diego Aguirre
#Class: Data Structures 2302
#Lab: 1
#Date completed: 9/12/19

import hashlib
def hash_with_sha256(str):
    hash_object = hashlib.sha256(str.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig
#compares generated string after being hashed
def compare(cur_perm):
    filename = "password_file.txt"
    f = open(filename, 'r')
    line = f.readline()
    while line:
        currentline = line.split(",")
        salt = str(currentline[1])   #salt value, hashed password and user taken from file
        hash_p = str(currentline[2])
        user = str(currentline[0])
        
        s_salt = cur_perm + salt    #string to pass into hashing method
        attempt = hash_with_sha256(s_salt)  #hashed number to compare
        if(hash_p == attempt):
            print("Matched " + attempt + " with " + hash_p + " for user " + user  )
            print("Password is: " + cur_perm)
        line = f.readline()
    f.close()
    
def brutus(s, unusedlist, length):
    if len(s) == length:    #checks if length matches the one required
        return compare(s)
        #return s
    for j in range(0,10):
        brutus(s + str(j),unusedlist, length) #recursively calls the method with an increased string

#needed range fed into for loop, then into the method call
for x in range(3,8):
    s = ""
    brutus(s, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], x)









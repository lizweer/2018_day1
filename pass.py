#something new

import pickle
import random

def get_credentials():
    username = input("Enter your username: ")
    password = input("Enter password: ")
    return username, password

def authenticate(user, pw, pwdb):
    status = False
    if user in pwdb:
        if pwdb[user][0] == hash_pw(pw, pwdb[user][1]):
            status = True
    return status

def add_user(user, pw, pwdb):
    if not user in pwdb:
        salt = random.randint(2,2*16)
        hash = hash_pw(pw,salt)
        pwdb[user] = (hash,salt)
    else:
        print("User already exists!")

def read_pwdb(pwdb_path):
    try:
        with open(pwdb_path, 'rb') as pwdb_file:
            pwdb = pickle.load(pwdb_file)
    except FileNotFoundError:
        pwdb = {}
        salt = 27496
        hash = hash_pw('admin',salt)
        pwdb['admin'] = (hash,salt)
    return pwdb

def write_pwdb(pwdb, pwdb_path):
    with open(pwdb_path, 'wb') as pwdb_file:
        pickle.dump(pwdb, pwdb_file)

def hash_pw(pw, salt):
    hash = 3 #this is changed
    for i, char in enumerate(pw):
        hash += ord(char)*salt*(i+1)
    return hash

if __name__=="__main__":
    pwdb_path = './tmp/pwdb.pkl'
    pwdb = read_pwdb(pwdb_path)
    user, pw = get_credentials()
    auth = authenticate(user, pw, pwdb)
    if auth:
        answer = input("Add user to database?: ")
        while answer=='yes' or answer=='y':
            u, p = get_credentials()
            add_user(u,p,pwdb)
            answer = input("Add user to database?: ")
        write_pwdb(pwdb,pwdb_path)
        print(pwdb)
    else:
        print("Wrong user/password")

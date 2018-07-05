# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 13:38:01 2018

@author: TOMAS
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  12 14:44:02 2017

@author: gita
"""

#from flask import Flask, render_template, flash, request,session, redirect,url_for, make_response
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from pymongo import MongoClient,ASCENDING #Manejos de base de datos
import pandas as pd
import numpy as np
import os
import pprint
#from random import randint
import hashlib
import string
import random

#Codificar contrasenna 
def hash_pass(password):
    salt = os.urandom(hashlib.blake2b.SALT_SIZE)
    salt_hash = hashlib.blake2b(salt=salt)
    salt_hash.update(password.encode('utf-8'))
    hash_password = salt_hash.digest()
    return hash_password,salt

def pass_generator(size=8, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for x in range(size))

##Crear Base de datos
##Crear cliente
client = MongoClient()
#
##Crear database
db = client.IPS_database
Users_data = db.Users_collection
usertag = "usuario"

hpassw,salt = hash_pass('consalGOB01!') 
Users_IPS = {
    usertag:'mincol01', 
    "password":hpassw,
    "salt":salt,
    'role':'gob',
    'ID':1,#toco :(
    'user_id':1
    }       
Users_data.insert_one(Users_IPS) 


#for doc in documents:
#    try:
#        # insert into new collection
#    except pymongo.errors.DuplicateKeyError:
#        # skip document because it already exists in new collection
#        continue
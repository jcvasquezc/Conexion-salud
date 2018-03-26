#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  12 14:44:02 2017

@author: gita
"""

from flask import Flask, render_template, flash, request,session, redirect,url_for, make_response
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from pymongo import MongoClient,ASCENDING #Manejos de base de datos
import pandas as pd
import numpy as np
import os
import pprint
from random import randint
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

#Directorio de proyecto
main_path = os.path.dirname(os.path.abspath(__file__))

##Crear Base de datos
##Crear cliente
client = MongoClient()
#
##Crear database
db = client.IPS_database
client.drop_database('IPS_database')

##Crear colecciones
IPS_data  = db.IPS_collection
Users_data = db.Users_collection
#Crear indice para usuarios
usertag = "usuario"
db.Users_data.create_index([(usertag,ASCENDING)],unique=True)

##Delete collection
db.IPS_collection.drop()

#Obtener lista de departamento y ciudades
#info_IPS = pd.read_csv(main_path+'/static/listaDB.csv')
info_IPS = pd.read_csv(main_path+'/static/BD_SEDES.csv')
#Obtener departamentos
df = pd.DataFrame(info_IPS)
#Reemplazar datos faltantes
df = df.replace(np.nan,'')
passw = []
idx_usr = 0 #Index for username

for idx_ips in range(0,df.shape[0]):
    ips = df.iloc[[idx_ips]]
    dpto = list(ips['DEPARTAMENTO'])[0]
    city = list(ips['MUNICIPIO'])[0]
    codhab = str(list(ips['CÓDIGO'])[0])#Codigo habilitacion
    nombreIPS = list(ips['NOMBRE'])[0]#Nombre del prestador de servicios
    nit = str(list(ips['NIT'])[0])
    razsoc = list(ips['RAZÓN SOCIAL'])[0]
    addr = list(ips['DIRECCION'])[0] 
    barr = list(ips['BARRIO'])[0] 
    tel = str(list(ips['TELEFONO'])[0])
    tel = tel.replace('\n',' ')     
    email = list(ips['E-MAIL EMPRESARIAL'])[0]#email del prestador de servicios   
    email = email.replace('\n',' ')    
    email = email.replace(';','')   
    email2 = list(ips['E-MAIL 2 EMPRESARIAL'])[0]#email del prestador de servicios   
    email2 = email2.replace('\n',' ')    
    email2 = email2.replace(';','')   
    ger = list(ips['GERENTE'])[0]   
    repre = list(ips['NOMBRE DEL REPRESENTANTE LEGAL'])[0]#Represenante legal    
    emailrep = list(ips['E-MAIL REPRESENTANTE LEGAL'])[0]#email del prestador de servicios   
    emailrep = emailrep.replace('\n',' ')    
    emailrep = emailrep.replace(';','')   
    telrep = str(list(ips['TELEFONO REPRESENTANTE LEGAL'])[0])
    telrep = telrep.replace('\n',' ')  
    niv = list(ips['NIVEL DE ATENCIÓN'])[0]#Nivel del prestador de servicios 
    usr = list(ips['NOMBRE PERSONA ENCARGADA DE TECNOLOGIA'])[0]
    usrmail = list(ips['EMAIL PERSONA ENCARGADA DE TECNOLOGIA'])[0]
    usrtel = list(ips['TELEFONO PERSONA ENCARGADA DE TECNOLOGIA'])[0]
    
    
    #Ingreso de usuario para login
    #IPS_data.update({"NIT":nit}, {'$push':{'Usuarios':{"Usuario":nit, "password":hash_pass(userpass)}}}, upsert=False)
    temppass = nit[-4:]
    userpass = pass_generator()#car[1]+temppass[3]+temppass[0]+car[-1:]+temppass[1]+temppass[2]+car[len(car)-2]+car[0]
    idx_usr = idx_usr+1
    username = 'saludcol'+str(idx_usr)
    dfpass = pd.DataFrame(np.reshape([dpto,city,codhab,username,userpass],(1,5)))
    passw.append(dfpass)
    hpassw,salt = hash_pass(userpass)
    
    IPS_index_data = {
                  "Validar INFO":False,
                  "Código Habilitación":codhab,
                  "ID":int(str(codhab+str(idx_usr))),
                  "Nombre del Prestador":nombreIPS,
                  "NIT":nit,
                  "Razón social":razsoc,
                  "Nivel del Prestador":niv,#str(int(niv)) if niv else 0,
                  "Gerente":ger,
                  "Dirección":addr,
                  "Barrio":barr,
                  "Municipio":city,
                  "Departamento":dpto,
                  "Teléfono":tel,
                  "E-mail empresarial":email,
                  "E-mail empresarial 2":email2,
                  "Representante legal":repre,
                  "E-mail del representante":emailrep,
                  "Teléfono del representate":telrep,
                  "Encargado de Encuesta":usr,
                  "E-mail del Encargado":usrmail,
                  "Teléfono del Encargado":usrtel,
                  "colaborador1 nombre":"",
                  "colaborador2 nombre":"",
                  "colaborador3 nombre":"",
                  "colaborador4 nombre":"",
                  "colaborador5 nombre":"",
                  "colaborador6 nombre":"",
                  "colaborador1 cargo":"",
                  "colaborador2 cargo":"",
                  "colaborador3 cargo":"",
                  "colaborador4 cargo":"",
                  "colaborador5 cargo":"",
                  "colaborador6 cargo":"",
                  "colaborador1 email":"",
                  "colaborador2 email":"",
                  "colaborador3 email":"",
                  "colaborador4 email":"",
                  "colaborador5 email":"",
                  "colaborador6 email":"",
                  #"Número de sedes":Nsed,
                  "Resultados Modulo 1":{},
                  "Resultados Modulo 2":{},
                  "Resultados Modulo 3":{},
                  "Resultados Modulo 4":{},
                  "Resultados Modulo 5":{},
                  "Resultados Modulo 6":{},
                  }
    Users_IPS = {
                usertag:username, 
                "password":hpassw,
                "salt":salt,
                "Codigo":codhab,
                'role':'manager',
                'user_id':int(str(codhab+str(idx_usr)))
                }
    
    #Llenar base de datos
    IPS_data.insert_one(IPS_index_data).inserted_id  
    Users_data.insert_one(Users_IPS).inserted_id  

tabla = pd.concat(passw)
tabla = tabla.rename(columns={0:'Departamento',1:'Municipio',2:"Código",3:'Usuario',4:'Contraseña'})
tabla.to_csv('Passwords.csv',index=False)

for docs in IPS_data.find({"NIT":"890906347"}):
    pprint.pprint(docs)
    print('--------------------------------')
    
for docs in Users_data.find({"usuario":"800155000"}):
    pprint.pprint(docs)
    print('--------------------------------')

#for doc in documents:
#    try:
#        # insert into new collection
#    except pymongo.errors.DuplicateKeyError:
#        # skip document because it already exists in new collection
#        continue

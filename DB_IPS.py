#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  12 14:44:02 2017

@author: gita
"""

from flask import Flask, render_template, flash, request,session, redirect,url_for
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
##db.IPS_collection.drop()

#Obtener lista de departamento y ciudades
#info_IPS = pd.read_csv(main_path+'/static/listaDB.csv')
info_IPS = pd.read_csv(main_path+'/static/BD_IPS.csv',sep=';')
#Obtener departamentos
df = pd.DataFrame(info_IPS)
#Reemplazar datos faltantes
df = df.replace(np.nan,'')
passw = []
for idx_ips in range(0,df.shape[0]):
    ips = df.iloc[[idx_ips]]
    dpto = list(ips['Departamento'])[0]
    city = list(ips['Municipio'])[0]
    codhab = str(list(ips['Código habilitacion'])[0])
    nombreIPS = list(ips['Nombre prestador'])[0]#Nombre del prestador de servicios
    nit = str(list(ips['NIT'])[0])
    razsoc = list(ips['Razón social'])[0]
    clprcod = list(ips['clpr codigo'])[0]#codigo clase de prestador
    clprnam = list(ips['clpr nombre'])[0]#clase de prestador
    ese = list(ips['ese'])[0]
    addr = list(ips['Direccion'])[0] 
    tel = str(list(ips['telefono'])[0])
    tel = tel.replace('\n',' ')     
    fax = str(list(ips['fax'])[0])
    fax = fax.replace('\n',' ')   
    email = list(ips['email'])[0]#email del prestador de servicios   
    email = email.replace('\n',' ')    
    email = email.replace(';','')   
    ger = list(ips['gerente'])[0]  
    niv = list(ips['nivel'])[0]#Nivel del prestador de servicios 
    car = list(ips['caracter'])[0]
    fech_rad = str(list(ips['fecha radicacion'])[0])
    fech_ven = str(list(ips['fecha vencimiento'])[0])
    dv = str(list(ips['dv'])[0])#Ultimo numero en el nit
    clasepr = list(ips['clase persona'])[0]
    naju = list(ips['naju nombre'])[0]
    numsedpri = str(list(ips['numero sede principal'])[0])
    fech_corte = list(ips['fecha corte REPS'])[0]#fecha corte REPS
#    hab = list(ips['habilitada'])[0]
#    email = email.split(' ')
#    usr = list(ips['Encargado'])[0]
#    usrmail = list(ips['Email Encargado'])[0]
#    usrjob = list(ips['Cargo Encargado'])[0]
    
    
    #Ingreso de usuario para login
    #IPS_data.update({"NIT":nit}, {'$push':{'Usuarios':{"Usuario":nit, "password":hash_pass(userpass)}}}, upsert=False)
    temppass = nit[-4:]
    userpass = pass_generator()#car[1]+temppass[3]+temppass[0]+car[-1:]+temppass[1]+temppass[2]+car[len(car)-2]+car[0]
    dfpass = pd.DataFrame(np.reshape([dpto,city,nit,userpass],(1,4)))
    passw.append(dfpass)
    hpassw,salt = hash_pass(userpass)
    
    IPS_index_data = {"Departamento":dpto,
                  "Municipio":city,
                  "Nombre del Prestador":nombreIPS,
                  "Gerente":ger,
                  "NIT":nit,
                  "Código Habilitación":codhab,
                  "Fecha de Radicación":fech_rad,
                  "Fecha de Vencimiento":fech_ven,
                  "Carácter Territorial":car,
                  "Razón Social":razsoc,
                  "Clase de Prestador":clprnam,
                  "Empresa Social del Estado":ese,
                  "Nivel del Prestador":niv,
                  "Naturaleza Jurídica":naju,
                  "Teléfono":tel,
                  "Fax":fax,
                  "Email del Prestador":email,
                  "Dirección":addr,
                  "Encargado de Encuesta":'',
                  "Email del Encargado":'',
                  "Cargo del Encargado":'',
                  "Resultados Modulo 1":{},
                  "Resultados Modulo 2":{},
                  "Resultados Modulo 3":{},
                  "Resultados Modulo 4":{},
                  "Resultados Modulo 5":{},
                  "Resultados Modulo 6":{},
                  }

    Users_IPS = {usertag:nit, "password":hpassw,"salt":salt,"IPS_NIT":nit,'level':'sup'}
    
    #Llenar base de datos
    IPS_data.insert_one(IPS_index_data).inserted_id  
    Users_data.insert_one(Users_IPS).inserted_id  

tabla = pd.concat(passw)
tabla = tabla.rename(columns={0:'Departamento',1:'Municipio',2:'Usuario',3:'Contraseña'})
tabla.to_csv('Passwords.csv',index=False)

for docs in IPS_data.find({"Departamento":"Antioquia","Municipio": "YOLOMBÓ"}):
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

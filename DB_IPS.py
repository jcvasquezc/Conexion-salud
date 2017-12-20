#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  12 14:44:02 2017

@author: gita
"""

from flask import Flask, render_template, flash, request,session, redirect,url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from pymongo import MongoClient #Manejos de base de datos
import pymongo
import pandas as pd
import numpy as np
import os
import json
import pprint
from random import randint
import hashlib

#Codificar contrasenna Jason Vanzin
def hash_pass(password):
    hash_password = hashlib.sha1(password.encode('utf-8')).digest()
    hash_password = hashlib.sha1(hash_password).hexdigest()
    hash_password = '*' + hash_password.upper()
    return hash_password

#Directorio de proyecto
main_path = os.path.dirname(os.path.abspath(__file__))

##Crear Base de datos
##Crear cliente
client = MongoClient()
#
##Crear database
db = client.IPS_database
#client.drop_database('IPS_database')

##Crear colección
IPS_data  = db.IPS_collection
##Delete collection
##db.IPS_collection.drop()

#Obtener lista de departamento y ciudades
info_IPS = pd.read_csv(main_path+'/static/listaDB.csv')
#Obtener departamentos
df = pd.DataFrame(info_IPS)
#Reemplazar datos faltantes
df = df.replace(np.nan,'')
passw = []
for idx_ips in range(0,df.shape[0]):
    ips = df.iloc[[idx_ips]]
    dpto = list(ips['Departamento'])[0]
    city = list(ips['Municipio'])[0]
    name = list(ips['IPS'])[0]
    nit = str(list(ips['NIT'])[0])
    car = list(ips['Caracter'])[0]
    ger = list(ips['Gerente'])[0]
    addr = list(ips['Direccion'])[0]    
    email = list(ips['Email'])[0]
    tel = str(list(ips['Telefono'])[0])
    tel = tel.replace('\n',' ')        
    email = email.replace('\n',' ')    
    email = email.replace(';','')
#    email = email.split(' ')
    usr = list(ips['Encargado'])[0]
    usrmail = list(ips['Email Encargado'])[0]
    usrjob = list(ips['Cargo Encargado'])[0]
    
    #Ingreso de usuario para login
    IPS_data.update({"NIT":nit}, {'$push':{'Usuarios':{"Usuario":nit, "password":hash_pass(userpass)}}}, upsert=False)
    temppass = nit[-4:]
    userpass = car[1]+temppass[3]+temppass[0]+car[-1:]+temppass[1]+temppass[2]+car[len(car)-2]+car[0]
    dfpass = pd.DataFrame(np.reshape([dpto,city,nit,userpass],(1,4)))
    passw.append(dfpass)
    IPS_index_data = {"IPS":name,
                  "Gerente":ger,
                  "NIT":nit,
                  "Carácter":car,
                  "Teléfono":tel,
                  "Email":email,
                  "Dirección":addr,
                  "Encargado":usr,
                  "Email Encargado":usrmail,
                  "Cargo Encargado":usrjob,                  
                  "Departamento":dpto,
                  "Municipio":city,
                  "Usuarios":[{"usuario":nit, "password":hash_pass(userpass)}]}


    IPS_data.insert_one(IPS_index_data).inserted_id  

tabla = pd.concat(passw)
tabla = tabla.rename(columns={0:'Departamento',1:'Municipio',2:'Usuario',3:'Contraseña'})
tabla.to_csv('Passwords.csv',index=False)

for docs in IPS_data.find({"Departamento":"Antioquia","Municipio": "YOLOMBÓ"}):
    pprint.pprint(docs)
    print('--------------------------------')
    
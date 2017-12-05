#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:44:02 2017

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


#Directorio de proyecto
main_path = os.path.dirname(os.path.abspath(__file__))

##Crear Base de datos
##Crear cliente
client = MongoClient()
#
##Crear database
db = client.IPS_DEMODB

##Crear colección
IPS_data  = db.IPS_Demo_collection

##Delete collection
##db.IPS_Demo_collection.drop()

#Obtener lista de departamento y ciudades
info_IPS = pd.read_csv(main_path+'/demo/listaDB.csv')
#Obtener departamentos
df = pd.DataFrame(info_IPS)

for idx_ips in range(0,df.shape[0]):
    ips = df.iloc[[idx_ips]]
    dpto = list(ips['Departamento'])[0]
    city = list(ips['Municipio'])[0]
    name = list(ips['IPS'])[0]
    nit = list(ips['NIT'])[0]
    car = list(ips['Caracter'])[0]
    ger = list(ips['Gerente'])[0]
    hab_opt = list(ips['Habilitada'])[0]
    niv_opt = list(ips['Nivel'])[0]
    addr = list(ips['Direccion'])[0]
    tel = list(ips['Telefono'])[0]
    email = list(ips['Email'])[0]
    usrname = ['Gerente'+str(idx_ips)][0]
    usrid = 1127710000+idx_ips
    usrjob = 'Gerente'

    IPS_index_data = {"Nombre IPS":name,
                  "NIT":str(nit),
                  "Caracter":car,
                  "Nombre del gerente":ger,
                  "Nivel de IPS":str(niv_opt),
                  "Habilitada":hab_opt,                      
                  "Departamento":dpto,
                  "Ciudad":city,
                  "Dirección":addr,
                  "Telefono":str(tel),
                  "e-mail":email,
                  "Nombre del responsable":usrname,
                  "ID del responsable":str(usrid),
                  "Cargo del responsable":usrjob}

    IPS_data.insert_one(IPS_index_data).inserted_id  

for docs in IPS_data.find({"Departamento": "Amazonas"}):
    pprint.pprint(docs)
    print('--------------------------------')
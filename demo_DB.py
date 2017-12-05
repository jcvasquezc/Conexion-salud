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
#client = MongoClient()
#
##Crear database
#db = client.IPS_DEMODB

##Crear colección
#IPS_data  = db.Index_collection

##Delete collection
##db.Index_collection.drop()

#Obtener lista de departamento y ciudades
info_IPS = pd.read_csv(main_path+'/demo/listaDB.csv')
#Obtener departamentos
IPS = pd.DataFrame(info_IPS)

IPS_index_data = {"Nombre IPS":name,
              "NIT":nit,
              "Caracter":car,
              "Nombre del gerente":ger,
              "Nivel de IPS":niv_opt,
              "Habilitada":hab_opt,                      
              "Departamento":dpto,
              "Ciudad":city,
              "Dirección":addr,
              "Telefono":tel,
              "e-mail":email,
              "Nombre del responsable":usrname,
              "ID del responsable":usrid,
              "Cargo del responsable":usrjob}

IPS_data.insert_one(IPS_index_data).inserted_id  
#dptos = list(np.unique(lista_dptos['Departamento']))
##Crear diccionario de ciudades
#cities = {}
#for idx in dptos:
#    cities[idx] = list(np.unique(df[df['Departamento']==idx]['Municipio']))

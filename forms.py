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
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from werkzeug.utils import secure_filename

#Directorio de proyecto
main_path = os.path.dirname(os.path.abspath(__file__))

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
#Carpeta para adjuntar archivos
UPLOAD_FOLDER = main_path+'/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Crear Base de datos
#Crear cliente
client = MongoClient()

#Crear database
db = client.IPS_database
#client.drop_database('IPS_database')

#Crear colección
IPS_data  = db.IPS_collection

##Delete collection
#db.Index_collection.drop()

#Crear indice basado en NIT
#db.Index_collection.create_index([('NIT', pymongo.ASCENDING)],unique=True)

class ReusableForm(Form):
    name = TextField('Nombre:', validators=[validators.required()])
    dpto = TextField('Departamento:', validators=[validators.required()])
    city = TextField('Ciudad:', validators=[validators.required()])
    addr = TextField('Dirección:', validators=[validators.required()])
    tel = IntegerField('Teléfono:', validators=[validators.required(), validators.NumberRange(min=0000, max=9999999999, message="Por favor introduzca un teléfono valido")])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35, message="Por favor introduzca un email valido")])

#Extensiones permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    #Obtener lista de departamento y ciudades
    lista_dptos = pd.read_csv(main_path+'/static/pos_col.csv')
    #Obtener departamentos
    df = pd.DataFrame(lista_dptos)
    del  df['lat']
    del  df['lon']
    del  df['ID']
    del  df['ID2']
    df = df.dropna()
    dptos = list(np.unique(df['Departamento']))
    #Crear diccionario de ciudades
    cities = {}
    for idx in dptos:
        cities[idx] = list(np.unique(df[df['Departamento']==idx]['Municipio']))

    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('index.html', **{"dptos":dptos},cities=json.dumps(cities))

######################################################
@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        dpto = request.form['reg_dpto']
        city = request.form['reg_city']

        IPS = []
        dict_IPS = {}
        for docs in IPS_data.find({"Departamento":dpto,"Municipio":city}):
            IPS.append(docs['IPS'])
            templist = []
            for key, value in docs.items():
                if key not in ['IPS','_id']:
                    templist.append(value)
            dict_IPS[docs['IPS']] = templist
#        return redirect(url_for('registro'))
    return render_template('registro.html',**{"dpto":dpto,"city":city,"IPS":IPS},dict_IPS=json.dumps(dict_IPS))

######################################################
@app.route("/loginIPS", methods=['GET', 'POST'])
def loginIPS():
#    if request.method == 'POST':
    return render_template('loginIPS.html')

#######################ENCUESTA#######################
@app.route("/preguntas", methods=['GET', 'POST'])
def preguntas():
    if request.method == 'POST':
        #Datos IPS
        name = request.form['reg_ips']
        nit = request.form['nit']
        car = request.form['car']
        ger = request.form['ger']
        niv_opt = request.form['nivel']
        dpto = request.form['dpto']
        city = request.form['city']
        addr = request.form['addr']
        tel = request.form['tel']
        email = request.form['email']
        username = request.form['username']
        usermail = request.form['usermail']
        userjob = request.form['userjob']

        IPS_index_data = {"IPS":name,
                      "NIT":nit,
                      "Carácter":car,
                      "Gerente":ger,
                      "Nivel":niv_opt,
                      "Departamento":dpto,
                      "Municipio":city,
                      "Dirección":addr,
                      "Teléfono":tel,
                      "e-mail":email,
                      "Encargado":username,
                      "Email encargado":usermail,
                      "Cargo encargado":userjob}

        temp = IPS_data.find({"NIT":nit}).count()
        if temp!=0:
            IPS_data.update_one({"NIT":nit},{"$set":IPS_index_data})
        else:
            IPS_data.insert_one(IPS_index_data).inserted_id
#        return redirect(url_for('preguntas'))

    return render_template('preguntas.html')

#######################ENCUESTA#######################
@app.route("/analisis", methods=['GET', 'POST'])
def analisis():
    if request.method == 'POST':
        for idx in range(1,9):
            #Verificacion de archivos adjuntos
            if 'file_p'+str(idx) not in request.files:
                flash('No file part')
#                return redirect(request.url)
            file = request.files['file_p'+str(idx)]
            #En caso de no adjuntar datos
            if file.filename == '':
                flash('No selected file')
#                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                return redirect(url_for('analisis',filename=filename))

        print('Pregunta 4 opcion '+str(request.form.getlist('question4')))
        return redirect(url_for('analisis'))
    return render_template('analisis.html')


@app.route("/preguntas_mod1", methods=['GET', 'POST'])
def preguntas_mod1():
    return render_template('preguntas_mod1.html')

@app.route("/preguntas_mod2", methods=['GET', 'POST'])
def preguntas_mod2():
    return render_template('preguntas_mod2.html')


if __name__ == "__main__":
    app.run()

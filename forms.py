# pythonspot.com
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

##Delete collection
#db.Index_collection.drop()

#Crear colección
IPS_data  = db.Index_collection

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
#    form = ReusableForm(request.form)

    #Obtener lista de IPS    
    lista_IPS = pd.read_csv(main_path+'/static/listaDB.csv')
    tablaIPS = pd.DataFrame(lista_IPS)
    IPS_dpto = list(np.unique(tablaIPS['Departamento']))
    
    #Obtener lista de departamento y ciudades
    lista_dptos = pd.read_csv(main_path+'/static/pos_col.csv')
    #Obtener departamentos
    df = pd.DataFrame(lista_dptos)
    dptos = list(np.unique(lista_dptos['Departamento']))
    #Crear diccionario de ciudades
    cities = {}
    for idx in dptos:
        cities[idx] = list(np.unique(df[df['Departamento']==idx]['Municipio']))
        
        
    if request.method == 'POST':
        return redirect(url_for('index'))
    
    return render_template('index.html', **{"dptos":dptos},cities=json.dumps(cities))
    
#######################ENCUESTA#######################
@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        #Datos IPS
        name = request.form['name']
        nit = request.form['nit']
        car = request.form['car']
        ger = request.form['ger']
        niv_opt = request.form['nivel']
        dpto = request.form['dpto']
        city = request.form['city']
        addr = request.form['addr']
        tel = request.form['tel']
        email = request.form['email']
        
        IPS_index_data = {"IPS":name,
                      "NIT":nit,
                      "Carácter":car,
                      "Gerente":ger,
                      "Nivel":niv_opt,
                      "Departamento":dpto,
                      "Municipio":city,
                      "Dirección":addr,
                      "Teléfono":tel,
                      "e-mail":email}

        IPS_data.insert_one(IPS_index_data).inserted_id
        for docs in IPS_data.find():
            pprint.pprint(docs)
            print('--------------------------------')
        return redirect(url_for('registro'))
    
    return render_template('registro.html')
#######################ENCUESTA#######################
@app.route("/preguntas", methods=['GET', 'POST'])
def preguntas():
    if request.method == 'POST':
        return redirect(url_for('preguntas'))
    
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

if __name__ == "__main__":
    app.run()

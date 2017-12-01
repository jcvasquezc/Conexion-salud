# pythonspot.com
from flask import Flask, render_template, flash, request,session, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from pymongo import MongoClient #Manejos de base de datos
import pymongo
import pandas as pd
import numpy as np
import os
import json
import pprint

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


#Crear Base de datos
#Crear cliente
client = MongoClient()

#Crear database
db = client.IPS_database

#Delete collection
#db.Index_collection.delete_many({})

#Crear colección
IPS_data  = db.Index_collection

#Crear indice basado en NIT
db.Index_collection.create_index([('NIT', pymongo.ASCENDING)],unique=True)

class ReusableForm(Form):
    name = TextField('Nombre:', validators=[validators.required()])
    dpto = TextField('Departamento:', validators=[validators.required()])
    city = TextField('Ciudad:', validators=[validators.required()])
    addr = TextField('Dirección:', validators=[validators.required()])
    tel = IntegerField('Teléfono:', validators=[validators.required(), validators.NumberRange(min=0000, max=9999999999, message="Por favor introduzca un teléfono valido")])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35, message="Por favor introduzca un email valido")])


@app.route("/", methods=['GET', 'POST'])
def datos_ips():
    
    form = ReusableForm(request.form)

    #Directorio de proyecto
    main_path = os.path.dirname(os.path.abspath(__file__))

    #Obtener lista de departamento y ciudades
    lista_dptos = pd.read_csv(main_path+'/static/lista_dptos.csv')
    #Obtener departamentos
    df = pd.DataFrame(lista_dptos)
    dptos = list(np.unique(lista_dptos['Departamento']))
    #Crear diccionario de ciudades
    cities = {}
    for idx in dptos:
        cities[idx] = list(np.unique(df[df['Departamento']==idx]['Municipio']))

    if request.method == 'POST':
        #Datos IPS
        name = request.form['name']
        nit = request.form['nit']
        car = request.form['car']
        ger = request.form['ger']
        niv_opt = request.form['nivel']
        hab_opt = request.form['habil']
        dpto = request.form['dpto']
        city = request.form['city']        
        addr = request.form['addr']
        tel = request.form['tel']
        email = request.form['email']
        
        #Datos de quien llena la encuesta
        usrname = request.form['username']
        usrid = request.form['userid']
        usrjob = request.form['userjob']
        
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
        
        if form.validate():
            # Save the comment here.
            flash('Gracias por registrarse ' + name)
                        #Insertar nueva IPS
            IPS_data.insert_one(IPS_index_data).inserted_id
            
            print (name, " ", dpto, " ", city, " ",car , " ",niv_opt, " ", addr, " ", tel, " ", email)
            print(db.collection_names(include_system_collections=False))
            for docs in IPS_data.find():
                pprint.pprint(docs)
                print('--------------------------------')
        else:
            flash('Error: Todos los campos son requeridos. ')

    return render_template('index.html', **{"dptos":dptos},cities=json.dumps(cities))

#######################BASE DE DATOS#######################



@app.route("/preguntas", methods=['GET', 'POST'])
def preguntas():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('preguntas.html', form=form)


if __name__ == "__main__":
    app.run()

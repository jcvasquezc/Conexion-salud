#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  12 14:44:02 2017

@author: gita
"""

from flask import Flask, render_template, flash, request, redirect,url_for, make_response, abort
from flask_login import LoginManager, login_required, login_user,logout_user,UserMixin, current_user
from pymongo import MongoClient #Manejos de base de datos
import pandas as pd
import numpy as np
import os
import json
from werkzeug.utils import secure_filename
import hashlib
from utils import send_email
from urllib.parse import urlparse, urljoin

#Directorio de proyecto
main_path = os.path.dirname(os.path.abspath(__file__))

# App config.
DEBUG = True
#LOGIN_DISABLED = True #Solo habilitar para pruebas.
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
#Carpeta para adjuntar archivos
UPLOAD_FOLDER = main_path+'/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Manejo de usuarios
login_manager = LoginManager()
login_manager.init_app(app)#Configurar app para login
login_manager.login_view = "Ingresar" #ir a esta html cuando se requiera el login


#Base de datos
#Crear cliente
client = MongoClient()

#Crear database
db = client.IPS_database
#client.drop_database('IPS_database')

#Crear colección
IPS_data  = db.IPS_collection
Users_data = db.Users_collection


##Delete collection
#db.Index_collection.drop()

#Crear indice basado en NIT
#db.Index_collection.create_index([('NIT', pymongo.ASCENDING)],unique=True)

#######################################################
#######################################################
#######################################################
#Usuario para login
class User(UserMixin):    
    def __init__(self,usr_id):
        self.id = usr_id

    def __repr__(self):
        return '<User {}>'.format(self.usr_id)

#Cargar usuarios
users=[]
for docs in Users_data.find():
    usr_id=docs["user_id"]
    users.append(User(usr_id))

@login_manager.user_loader
def load_user(usr_id):
    return User(usr_id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
#######################################################
#######################################################
#######################################################
#safe redirect
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
        
def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)
#######################################################
#######################################################
#######################################################
    
#Obtener listas de departamentos y ciudades
def set_dptos():
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
    return dptos,cities


#Extensiones permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#def new_user(nit):
#    # Creates a new user for the company passed into the function if it doesn't already exist. se
#    import hashlib
#    user_data = {}
#    user_data['username'] =  input("Please enter your desired username: ").lower()
#    while user_exists(company.upper(), user_data['username']):
#        user_data['username'] = input("Username already exist. Please try a different username: ").lower()
#    password = input("Please enter a password: ")
#    user_data['password'] = hash_pass(password)
#    user_data['email'] = input("Please enter your email address: ")
#    update_result = update_mongo_document(company.upper(), 'user', '$push', user_data)
#    
####################################
#Codificar contrasenna
def hash_pass(password,salt):
    salt_hash = hashlib.blake2b(salt=salt)
    salt_hash.update(password.encode('utf-8'))
    hash_password = salt_hash.digest()
    return hash_password
########################################################
#Verificar credenciales
def get_credentials(usr,userpass):    
    temp = Users_data.find({"usuario":usr}).count()
    print(temp)
    if temp == 0:
        return False
    else:
        results = Users_data.find({"usuario":usr})[0]
        if hash_pass(userpass,results['salt']) == results['password']:
            return True
        return False
######################################################
@app.route("/", methods=['GET', 'POST'])
def index():
#    dptos,cities = set_dptos()
    if request.method == 'POST':
        return redirect(url_for('index'))
#    return render_template('index.html', **{"dptos":dptos},cities=json.dumps(cities))
    return render_template('index.html')
###################################################3##
@app.route("/Ingresar", methods=['GET', 'POST'])
def Ingresar():    
    next = get_redirect_target()
    if request.method == 'POST':
        username = request.form['usrlog']
        userpass = request.form['passlog']
        credentials = get_credentials(username,userpass)
        error = ''
        #Verificarcontrasennas
        if credentials:
            user_id = Users_data.find({"usuario":username})[0]['user_id']
            user = User(user_id)
            login_user(user)        
#            if not is_safe_url(next):
#                return abort(400)

            return redirect(next or url_for('index'))
#            return render_template('modulos.html')
        else:
            error = ' (Usuario o Contraseña incorrecto)'
            return render_template('Ingresar.html',error=error)
    return render_template('Ingresar.html',next=next)

######################################################
@app.route("/registro", methods=['GET', 'POST'])
@login_required
def registro():
    dptos,cities = set_dptos()
    if request.method == 'POST':        
        #Datos prestador
        nombreIPS = request.form['reg_ips']#Nombre del prestador
        nit = request.form['reg_nit']#Nit del prestador
        Nsed = request.form['reg_numsede']#Numero de sedes
        naju = request.form['reg_natjur']#Naturaleza juridica
        clpr = request.form['reg_clase']#Clase de prestador
        niv = request.form['reg_nivel']#Nivel del prestador
        dptoP = request.form['reg_dptoP']#Departamento del prestador
        cityP = request.form['reg_cityP']#Municipio del prestador
        userenc = request.form['reg_manag']#nombre del encargado
        mailenc = request.form['reg_manmail']#email del encargado
        jobenc = request.form['reg_manjob']#cargo del encargado
        
        IPS_reg_data = {
                  "Clase de Prestador":clpr,
                  "Cargo del Encargado":jobenc,
                  "Departamento":dptoP,
                  "Encargado de Encuesta":userenc,
                  "Email del Encargado":mailenc,
                  "Municipio":cityP,
                  "Nivel del Prestador":niv,
                  "Naturaleza Jurídica":naju,
                  "Nombre del Prestador":nombreIPS,
                  "NIT":nit,
                  "Número de sedes":Nsed,
                  }       
        
        temp = IPS_data.find({"NIT":nit}).count()
        if temp!=0:
            IPS_data.update_one({"NIT":nit},{"$set":IPS_reg_data})
        else:
            IPS_data.insert_one(IPS_reg_data).inserted_id
        
        return redirect(url_for('modulos'))

    return render_template('registro.html',**{"dptos":dptos},cities=json.dumps(cities))
######################################################
@app.route("/modulos", methods=['GET', 'POST'])
@login_required
def modulos():
    dptos,cities = set_dptos()
    #Verificar si es necesario registrar
    usr_id = int(current_user.id)
    print(usr_id)
    nit = Users_data.find({"user_id":usr_id})[0]['IPS_NIT']
    IPSdata = IPS_data.find({"NIT":nit})[0]
    if len(IPSdata['Encargado de Encuesta'])==0:
        dptos,cities = set_dptos()                
        IPSdata.pop('_id', None)
        return render_template('registro.html',**{"dptos":dptos},cities=json.dumps(cities),IPSdata=json.dumps(dict(IPSdata)))
    if request.method == 'POST': 
        print(request.form)       
        print("############ doing post")
        name1 = request.form['nombre1']
        email1= request.form['email1']
        cargo1= request.form['cargo1']
        print(name1, email1, cargo1)
        name2 = request.form['nombre2']
        email2= request.form['email2']
        cargo2= request.form['cargo2']
        name3 = request.form['nombre3']
        email3= request.form['email3']
        cargo3= request.form['cargo3']
        name4 = request.form['nombre4']
        email4= request.form['email4']
        cargo4= request.form['cargo4']
        name5 = request.form['nombre5']
        email5= request.form['email5']
        cargo5= request.form['cargo5']
        name6 = request.form['nombre6']
        email6= request.form['email6']
        cargo6= request.form['cargo6']

        

        usr_id = current_user.id
        print(usr_id)
        print(Users_data.find()[0])
        usr =   Users_data.find({'user_id': int(usr_id)})[0]


        temp = IPS_data.find({"NIT":usr['IPS_NIT']})
        Ntemp=temp.count()
        if Ntemp!=0:



            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador1 nombre": name1}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador2 nombre": name2}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador3 nombre": name3}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador4 nombre": name4}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador5 nombre": name5}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador6 nombre": name6}}, upsert=False, full_response= True)

            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador1 cargo": cargo1}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador2 cargo": cargo2}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador3 cargo": cargo3}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador4 cargo": cargo4}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador5 cargo": cargo5}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador6 cargo": cargo6}}, upsert=False, full_response= True)


            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador1 email": email1}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador2 email": email2}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador3 email": email3}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador4 email": email4}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador5 email": email5}}, upsert=False, full_response= True)
            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"colaborador6 email": email6}}, upsert=False, full_response= True)



        return render_template('modulos.html')

    return render_template('modulos.html')

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
@login_required
def preguntas_mod1():
    global usr
    if request.method == 'POST':
        """
        name_gerente = request.form['gerente']
        email_gerente= request.form['email1']
        nombre_mod2 = request.form['nombre_mod2']
        email_2= request.form['email2']
        nombre_mod3 = request.form['nombre_mod3']
        email_3= request.form['email3']
        nombre_mod4 = request.form['nombre_mod4']
        email_4= request.form['email4']
        nombre_mod5 = request.form['nombre_mod5']
        email_5= request.form['email5']
        nombre_mod6 = request.form['nombre_mod6']
        email_6= request.form['email6']

        nombre_mod7=[request.form['nombre_mod7_'+str(i)] for i in range(1,5)]
        email_7=[request.form['email7_'+str(i)] for i in range(1,5)]

        nombres=np.hstack((name_gerente, nombre_mod2, nombre_mod3, nombre_mod4, nombre_mod5, nombre_mod6, nombre_mod7))
        emails=np.hstack((email_gerente, email_2, email_3, email_4, email_5, email_6, email_7))
        key_pass=get_credentials(usr)
        for j in range(len(nombres)):
            if len(emails[j])>0:
                print(emails[j], nombres[j], usr, key_pass)
                send_email(emails[j], nombres[j], usr, key_pass)

        """
        # guarda automaticamente resultados de la encuesta cada cierto tiempo
        data_enc=[]
        print(request.form)
        dict_encuesta={}
        for j in request.form:
            if j.find("question")>=0:
                dict_encuesta[j]=request.form[j]
        print(dict_encuesta)
        usr_id = current_user.id
        print(usr_id)
        print(Users_data.find()[0])
        usr =   Users_data.find({'user_id': int(usr_id)})[0]

        temp = IPS_data.find({"NIT":usr['IPS_NIT']})
        Ntemp=temp.count()
        if Ntemp!=0:

            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"Resultados Modulo 2": dict_encuesta}}, upsert=False, full_response= True)
        

    return render_template('preguntas_mod1.html')

@app.route("/preguntas_mod2", methods=['GET', 'POST'])
@login_required
def preguntas_mod2():
    if request.method == 'POST':
        data_enc=[]
        print(request.form)
        dict_encuesta={}
        for j in request.form:
            if j.find("question")>=0:
                dict_encuesta[j]=request.form[j]
        print(dict_encuesta)
        usr_id = current_user.id
        print(usr_id)
        print(Users_data.find()[0])
        usr =   Users_data.find({'user_id': int(usr_id)})[0]
        temp = IPS_data.find({"NIT":usr['IPS_NIT']})
        Ntemp=temp.count()
        if Ntemp!=0:

            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"Resultados Modulo 2": dict_encuesta}}, upsert=False, full_response= True)
        

    return render_template('preguntas_mod2.html')

@app.route("/preguntas_mod3", methods=['GET', 'POST'])
@login_required
def preguntas_mod3():
    if request.method == 'POST':
        data_enc=[]
        print(request.form)
        dict_encuesta={}
        for j in request.form:
            if j.find("question")>=0:
                dict_encuesta[j]=request.form[j]
        print(dict_encuesta)
        usr_id = current_user.id
        print(usr_id)
        print(Users_data.find()[0])
        usr =   Users_data.find({'user_id': int(usr_id)})[0]
        temp = IPS_data.find({"NIT":usr['IPS_NIT']})
        Ntemp=temp.count()
        if Ntemp!=0:

            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"Resultados Modulo 3": dict_encuesta}}, upsert=False, full_response= True)
        

    return render_template('preguntas_mod3.html')

@app.route("/preguntas_mod4", methods=['GET', 'POST'])
@login_required
def preguntas_mod4():

    if request.method == 'POST':
        data_enc=[]
        print(request.form)
        dict_encuesta={}
        for j in request.form:
            if j.find("question")>=0:
                dict_encuesta[j]=request.form[j]
        print(dict_encuesta)
        usr_id = current_user.id
        print(usr_id)
        print(Users_data.find()[0])
        usr =   Users_data.find({'user_id': int(usr_id)})[0]
        temp = IPS_data.find({"NIT":usr['IPS_NIT']})
        Ntemp=temp.count()
        if Ntemp!=0:

            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"Resultados Modulo 4": dict_encuesta}}, upsert=False, full_response= True)
        
    return render_template('preguntas_mod4.html')

@app.route("/preguntas_mod5", methods=['GET', 'POST'])
@login_required
def preguntas_mod5():
    if request.method == 'POST':
        data_enc=[]
        print(request.form)
        dict_encuesta={}
        for j in request.form:
            if j.find("question")>=0:
                dict_encuesta[j]=request.form[j]
        print(dict_encuesta)
        usr_id = current_user.id
        print(usr_id)
        print(Users_data.find()[0])
        usr =   Users_data.find({'user_id': int(usr_id)})[0]
        temp = IPS_data.find({"NIT":usr['IPS_NIT']})
        Ntemp=temp.count()
        if Ntemp!=0:

            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"Resultados Modulo 5": dict_encuesta}}, upsert=False, full_response= True)
        

    return render_template('preguntas_mod5.html')

@app.route("/preguntas_mod6", methods=['GET', 'POST'])
@login_required
def preguntas_mod6():
    nquestion=0
    if request.method == 'POST':
        form_mod6 = request.form
        nquestion=0
        data_enc=[]
        print(request.form)
        dict_encuesta={}
        for j in request.form:
            if j.find("question")>=0:
                dict_encuesta[j]=request.form[j]
            if len(request.form[j])>0:
                nquestion=nquestion+1

        print(dict_encuesta)
        usr_id = current_user.id
        print(usr_id)
        print(Users_data.find()[0])
        usr =   Users_data.find({'user_id': int(usr_id)})[0]
        print(usr)       

        temp = IPS_data.find({"NIT":usr['IPS_NIT']})
        Ntemp=temp.count()
        if Ntemp!=0:

            IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"Resultados Modulo 6": dict_encuesta}}, upsert=False, full_response= True)

    return render_template('preguntas_mod6.html', nquestion=nquestion)

@app.route("/validar<modulo>", methods=['GET', 'POST'])
@login_required
def validar(modulo):

    print(request.method)
    if request.method == 'POST':
        data_enc=[]
        print("MODULO: ", modulo)
        print(request.form)
        
        
        usr_id = current_user.id
        print(usr_id)
        
        print(Users_data.find()[0])
        usr =   Users_data.find({'user_id': int(usr_id)})[0]
        print(usr)       
        temp = IPS_data.find({"NIT":usr['IPS_NIT']})
        print(temp)
        Ntemp=temp.count()
        print(Ntemp)
        dict_encuesta={}
        print(usr['IPS_NIT'])
        dict_encuesta["NIT"]=usr['IPS_NIT']
        for j in request.form:
            if j.find("question")>=0:
                dict_encuesta[j]=request.form[j]
        print(dict_encuesta)

        IPS_data.find_and_modify(query={'NIT':usr['IPS_NIT']}, update={"$set": {"Resultados Modulo "+str(modulo): dict_encuesta}}, upsert=False, full_response= True)
       
        return render_template('validar.html', nit=usr['IPS_NIT'])
    return render_template('validar.html', nit=usr['IPS_NIT'])



@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():

    temp = IPS_data.find({"Encargado de Encuesta":{'$not': {'$size': 0}}})
    Nregistered=0
    Nmiss=0
    tab_reg=[]
    tab_miss=[]
    n_mod=np.zeros(6)
    for reg in temp:
        if len(reg["Encargado de Encuesta"])>0:
            print(reg["Encargado de Encuesta"])
            Nregistered=Nregistered+1
            tab_reg.append([reg["Departamento"],reg["Municipio"], reg["Nombre del Prestador"], reg["NIT"], "Aqui"])
        else:
            Nmiss=Nmiss+1
            tab_miss.append([reg["Departamento"],reg["Municipio"], reg["Nombre del Prestador"], reg["NIT"], "Aqui"])
        for k in np.arange(1,7):
            if len(reg["Resultados Modulo "+str(k)])>0:
                n_mod[k-1]=n_mod[k-1]+1
    
    n_mod=np.round(100*n_mod/(Nregistered+Nmiss),2)


    return render_template('admin.html', Nregistered=Nregistered, Nmiss=Nmiss, **{"tab_reg":tab_reg},**{"tab_miss":tab_miss}, n_mod=n_mod)



@app.route("/adminips_<ips_usr>", methods=['GET', 'POST'])
@login_required
def adminips_(ips_usr):
    print(ips_usr)

    usr =   IPS_data.find({"NIT":ips_usr})[0]
    general_info={'Código Habilitación':usr['Código Habilitación'],
                        'Código de sede':usr['Código de sede'],
                        'Carácter Territorial': usr['Carácter Territorial'],
                        'Clase de Prestador': usr['Clase de Prestador'],
                        'Municipio': usr['Municipio'],
                        'Departamento':usr['Departamento'],
                        'Nombre del Prestador':usr['Nombre del Prestador'],
                        'NIT': usr['NIT'],
                        'Dirección':usr['Dirección'],
                        'Teléfono':usr['Teléfono'],
                        'name1':usr['colaborador1 nombre'],
                        'name2':usr['colaborador2 nombre'],
                        'name3':usr['colaborador3 nombre'],
                        'name4':usr['colaborador4 nombre'],
                        'name5':usr['colaborador5 nombre'],
                        'name6':usr['colaborador6 nombre'],
                        'cargo1':usr['colaborador1 cargo'],
                        'cargo2':usr['colaborador2 cargo'],
                        'cargo3':usr['colaborador3 cargo'],
                        'cargo4':usr['colaborador4 cargo'],
                        'cargo5':usr['colaborador5 cargo'],
                        'cargo6':usr['colaborador6 cargo'],
                        'email1':usr['colaborador1 email'],
                        'email2':usr['colaborador2 email'],
                        'email3':usr['colaborador3 email'],
                        'email14':usr['colaborador4 email'],
                        'email5':usr['colaborador5 email'],
                        'email6':usr['colaborador6 email'],

    }
    Resultados_mod1=usr["Resultados Modulo 1"]
    Resultados_mod2=usr["Resultados Modulo 2"]
    Resultados_mod3=usr["Resultados Modulo 3"]
    Resultados_mod4=usr["Resultados Modulo 4"]
    Resultados_mod5=usr["Resultados Modulo 5"]
    Resultados_mod6=usr["Resultados Modulo 6"]

    print(Resultados_mod5)
    perc_mod=[int(100*(len(Resultados_mod1)-1)/7), int(100*(len(Resultados_mod2)-1)/31), int(100*(len(Resultados_mod3)-1)/29), int(100*(len(Resultados_mod4)-1)/3), int(100*(len(Resultados_mod5)-1)/4), int(100*(len(Resultados_mod6)-1)/3)]
    perc_mod=np.asarray(perc_mod)
    find0=np.asarray(np.where(np.asarray(perc_mod)<0)[0])
    print(find0)
    perc_mod[find0]=0
    print(Resultados_mod1)
    return render_template('adminips_.html', **{"general_info":general_info},**{"Resultados_mod1":Resultados_mod1},**{"Resultados_mod2":Resultados_mod2},**{"Resultados_mod3":Resultados_mod3},**{"Resultados_mod4":Resultados_mod4},**{"Resultados_mod5":Resultados_mod5},**{"Resultados_mod6":Resultados_mod6},perc_mod=perc_mod)






@app.route("/exportcsv<modulo>", methods=['GET', 'POST'])
@login_required
def exportcsv(modulo):
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()

    if request.method == 'POST': 
        temp = IPS_data.find({"Encargado de Encuesta":{'$not': {'$size': 0}}})
        
        row = -1
        df=pd.DataFrame([])
        for reg in temp:
            if len(reg["Resultados Modulo "+str(modulo)])>0:
                print(reg["Resultados Modulo "+str(modulo)])
                row = row + 1

                data=reg["Resultados Modulo "+str(modulo)]

                for key in data.keys():
                    df.loc[row,key] = data[key]
        print(df)
        csv_file=df.to_csv(sep='\t')


        resp = make_response(csv_file)
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    return render_template('admin.html')



if __name__ == "__main__":
    app.run()

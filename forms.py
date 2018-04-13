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
        cities[idx.upper()] = list(np.unique(df[df['Departamento']==idx]['Municipio']))

    #Set DEPARTAMENTOS to UPPERCASE
    idx = 0
    for d in dptos:
        dptos[idx]=d.upper()
        idx = idx+1        
    return dptos,cities
##############################################
##############################################
#Extensiones permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Validar Numeros
def val_num(x):
  try:
    return int(x)
  except ValueError:
    return False

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
#    print(temp)
    if temp == 0:
        return False
    else:
        results = Users_data.find({"usuario":usr})[0]
#        print(userpass)
#        print(results['password_nc'])
        if hash_pass(userpass,results['salt']) == results['password']:
            return True
        return False
######################################################
@app.route("/", methods=['GET', 'POST'])
def index():
    LogFlag = "False"
    if current_user.is_active==True:
        LogFlag = "True"
#    dptos,cities = set_dptos()
    if request.method == 'POST':
        return redirect(url_for('index'))
#    return render_template('index.html', **{"dptos":dptos},cities=json.dumps(cities))

    return render_template('index.html',LogFlag=json.dumps(LogFlag))

@app.route("/instructivo", methods=['GET', 'POST'])
def instructivo():
    LogFlag = "False"
    if current_user.is_active==True:
        LogFlag = "True"
#    dptos,cities = set_dptos()
    if request.method == 'POST':
        return redirect(url_for('instructivo'))
#    return render_template('index.html', **{"dptos":dptos},cities=json.dumps(cities))

    return render_template('instructivo.html',LogFlag=json.dumps(LogFlag))

@app.route("/faqs", methods=['GET', 'POST'])
def faqs():
    LogFlag = "False"
    if current_user.is_active==True:
        LogFlag = "True"
#    dptos,cities = set_dptos()
    if request.method == 'POST':
        return redirect(url_for('faqs'))
#    return render_template('index.html', **{"dptos":dptos},cities=json.dumps(cities))

    return render_template('faqs.html',LogFlag=json.dumps(LogFlag))

@app.route("/contacto", methods=['GET', 'POST'])
def contacto():
    LogFlag = "False"
    if current_user.is_active==True:
        LogFlag = "True"
#    dptos,cities = set_dptos()
    if request.method == 'POST':
        return redirect(url_for('contacto'))
#    return render_template('index.html', **{"dptos":dptos},cities=json.dumps(cities))

    return render_template('contacto.html',LogFlag=json.dumps(LogFlag))

###################################################3##
@app.route("/Ingresar", methods=['GET', 'POST'])
def Ingresar():    
#    next = get_redirect_target()
    LogFlag = "False"
    if request.method == 'POST':
        if current_user.is_active==True:
            LogFlag = "True"
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

            return redirect(url_for('index',LogFlag=json.dumps(LogFlag)))
#            return render_template('modulos.html')
        else:
            error = ' (Usuario o Contraseña incorrecto)'
            return render_template('Ingresar.html',error=error,LogFlag=json.dumps(LogFlag))
    return render_template('Ingresar.html',LogFlag=json.dumps(LogFlag))
#####################################################
@app.route("/redirec", methods=['GET', 'POST'])
def redirec():    
    next = get_redirect_target()
    LogFlag = "False"
    if request.method == 'POST':
        if current_user.is_active==True:
            LogFlag = "True"
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

            return redirect(next or url_for('index',LogFlag=json.dumps(LogFlag)))
#            return render_template('modulos.html')
        else:
            error = ' (Usuario o Contraseña incorrecto)'
            return render_template('Ingresar.html',error=error,LogFlag=json.dumps(LogFlag))
    return render_template('Ingresar.html',next=next,LogFlag=json.dumps(LogFlag))
######################################################
@app.route("/registro", methods=['GET', 'POST'])
@login_required
def registro():
    dptos,cities = set_dptos()   
    #Current User
    usr_id = int(current_user.id)
    usrid = Users_data.find({"user_id":usr_id})[0]
    
    #Select colab
    if (usrid['role']!='manager'):
        return redirect(url_for('index'))
    
    IPSdata = IPS_data.find({"ID":usrid['ID']})[0]
    IPSdata.pop('_id', None)#JSON CANT SERIALIZED ObjectID
    
    if request.method == 'POST': 
        #Datos prestador
        nombreIPS = request.form['reg_ips']#Nombre del prestador
        nit = request.form['reg_nit']#Nit del prestador
        Nsed = request.form['reg_numsede']#Numero de sedes
        codhab = request.form['reg_hab']#NCdigo habilitacion
        naju = request.form['reg_natjur']#Naturaleza juridica
        clpr = request.form['reg_clase']#Clase de prestador
        niv = request.form['reg_nivel']#Nivel del prestador
        dptoP = request.form['reg_dptoP']#Departamento del prestador
        cod_dpto = request.form['reg_coddpto']#Departamento del prestador
        cod_city = request.form['reg_codcity']#Municipio del prestador
        cityP = request.form['reg_cityP']#Municipio del prestador
        userenc = request.form['reg_manag']#nombre del encargado
        mailenc = request.form['reg_manmail']#email del encargado
        telenc = request.form['reg_mantel']#Telefono del encargado
        IPS_reg_data = {
                  "Código Habilitación":codhab,
                  "Validar INFO":True,
                  "Código Municipio":cod_city,
                  "Código Departamento":cod_dpto,
                  "Departamento":dptoP,
                  "Encargado de Encuesta":userenc,
                  "E-mail del Encargado":mailenc,
                  "Teléfono del Encargado":telenc,
                  "Municipio":cityP,
                  "Nivel del Prestador":niv,
                  "Naturaleza Jurídica":naju,
                  "Clase de Prestador":clpr,
                  "Nombre del Prestador":nombreIPS,
                  "NIT":nit,
                  "Número de sede":Nsed,
                  }       
        #print(IPS_reg_data)
        usr_id = int(current_user.id)
        ID = Users_data.find({"user_id":usr_id})[0]['user_id']
        temp = IPS_data.find({"ID":ID}).count()
        if temp!=0:
            IPS_data.update_one({"ID":ID},{"$set":IPS_reg_data})
        else:
            IPS_data.insert_one(IPS_reg_data).inserted_id
        
        return redirect(url_for('modulos'))

    return render_template('registro.html',**{"dptos":dptos},cities=json.dumps(cities),IPSdata=json.dumps(dict(IPSdata)))
######################################################
@app.route("/modulos", methods=['GET', 'POST'])
@login_required
def modulos():
    dptos,cities = set_dptos()
    #Verificar si es necesario registrar
    usr_id = int(current_user.id)   
    usrid = Users_data.find({"user_id":usr_id})[0] 
    #Select colab
    if (usrid['role']=='member1'):
        return redirect(url_for('preguntas_mod1'))
    if (usrid['role']=='member2'):
        return redirect(url_for('preguntas_mod2'))
    if (usrid['role']=='member3'):
        return redirect(url_for('preguntas_mod3'))
    if (usrid['role']=='member4'):
        return redirect(url_for('preguntas_mod4'))
    if (usrid['role']=='member5'):
        return redirect(url_for('preguntas_mod5'))
    if (usrid['role']=='member6'):
        return redirect(url_for('preguntas_mod6'))
    if (usrid['role']=='admin'):
        return redirect(url_for('admin')) 
    usrid = Users_data.find({"user_id":usr_id})[0] 
    IPSdata = IPS_data.find({"ID":usrid['user_id']})[0]
    if IPSdata['Validar INFO']==False:
        return redirect(url_for('registro'))
        
    if request.method == 'POST': 
        colabs = {}
        Ncolabs = 6 #Numero maximo de colaboradores
        for idx in range(1,Ncolabs+1):
            colabs['nombre'+str(idx)] = request.form['nombre'+str(idx)]
            colabs['email'+str(idx)] = request.form['email'+str(idx)]
            colabs['cargo'+str(idx)] = request.form['cargo'+str(idx)]        

        usr_id = current_user.id
        usr =   Users_data.find({'user_id': int(usr_id)})[0]
        temp = IPS_data.find({"ID":usr['user_id']})
        Ntemp=temp.count()
        if Ntemp!=0:
            for idx in range(1,Ncolabs+1):
                IPS_data.find_and_modify(query={'ID':usr['user_id']}, update={"$set": {'colaborador'+str(idx)+' nombre': colabs['nombre'+str(idx)]}}, upsert=False, full_response= True)
                IPS_data.find_and_modify(query={'ID':usr['user_id']}, update={"$set": {'colaborador'+str(idx)+' cargo': colabs['cargo'+str(idx)]}}, upsert=False, full_response= True)
                IPS_data.find_and_modify(query={'ID':usr['user_id']}, update={"$set": {'colaborador'+str(idx)+' email': colabs['email'+str(idx)]}}, upsert=False, full_response= True)

        return redirect(url_for('modulos',userid=IPS_data.find({"ID":usrid['ID']})[0]['ID'], message=["","","","","",""]))
#        return render_template('modulos.html',userid=IPS_data.find({"ID":usrid['ID']})[0]['ID'], message=["","","","","",""])
    
    return render_template('modulos.html',userid=IPS_data.find({"ID":usrid['ID']})[0]['ID'], message=["","","","","",""])


#######################ENCUESTA#######################
@app.route("/analisis", methods=['GET', 'POST'])
def analisis():
    if request.method == 'POST':
#        for idx in range(1,9):
#            #Verificacion de archivos adjuntos
#            if 'file_p'+str(idx) not in request.files:
#                flash('No file part')
##                return redirect(request.url)
#            file = request.files['file_p'+str(idx)]
#            #En caso de no adjuntar datos
#            if file.filename == '':
#                flash('No selected file')
##                return redirect(request.url)
#            if file and allowed_file(file.filename):
#                filename = secure_filename(file.filename)
#                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
##                return redirect(url_for('analisis',filename=filename))
#
#        #print('Pregunta 4 opcion '+str(request.form.getlist('question4')))
        return redirect(url_for('analisis'))
    return render_template('analisis.html')


@app.route("/preguntas_mod1", methods=['GET', 'POST'])
@login_required
def preguntas_mod1():
    global usr
    usr_id = current_user.id
    usr =   Users_data.find({'user_id': int(usr_id)})[0]
    temp = IPS_data.find({"ID":usr['ID']})  
    temp2=temp[0]     
    Rtas = temp2["Resultados Modulo 1"]
    if request.method == 'POST':
        return redirect(url_for('preguntas_mod1'))
    return render_template('preguntas_mod1.html',Rtas=json.dumps(dict(Rtas)))

@app.route("/preguntas_mod2", methods=['GET', 'POST'])
@login_required
def preguntas_mod2():
    usr_id = current_user.id
    usr =   Users_data.find({'user_id': int(usr_id)})[0]
    temp = IPS_data.find({"ID":usr['ID']})
    temp2=temp[0]     
    Rtas = temp2["Resultados Modulo 2"]
    if request.method == 'POST':
      return redirect(url_for('preguntas_mod2'))
    return render_template('preguntas_mod2.html',Rtas=json.dumps(dict(Rtas)))

@app.route("/preguntas_mod3", methods=['GET', 'POST'])
@login_required
def preguntas_mod3():
    usr_id = current_user.id
    usr =   Users_data.find({'user_id': int(usr_id)})[0]
    temp = IPS_data.find({"ID":usr['ID']})
    temp2=temp[0]     
    Rtas = temp2["Resultados Modulo 3"]
    
    if request.method == 'POST':
      return redirect(url_for('preguntas_mod3'))
    return render_template('preguntas_mod3.html',Rtas=json.dumps(dict(Rtas)))

@app.route("/preguntas_mod4", methods=['GET', 'POST'])
@login_required
def preguntas_mod4():
    usr_id = current_user.id
    usr =   Users_data.find({'user_id': int(usr_id)})[0]
    temp = IPS_data.find({"ID":usr['ID']})
    temp2=temp[0]     
    Rtas = temp2["Resultados Modulo 4"]
    if request.method == 'POST':
        return redirect(url_for('preguntas_mod4'))
    return render_template('preguntas_mod4.html',Rtas=json.dumps(dict(Rtas)))

@app.route("/preguntas_mod5", methods=['GET', 'POST'])
@login_required
def preguntas_mod5():
    usr_id = current_user.id
    usr =   Users_data.find({'user_id': int(usr_id)})[0]
    temp = IPS_data.find({"ID":usr['ID']})
    temp2=temp[0]     
    Rtas = temp2["Resultados Modulo 5"]
    if request.method == 'POST':
        return redirect(url_for('preguntas_mod5'))
    return render_template('preguntas_mod5.html',Rtas=json.dumps(dict(Rtas)))
################################################################
################################################################
@app.route("/preguntas_mod6", methods=['GET', 'POST'])
@login_required
def preguntas_mod6():
    usr_id = current_user.id
    usr =   Users_data.find({'user_id': int(usr_id)})[0]
    temp = IPS_data.find({"ID":usr['ID']})
    temp2 = temp[0]
    Rtas = temp2["Resultados Modulo 6"]
    nquestion=0
    if request.method == 'POST':
#        return render_template('preguntas_mod6.html', nquestion=nquestion,Rtas=json.dumps(dict(Rtas)))
        return redirect(url_for('preguntas_mod6'))

    return render_template('preguntas_mod6.html', nquestion=nquestion,Rtas=json.dumps(dict(Rtas)))

@app.route("/validar<modulo>", methods=['GET', 'POST'])
@login_required
def validar(modulo):
    if request.method == 'POST': 
        usr_id = current_user.id
        usr =   Users_data.find({'user_id': int(usr_id)})[0]
        temp = IPS_data.find({"ID":usr['ID']})
        Ntemp=temp.count()
        dict_encuesta={}
        dict_encuesta["ID"]=usr['ID']
        for j in request.form:
            if int(modulo)==1 and len(request.form[j])>0:
                IPS_data.find_and_modify(query={"ID":usr['ID']}, update={"$set": {"valmod1": True}}, upsert=False, full_response= True)
                dict_encuesta[j]=request.form.getlist(j)
                if len(dict_encuesta[j])==1:
                    dict_encuesta[j]=dict_encuesta[j][0]
                continue
            if j.find("question")>=0:
                dict_encuesta[j]=request.form.getlist(j)
                if len(dict_encuesta[j])==1:
                    dict_encuesta[j]=dict_encuesta[j][0]
        IPS_data.find_and_modify(query={"ID":usr['ID']}, update={"$set": {"Resultados Modulo "+str(modulo): dict_encuesta}}, upsert=False, full_response= True)
       
        return render_template('validar.html', nit=usr['Codigo'])
    return render_template('validar.html', nit=usr['Codigo'])

@app.route("/mensaje", methods=['GET', 'POST'])
@login_required
def mensaje():
    return render_template('mensaje.html')

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():    
    usr_id = int(current_user.id)   
    usrid = Users_data.find({"user_id":usr_id})[0] 
    #Select colab
    if (usrid['role']!='admin'):
        return redirect(url_for('index'))
    
    Nregistered=0
    Nmiss=0
    tab_reg=[]
    tab_miss=[]
    n_mod=np.zeros(6)
    #IPS registradas
    
    for docs in IPS_data.find():
        if docs["Validar INFO"]==True:#IPS REGISTRADAS
            Nregistered=Nregistered+1
            tab_reg.append([docs["Departamento"],docs["Municipio"], docs["Nombre del Prestador"], docs["ID"], "Aqui"])
        else:#IPS FALTANTES
            Nmiss = Nmiss+1
            tab_miss.append([docs["Departamento"],docs["Municipio"], docs["Nombre del Prestador"], docs["ID"], "Aqui"])

        for k in np.arange(1,7):
            if len(docs["Resultados Modulo "+str(k)])>0:
                n_mod[k-1]=n_mod[k-1]+1

    n_mod=np.round(100*n_mod/(Nregistered+Nmiss),2)
    return render_template('admin.html', Nregistered=Nregistered, Nmiss=Nmiss, **{"tab_reg":tab_reg},**{"tab_miss":tab_miss}, n_mod=n_mod)

@app.route("/adminips_<ips_usr>", methods=['GET', 'POST'])
@login_required
def adminips_(ips_usr):
    
    #print('IPS ID',ips_usr)
    usr =   IPS_data.find({"ID":int(ips_usr)})[0]
    general_info={
                  "Código Habilitación":usr['Código Habilitación'],
                  "Nombre del Prestador":usr['Nombre del Prestador'],
                  "NIT":usr['NIT'],
                  "Razón social":usr['Razón social'],
                  "Nivel del Prestador":usr["Nivel del Prestador"],
                  "Gerente":usr["Gerente"],
                  "Dirección":usr["Dirección"],
                  "Barrio":usr["Barrio"],
                  "Municipio":usr["Municipio"],
                  "Código Municipio":usr["Código Municipio"],
                  "Departamento":usr["Departamento"],
                  "Código Departamento":usr["Código Departamento"],
                  "Teléfono":usr["Teléfono"],
                  "E-mail empresarial":usr["E-mail empresarial"],
                  "Representante legal":usr["Representante legal"],
                  "E-mail del representante":usr["E-mail del representante"],
                  "Teléfono del representate":usr["Teléfono del representate"],
                  "Encargado de Encuesta":usr["Encargado de Encuesta"],
                  "E-mail del Encargado":usr["E-mail del Encargado"],
                  "Teléfono del Encargado":usr["Teléfono del Encargado"],            
    }
    for idx in range(1,7):
        general_info['name'+str(idx)] =usr['colaborador'+str(idx)+' nombre']
        general_info['cargo'+str(idx)] =usr['colaborador'+str(idx)+' cargo']
        general_info['email'+str(idx)] =usr['colaborador'+str(idx)+' email']
            
    Resultados_mod1=usr["Resultados Modulo 1"]
    Resultados_mod2=usr["Resultados Modulo 2"]
    Resultados_mod3=usr["Resultados Modulo 3"]
    Resultados_mod4=usr["Resultados Modulo 4"]
    Resultados_mod5=usr["Resultados Modulo 5"]
    Resultados_mod6=usr["Resultados Modulo 6"]

    perc_mod=[int(100*(len(Resultados_mod1)-1)/84), int(100*(len(Resultados_mod2)-1)/31), int(100*(len(Resultados_mod3)-1)/29), int(100*(len(Resultados_mod4)-1)/3), int(100*(len(Resultados_mod5)-1)/4), int(100*(len(Resultados_mod6)-1)/3)]
    perc_mod=np.asarray(perc_mod)
    find0=np.asarray(np.where(np.asarray(perc_mod)<0)[0])

    perc_mod[find0]=0
    find100=np.asarray(np.where(np.asarray(perc_mod)>100)[0])
    
    perc_mod[find100]=100

    if len(Resultados_mod6)>0:
        if Resultados_mod6["question1"].find("NO")>=0:
            perc_mod[5]=100

    
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
                #print(reg["Resultados Modulo "+str(modulo)])
                row = row + 1

                data=reg["Resultados Modulo "+str(modulo)]

                for key in data.keys():
                    df.loc[row,key] = data[key]
        #print(df)
        csv_file=df.to_csv(sep='\t')


        resp = make_response(csv_file)
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    return render_template('admin.html')




@app.route("/sendmail<modulo>", methods=['GET', 'POST'])
@login_required
def sendmail(modulo):
    if request.method == 'POST': 
        nombres=request.form['nombre'+str(modulo)]

        usr_id = int(current_user.id)
        usrid = Users_data.find({"user_id":usr_id})[0]
        user_encargado=usrid["usuario"]
        user=user_encargado+"colab"+str(modulo)
        usrid_colab = Users_data.find({"usuario":user})[0]
        key_pass=usrid_colab["password_nc"]
        to_email=request.form['email'+str(modulo)]
        send_email(to_email, nombres, user, key_pass, modulo, file_email="./templates/email.html")
        return redirect(url_for('modulos'))
    return redirect(url_for('modulos'))




if __name__ == "__main__":
    app.run()

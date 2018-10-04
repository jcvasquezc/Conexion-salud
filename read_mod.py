# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 12:13:20 2018

@author: TOMAS
"""
import pandas as pd
import numpy as np
import plot_map
import plotly
from collections import Counter

#******************************************************************
#******************************************************************
#******************************************************************
def leer_rta_mod(db_files,mod):
    file_path = './BD/'+db_files[mod]
    #Leer archivo de excel con respuestas de modulos
    file_path = './BD/'+db_files[mod]
    mod_data = pd.read_excel(file_path)
    mod_data = mod_data.fillna('NO')#Cambiar 'NaN' por 'NO'
    return mod_data

#******************************************************************
#******************************************************************
#******************************************************************

def leer_pregunta(mod_data,IPS,numpreg,usr_name = 'ID'):
    preg_label = 'Pregunta: '+numpreg #Etiqueta de la pregunta en la BD
    #Leer todas las respuestas asociadas a "preg_label"
    colnames = list(mod_data.columns)
    sel_col =[usr_name]    
    for idxcol in colnames:
        preg_ops = preg_label+'_'#Si la pregunta tiene otra opcion que se despliega
        if (preg_label==idxcol)or(idxcol.find(preg_ops)!=-1):
            sel_col.extend([idxcol])

    answ = mod_data[sel_col]
    answ =answ.sort_values([usr_name], ascending=[1])
    answ = answ.reset_index(drop=True)

    #Agregar informacon de la ciudad y el departamento
    usrs = list(answ[usr_name])
    usr_info = IPS[IPS[usr_name].isin(usrs)]
    usr_info = usr_info[[usr_name,'Municipio','Departamento']]
    usr_info = usr_info.sort_values([usr_name], ascending=[1])
    usr_info = usr_info.drop([usr_name],axis=1)
    usr_info = usr_info.reset_index(drop=True)

    #Unir Info de usuario y respuesta
    tabla = usr_info.copy()
    tabla = tabla.join(answ)
    return tabla,sel_col

#******************************************************************
#******************************************************************
#******************************************************************

def ubicacion(tabla,dfpmap,qcol):
    """
    Agregar puntos en el mapa
    """
    dpto_mpio_db=np.asarray([tabla["Departamento"][j].upper() +"_"+tabla["Municipio"][j].upper() for j in range(len(tabla["Departamento"]))])
    lat = [str(dfpmap["lat"][j]) for j in range(len(dfpmap["lat"]))]
    lon = [str(dfpmap["lon"][j]) for j in range(len(dfpmap["lon"]))]
    dpto_mpio_pos=np.asarray([dfpmap["Departamento"][j].upper()+"_"+dfpmap["Municipio"][j].upper() for j in range(len(dfpmap["Departamento"]))])

    answer=[]
    sizemap=[]
    lonmap=[]
    latmap=[]
    city=[]

    for k in range(len(dpto_mpio_pos)):

        pmap=np.where(dpto_mpio_db==dpto_mpio_pos[k])[0]

        if len (pmap)>0:
            if len(pmap)==1:
                answer.append(tabla[qcol][pmap].values[0])
            else:
                answers=tabla[qcol][pmap].values

                sents_to_count = (word for word in answers if word[:1].isupper())
                c = Counter(sents_to_count)
                ans=c.most_common(1)

                answer.append(ans[0][0])

            sizemap.append(15)
            latmap.append(lat[k])
            lonmap.append(lon[k])
            city.append(dpto_mpio_db[pmap[0]])

    list_a=np.asarray(answer)
    n_ind=np.unique(list_a)

    print(len(list_a), len(answer), len(city), len(latmap))
    list_n=np.zeros(len(list_a))
    for j in range(len(n_ind)):
        pos_=np.where(list_a==n_ind[j])[0]

        list_n[pos_]=j

    return latmap, lonmap, sizemap, city,n_ind,list_n
#******************************************************************
#******************************************************************
#******************************************************************
def tabla_rtas(rtas,preg_label):
    dptos_map=rtas["Departamento"]
    dptos_map_unique=np.unique(dptos_map)
    tab_resp={}
    tab_resp["Departamento"]=dptos_map_unique
    ans_unique=np.unique(rtas[preg_label[0]])
    for k in ans_unique:
        tab_resp[k]=np.zeros(len(dptos_map_unique))
    for j in range(len(rtas[preg_label[0]])):
        dpto_actual=dptos_map[j]
        pos_dpto=np.where(dptos_map_unique==dpto_actual)[0]
        tab_resp[rtas[preg_label[0]][j]][pos_dpto]=tab_resp[rtas[preg_label[0]][j]][pos_dpto]+1

    tab_resp_sort=[]
    for j in range(len(dptos_map_unique)):
        tab1=dptos_map_unique[j]
        tab2=[int(tab_resp[ans_unique[k]][j]) for k in range(len(ans_unique))]
        tab_resp_sort.append([tab1]+tab2)
    
    return ans_unique,tab_resp_sort
#******************************************************************
#******************************************************************
#******************************************************************
def mapa_gral(sttmod,db_files,IPS,dfpmap,clr_rta):
    """
    Entradas:
        sttmod: Respuesta obtenida del usuario, desde la interfaz web (mapa.html)
        db_files: Lista con los archivos de excel que contienen las respuestas
        IPS: Informacion de las IPS
        dfpmap: Longitud y latitud para mapa
        clr_rta: Bnadera que indica que tipo de paleta de colores se debe usar en el mapa
                -'sval': Tipo de respuesta SI/NO
                -'mval': Multiples opciones, unica respuesta
    """
    #******************************************************************
    sep = sttmod.find('_')#El guion bajo separa entre modulo y pregunta
    mod = int(sttmod[0:sep])#Obtener numero del modulo
    numpreg = sttmod[sep+1:]#Obtener el numero de la pregunta
    #******************************************************************
    #Obetner respuestas
    mod_data = leer_rta_mod(db_files,mod)
    #******************************************************************
    #Obtener tabla de respuestas de un modulo (mod) y pregunta especificos (numpreg)
    rtas,sel_col = leer_pregunta(mod_data,IPS,numpreg)
    #******************************************************************
    #Obtener latitud, longitud, tamanno del marcador y ciudades
    preg_label = sel_col.copy()
    preg_label.remove('ID')#Dejar solo las etiquetas de las preguntas
    lat,lon,szmark,ctymap,n_ind,list_n = ubicacion(rtas,dfpmap,preg_label[0])
    #******************************************************************
    #Crear tabla para visualizar la cantidad de respuestas
    ans_unique,tab_resp_sort = tabla_rtas(rtas,preg_label)
    total = pd.DataFrame(tab_resp_sort)#Calcular total
    total = total.drop([0],axis=1)#Calcular total
    tab_total = np.sum(total.values,axis=0)#Calcular total
    #******************************************************************
    #Graficar
    df_title = pd.read_excel('./static/titulo_mapa.xlsx')#Titulo de la grafica
    numpreg = int(numpreg)#Numero de la pregunta
    maptit = df_title[(df_title['Modulo']==mod)&(df_title['Pregunta']==numpreg)]#Titulo de la grafica
    maptit = maptit['Titulo'].values[0]#Titulo de la grafica
    data, layout = plot_map.get_data_map(lat,lon,szmark, ctymap,n_ind,list_n,maptit,clr_rta)#Mapa
    fig = dict(data=data, layout=layout)
    maptxt = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div',filename='horizontal-legend')
    #******************************************************************
    return maptxt,ans_unique,tab_resp_sort,list(tab_total)
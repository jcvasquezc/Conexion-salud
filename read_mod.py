# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 12:13:20 2018

@author: TOMAS
"""
import pandas as pd
import numpy as np
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
    preg_label = 'Pregunta: '+str(numpreg)#Etiqueta de la pregunta en la BD
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

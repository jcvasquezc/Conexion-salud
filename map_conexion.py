#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  12 14:44:02 2017

@author: gita
"""
from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import base64
import os
import numpy as np
from utils import get_data_map, get_radar, compute_indicator_map
import unidecode
import pymongo
from pymongo import MongoClient #Manejos de base de datos
import pprint




def progreso_mod(ips):
    div=[93,25,29,3,3,5]

    if "question3" in ips["Resultados Modulo 5"].keys():
        if ips["Resultados Modulo 5"]["question3"][0]=="SI":
            div[4]=4

    perc_mod = []
    for idxmod in range(1,7):
        rtas = ips["Resultados Modulo "+str(idxmod)]
        cont = 0 #Contar respuestas
        for idx in rtas.keys():
            if "INGP" not in idx:
                cont = cont+1

        calc = int(100*(cont-1)/div[idxmod-1])#cont-1 por la etiqueta "ID"
        perc_mod.append(calc)


#    perc_mod=[int(100*(len(Resultados_mod1)-1)/div[0]), int(100*(len(Resultados_mod2)-1)/div[1]), int(100*(len(Resultados_mod3)-1)/div[2]), int(100*(len(Resultados_mod4)-1)/div[3]), int(100*(len(Resultados_mod5)-1)/div[4]), int(100*(len(Resultados_mod6)-1)/div[5])]

    perc_mod=np.asarray(perc_mod)
    find0=np.asarray(np.where(np.asarray(perc_mod)<0)[0])

    perc_mod[find0]=0
    find100=np.asarray(np.where(np.asarray(perc_mod)>100)[0])

    perc_mod[find100]=100

    if len(ips["Resultados Modulo 6"])>1:
        if ips["Resultados Modulo 6"]["question1"][0].find("NO")>=0:
            perc_mod[5]=100

    return perc_mod

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
application = app.server


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

client = MongoClient()
db = client.IPS_database

IPS_data  = db.IPS_collection
Users_data = db.Users_collection

dfpmap=pd.read_csv('./static/pos_col.csv')

lat=[str(dfpmap["lat"][j]) for j in range(len(dfpmap["lat"]))]
lon=[str(dfpmap["lon"][j]) for j in range(len(dfpmap["lon"]))]
dptos_all=np.asarray([dfpmap["Departamento"][j].upper() for j in range(len(dfpmap["lat"]))])
dptos = list(np.unique(dptos_all))
dptos=["TODOS"]+dptos
city_map=dfpmap["Municipio"]
dpto_map=[dfpmap["Departamento"][j].upper() for j in range(len(dfpmap["lat"]))]

token='pk.eyJ1IjoiamN2YXNxdWV6YyIsImEiOiJjajhpOHJzYzEwd2lhMndteGE3dXdoZ2JwIn0.FXt2St8t89mIZ-L-UpCYkg'

mapbox_access_token = token
datamap, layoutmap=get_data_map([4.6], [-74], [8], ['Bogotá'],[2], mapbox_access_token)

padding= ['0%' '0%' '0%' '0%']

padding2= ['20%' '0%' '0%' '0%']

app.layout = html.Div([

    html.Div([
        html.Label(["Departamento"]),
        dcc.Dropdown(id="dpto",
            options=[{'label': dptos[i], "value": dptos[i]} for i in range(len(dptos))]),
        html.Label(["Municipio"]),
        dcc.Dropdown(id="mpio",
            options=[{'label': "Municipio", "value": "Municipio"}]),
    ],style={'padding':padding,'columnCount': 2}),


    html.Div([
    dcc.Markdown(
        """


            Porcentaje de IPSs que han diligenciado la encuesta: '{}'

            Porcentaje de IPSs que han diligenciado la encuesta en el departamento: '{}'

            Porcentaje de IPSs que han diligenciado la encuesta en el municipio: '{}'

        """.replace('   ', '').format('0.0%', '0.0%', '0.0%')),
    ], id="porc", style={'width':'100%', 'display': 'inline-block'}),

    html.Div([
         dcc.Graph(id='map',
             figure={'data': datamap, 'layout': layoutmap}
             )
    ], style={'width':'100%',  'display': 'inline-block'}),


])


@app.callback(
     dash.dependencies.Output('mpio', 'options'),
     [dash.dependencies.Input('dpto', 'value'),
      ])
def update_mpio_drop(dpto):
    global dpto_c
    print(dpto, dpto_map[0])
    pos_dpto=np.where(dpto==np.asarray(dpto_map))
    print(pos_dpto)
    cities_dr=city_map[pos_dpto[0]].values
    dpto_c=dpto
    return [{'label': cities_dr[i], "value": cities_dr[i]} for i in range(len(cities_dr))]



@app.callback(
     dash.dependencies.Output('map', 'figure'),
     [dash.dependencies.Input('dpto', 'value'),
      ])
def update_map(dpto):

    Nregistered=0

    cities_all=[]
    dptos_all=[]
    ips_all=[]
    user_all=[]
    for docs in IPS_data.find():
        if docs["Validar INFO"]==True:#IPS REGISTRADAS
            Nregistered=Nregistered+1
            dptos_all.append(docs["Departamento"])
            cities_all.append(docs["Municipio"])
            ips_all.append(docs["Nombre del Prestador"])
            user_all.append(docs["ID"])
    print(dptos_all)
    print(cities_all)

    latmap=[]
    lonmap=[]
    sizemap=[]
    textmap=[]
    nivelmap=[]
    if dpto!="TODOS":
        for k in range(len(cities_all)):
            pmap=np.where(city_map==cities_all[k])[0]

            #print(citiesIPS[k], pos_map)
            if len(pmap)>0 and dptos_all[k]==dpto:
                # try:
                for docs in IPS_data.find({"Municipio": cities_all[k], "Departamento": dpto}):
                    name=docs["Nombre del Prestador"]
                    print(name)
                    prob=0
                    nivel=1

                    perc_mod = progreso_mod(docs)
                    perc_mod_str=[str(np.round(perc_mod[j])) for j in range(len(perc_mod))]

                    str_prgress=" \n\r Modulo 1: "+perc_mod_str[0]
                    str_prgress=str_prgress+" \n\r Modulo 2: "+perc_mod_str[1]+"%"
                    str_prgress=str_prgress+" \n\r Modulo 3: "+perc_mod_str[2]+"%"
                    str_prgress=str_prgress+" \n\r Modulo 4: "+perc_mod_str[3]+"%"
                    str_prgress=str_prgress+" \n\r Modulo 5: "+perc_mod_str[4]+"%"
                    str_prgress=str_prgress+" \n\r Modulo 6: "+perc_mod_str[5]+"%"

                    sizemap.append(15)
                    nivelmap.append(int(nivel))
                    latmap.append(lat[pmap[0]])
                    lonmap.append(lon[pmap[0]])

                    textmap.append(cities_all[k]+' \n\r '+name+str_prgress)
                # except:
                #     print(cities_all[k])
    else:
        for k in range(len(cities_all)):
            pmap=np.where(city_map==cities_all[k])[0]
            #pos_dep=np.where(dpto_map==dptos_all[k])[0]
            #pmap=np.intersect1d(pos_map, pos_dep)
            #print(pos_map, pos_dep, dptos_all[k], dpto_map[8])

            if len(pmap)>0:
                #try:

                for docs in IPS_data.find({"Municipio": cities_all[k]}):
                    name=docs["Nombre del Prestador"]
                    print(name)
                    prob=0
                    nivel=1
                    latmap.append(lat[pmap[0]])
                    lonmap.append(lon[pmap[0]])
                    sizemap.append(15)
                    nivelmap.append(int(nivel))

                    perc_mod = progreso_mod(docs)
                    perc_mod_str=[str(np.round(perc_mod[j])) for j in range(len(perc_mod))]

                    str_prgress=" \n\r Modulo 1: "+perc_mod_str[0]
                    str_prgress=str_prgress+" \n\r Modulo 2: "+perc_mod_str[1]+"%"
                    str_prgress=str_prgress+" \n\r Modulo 3: "+perc_mod_str[2]+"%"
                    str_prgress=str_prgress+" \n\r Modulo 4: "+perc_mod_str[3]+"%"
                    str_prgress=str_prgress+" \n\r Modulo 5: "+perc_mod_str[4]+"%"
                    str_prgress=str_prgress+" \n\r Modulo 6: "+perc_mod_str[5]+"%"



                    textmap.append(cities_all[k]+' \n\r '+name+str_prgress)
                    if float(lat[pmap[0]])>1000 or float(lon[pmap[0]])>1000:
                        print(lat[pmap[0]], lon[pmap[0]], cities_all[k], np.round(prob,3))
                #except:
                    #print(cities_all[k])

    datamap, layoutmap=get_data_map(latmap, lonmap, sizemap, textmap, nivelmap, mapbox_access_token)

    return {
            'data': datamap,
            'layout':layoutmap }






@app.callback(
     dash.dependencies.Output('porc', 'children'),
     [dash.dependencies.Input('dpto', 'value'),
     dash.dependencies.Input('mpio', 'value'),
      ])
def update_markdown(dpto, mpio):


    Nregistered_total=0
    miss_reg_total=0
    Nregistered_dpto=0
    miss_reg_dpto=0
    Nregistered_mpio=0
    miss_reg_mpio=0

    cities_all=[]
    dptos_all=[]
    ips_all=[]
    user_all=[]
    for docs in IPS_data.find():
        if docs["Validar INFO"]==True:#IPS REGISTRADAS
            Nregistered_total=Nregistered_total+1
            if docs["Departamento"]==dpto:
                Nregistered_dpto=Nregistered_dpto+1
            if docs["Municipio"]==mpio:
                Nregistered_mpio=Nregistered_mpio+1
        else:
            miss_reg_total=miss_reg_total+1
            if docs["Departamento"]==dpto:
                miss_reg_dpto=miss_reg_dpto+1
            if docs["Municipio"]==mpio:
                miss_reg_mpio=miss_reg_mpio+1

    perc1=str(np.round(100*Nregistered_total/miss_reg_total,2))+"%"
    perc2=str(np.round(100*Nregistered_dpto/miss_reg_dpto,2))+"%"
    perc3=str(np.round(100*Nregistered_mpio/miss_reg_mpio,2))+"%"
    return [dcc.Markdown(
            """


                Porcentaje de IPSs que han diligenciado la encuesta: '{}'

                Porcentaje de IPSs que han diligenciado la encuesta en el departamento: '{}'

                Porcentaje de IPSs que han diligenciado la encuesta en el municipio: '{}'

            """.replace('   ', '').format(perc1, perc2, perc3))]








if __name__ == '__main__':
    app.run_server()

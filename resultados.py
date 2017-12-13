import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import base64
import os
import numpy as np
from utils import get_data_map, get_radar
import unidecode
import pymongo
from pymongo import MongoClient

import pprint


app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})





## definiciones globales

main_path = os.path.dirname(os.path.abspath(__file__))
lista_dptos = pd.read_csv(main_path+'/static/lista_dptos.csv')
dfd = pd.DataFrame(lista_dptos)
dptos = list(np.unique(lista_dptos['Departamento']))
dptos=["TODOS"]+dptos

citiesIPS=list(np.unique(lista_dptos['Municipio']))


dptos_all=list(lista_dptos['Departamento'])
cities_all=list(lista_dptos['Municipio'])

img1file="./static/udea.jpg"
img2file="./static/colciencias.png"
img3file="./static/mintic.png"
dfpmap=pd.read_csv('./static/pos_col.csv')
lat=[str(dfpmap["lat"][j]) for j in range(len(dfpmap["lat"]))]
lon=[str(dfpmap["lon"][j]) for j in range(len(dfpmap["lon"]))]



city_map=dfpmap["Municipio"]
dpto_map=dfpmap["Departamento"]

encoded_image1=base64.b64encode(open(img1file, 'rb').read())
encoded_image2=base64.b64encode(open(img2file, 'rb').read())
encoded_image3=base64.b64encode(open(img3file, 'rb').read())

token='pk.eyJ1IjoiamN2YXNxdWV6YyIsImEiOiJjajhpOHJzYzEwd2lhMndteGE3dXdoZ2JwIn0.FXt2St8t89mIZ-L-UpCYkg'


mapbox_access_token = token

datamap, layoutmap=get_data_map([4.6], [-74], [8], ['Bogotá'],[2], mapbox_access_token)



############## data radar

refh=[0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
refl=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

data_ips_radar=[0.7, 0.2, 0.8, 0.95, 0.7, 0.7]
legends_radar=['Equipos \r\n conectados', 'Ancho de \r\n banda', 'Empleados \r\n con equipos', 'Empleados \r\n conectados','Conexiones/\r\nEmpleado', 'Equipos \r\n conectados', 'Ancho de \r\n banda']
data_radar, layout_radar=get_radar(refh, data_ips_radar, legends_radar)


### estilos
padding= ['0%' '10%' '0%' '10%']
padding2= ['0%' '0%' '0%' '10%']
padding3= ['0%' '0%' '0%' '5%']
border='thin lightgrey solid'

labels = [['1-5','6-10','11-20','>20'],
            ['<1Mbps','2-5Mbps','6-10Mbps','11-20Mbps', '>20Mbps'],
            ['1-10','11-30','31-50','51-100','>100'],
            ['1-10','11-30','31-50','51-100','>100']]
values = [[4500,2500,1053,500],[4500,2500,1053,500,500], [4500,2500,1053,500,200], [4500,2500,1053,500,450], [4500,2500,1053,500,50]]



client = MongoClient()
db = client['IPS_DEMODB']

collection=db["IPS_Demo_collection"]



print(collection.count())


app.layout = html.Div([
    html.Title("Estudio sobre el nivel de madurez del ecosistema de TIC en las IPS públicas"),

    html.Div([("Estudio sobre el nivel de madurez del ecosistema de TIC en las IPS públicas")], style={"padding":padding, "font-size":"180%", 'display': 'inline-block', "align-content":"center"}),

    html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()), style={"padding":padding2,'width': '10%', 'display': 'inline-block', 'columnCount': 3}),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), style={'width': '15%', 'display': 'inline-block', 'columnCount': 3}),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image3.decode()), style={'width': '30%', 'display': 'inline-block', 'columnCount': 3}),
            ]),

    html.Div(["\n"]),


    html.Div([
        html.Label(["Departamento"]),
        dcc.Dropdown(id="dpto",
            options=[{'label': dptos[i], "value": dptos[i]} for i in range(len(dptos))]),
        html.Label(["Municipio"]),
        dcc.Dropdown(id="mpio",
            options=[{'label': "Municipio", "value": "Municipio"}]),
        html.Label(["IPS"]),
        dcc.Dropdown(id="ips",
            options=[{'label': "IPS", "value": "IPS"}]),
    ],style={'padding':padding,'columnCount': 2}),


    html.Div([
        html.Div([

        dcc.Markdown(
            """
                Porcentaje de municipios conectados a internet: '{}'

                Porcentaje de municipios que cuentan con conexión inalambrica (Wifi): '{}'

                Porcentaje de municipios que cuentan con servidores para manejo de hisoria clínica: '{}'

                Porcentaje de municipios que cuentan con una dirección IP pública: '{}'

            """.replace('   ', '').format('0.0%', '0.0%', '0.0%', '0.0%'), id="porc"),
        ], style={'width':'100%', 'display': 'inline-block'}),

        html.Div([
         dcc.Graph(id='radar',
             figure={'data': data_radar, 'layout': go.Layout(layout_radar)}
             ),
        ], style={'width':'100%', 'display': 'inline-block'}),

        html.Div([
         dcc.Graph(id='map',
             figure={'data': datamap, 'layout': layoutmap}
             )
    ], style={'width':'100%', 'display': 'inline-block'}),
    ], style={'columnCount': 2, 'padding': padding}),



    html.Div([
        html.Div([
         dcc.Graph(
             id='p2',
             figure={'data': [
                     go.Pie(labels=labels[0], values=values[0])],
                 'layout': go.Layout(
                     title='Num. Equipos conectados a internet',
                 )
             }
         )], style={'width': '100%', 'display': 'inline-block'}),

        html.Div([
         dcc.Graph(
             id='p5',
             figure={'data': [
                     go.Pie(labels=labels[1], values=values[1])],
                 'layout': go.Layout(
                     title='Ancho de banda de conexión a internet',

                 )

             }
         )], style={'width': '100%', 'display': 'inline-block'}),

        html.Div([
         dcc.Graph(
             id='p6',
             figure={'data': [
                     go.Pie(labels=labels[2], values=values[2])],
                 'layout': go.Layout(
                     title='Num. Empleados con equipos de computo',
                 )

             }
         )], style={'width': '100%', 'display': 'inline-block'}),

        html.Div([
         dcc.Graph(
             id='p7',
             figure={'data': [
                     go.Pie(labels=labels[3], values=values[3])],
                 'layout': go.Layout(
                     title='Num. Empleados con acceso a internet',
                 )

             }
         )], style={'width': '100%', 'display': 'inline-block'}),
     ], style={'padding':padding,'columnCount': 2}),




])


@app.callback(
     dash.dependencies.Output('map', 'figure'),
     [dash.dependencies.Input('dpto', 'value'),
      ])
def update_map(dpto):

    latmap=[]
    lonmap=[]
    sizemap=[]
    textmap=[]
    nivelmap=[]
    if dpto!="TODOS":
        for k in range(len(cities_all)):
            pos_map=np.where(city_map==cities_all[k])[0]
            pos_dep=np.where(dpto_map==dptos_all[k])[0]
            #print(citiesIPS[k], pos_map)
            pmap=np.intersect1d(pos_map, pos_dep)
            if len(pos_map)>0 and len(pos_dep)>0 and dptos_all[k]==dpto:
                try:
                    latmap.append(lat[pmap[0]])
                    lonmap.append(lon[pmap[0]])
                    prob=np.random.rand(1)
                    sizemap.append(int(np.ceil((prob*30)))+4)
                    nivelmap.append(int(3*np.random.rand(1))+1)
                    textmap.append(cities_all[k]+'\n\r'+"Indicador conectividad="+str(np.round(prob[0],3)))
                except:
                    print(cities_all[k])
    else:
        for k in range(len(cities_all)):
            pos_map=np.where(city_map==cities_all[k])[0]
            pos_dep=np.where(dpto_map==dptos_all[k])[0]
            #print(citiesIPS[k], pos_map)
            pmap=np.intersect1d(pos_map, pos_dep)
            if len(pos_map)>0 and len(pos_dep)>0:
                try:
                    latmap.append(lat[pmap[0]])
                    lonmap.append(lon[pmap[0]])
                    prob=np.random.rand(1)
                    sizemap.append(int(np.ceil((prob*30)))+4)
                    nivelmap.append(int(3*np.random.rand(1))+1)
                    textmap.append(cities_all[k]+'\n\r'+"Indicador conectividad="+str(np.round(prob[0],3)))
                except:
                    print(cities_all[k])


    datamap, layoutmap=get_data_map(latmap, lonmap, sizemap, textmap, nivelmap, mapbox_access_token)

    return {
            'data': datamap,
            'layout':layoutmap }

@app.callback(
     dash.dependencies.Output('mpio', 'options'),
     [dash.dependencies.Input('dpto', 'value'),
      ])
def update_mpio_drop(dpto):

    pos_dpto=np.where(dpto==dpto_map)
    cities_dr=city_map[pos_dpto[0]].values
    print(cities_dr)
    return [{'label': cities_dr[i], "value": cities_dr[i]} for i in range(len(cities_dr))]






if __name__ == '__main__':
    app.run_server()

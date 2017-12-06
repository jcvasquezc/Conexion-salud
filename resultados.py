import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import base64
import os
import numpy as np
from utils import get_data_map, get_data_radar


df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})




## definiciones globales

main_path = os.path.dirname(os.path.abspath(__file__))
lista_dptos = pd.read_csv(main_path+'/static/lista_dptos.csv')
dfd = pd.DataFrame(lista_dptos)
dptos = list(np.unique(lista_dptos['Departamento']))

img1file="./static/udea.jpg"
img2file="./static/colciencias.png"
img3file="./static/mintic.png"
encoded_image1=base64.b64encode(open(img1file, 'rb').read())
encoded_image2=base64.b64encode(open(img2file, 'rb').read())
encoded_image3=base64.b64encode(open(img3file, 'rb').read())

token='pk.eyJ1IjoiamN2YXNxdWV6YyIsImEiOiJjajhpOHJzYzEwd2lhMndteGE3dXdoZ2JwIn0.FXt2St8t89mIZ-L-UpCYkg'


mapbox_access_token = token

datamap, layoutmap=get_data_map([], mapbox_access_token)






############## data radar

refh=[0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
refl=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

data_ips_radar=[0.7, 0.2, 0.8, 0.95, 0.7, 0.7]
data_radar, layout_radar=get_data_radar(refh, refl, data_ips_radar)




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
        dcc.Markdown(
            """
                Porcentaje de municipios conectados a internet: '{}'

                Porcentaje de municipios que cuentan con conexión inalambrica (Wifi): '{}'

                Porcentaje de municipios que cuentan con servidores para manejo de hisoria clínica: '{}'

                Porcentaje de municipios que cuentan con una dirección IP pública: '{}'

            """.replace('   ', '').format('0.0%', '0.0%', '0.0%', '0.0%'), id="porc"),

         dcc.Graph(id='radar',
             figure={'data': data_radar, 'layout': layout_radar}
             ),
         dcc.Graph(id='map',
             figure={'data': datamap, 'layout': layoutmap}
             )
    ], style={'columnCount': 2, 'padding': padding, 'display': 'inline-block'}),



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
         )], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
         dcc.Graph(
             id='p5',
             figure={'data': [
                     go.Pie(labels=labels[1], values=values[1])],
                 'layout': go.Layout(
                     title='Ancho de banda de conexión a internet',

                 )

             }
         )], style={'width': '33%', 'display': 'inline-block'}),

        html.Div([
         dcc.Graph(
             id='p6',
             figure={'data': [
                     go.Pie(labels=labels[2], values=values[2])],
                 'layout': go.Layout(
                     title='Num. Empleados con equipos de computo',
                 )

             }
         )], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
         dcc.Graph(
             id='p7',
             figure={'data': [
                     go.Pie(labels=labels[3], values=values[3])],
                 'layout': go.Layout(
                     title='Num. Empleados con acceso a internet',
                 )

             }
         )], style={'width': '30%', 'display': 'inline-block'}),
     ], style={'padding':padding}),




])





#
#
# @app.callback(
#     dash.dependencies.Output('graph-with-slider', 'figure'),
#     [dash.dependencies.Input('year-slider', 'value')])
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#     traces = []
#     for i in filtered_df.continent.unique():
#         df_by_continent = filtered_df[filtered_df['continent'] == i]
#         traces.append(go.Scatter(
#             x=df_by_continent['gdpPercap'],
#             y=df_by_continent['lifeExp'],
#             text=df_by_continent['country'],
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 15,
#                 'line': {'width': 0.5, 'color': 'white'}
#             },
#             name=i
#         ))
#
#     return {
#         'data': traces,
#         'layout': go.Layout(
#             xaxis={'type': 'log', 'title': 'GDP Per Capita'},
#             yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest'
#         )
#     }


if __name__ == '__main__':
    app.run_server()

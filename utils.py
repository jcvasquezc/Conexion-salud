import plotly.graph_objs as go
import numpy as np


def get_data_map(lati, longi, sizem, textm, mapbox_access_token):
    #print(textm)
    datamap = go.Data([
        go.Scattermapbox(
            lat=lati,
            lon=longi,
            mode='markers',
            marker=go.Marker(size=sizem),
            text=textm,
        )
    ])

    layoutmap = go.Layout(
        title="Estado de conectividad de IPS públicas en Colombia",
        hovermode='closest',
        autosize=False,
        width=600,
        height=800,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=4.6,
                lon=-74.09
            ),
            domain=dict(
                    x=[0,1],
                    y=[0,1]
                ),
            pitch=0,
            style='light',
            zoom=4.5
        ),
    )
    return datamap, layoutmap


def get_data_radar(refh, refl, data_ips_radar):
    datap = []
    datap.append(
        go.Scatter(
            t=np.arange(0,360+72,72),
            r=refh,
            name = 'Referencia',
            mode='lines',
            fill="toself",
            marker = dict(color = "white",
                        size = 6,
                        line = dict(width = 4, color='rgb(69,124,235, 0.5)')),
    ))

    datap.append(
        go.Scatter(
            t=np.arange(0,360+72,72),
            r=refh,
            name="",
            showlegend = False,
            mode='markers',
            marker=dict(
                color='rgb(80,140,235, 0.5)',
                size=20 )
    ))

    datap.append(
        go.Scatter(
            t=np.arange(0,360+72,72),
            r=data_ips_radar,
            name = 'Su IPS',
            mode = "lines",
            fill="toself",
            marker = dict(color = "white",
                        size = 4,
                        line = dict(width = 4, color='rgb(255,78,252, 0.5)')),
    ))




    datap.append(
        go.Scatter(
            #t=np.arange(0,360+72,72),
            t=['Equipos conectados', 'Ancho de banda', 'Empleados con equipos', 'Empleados conectados', 'Conexiones/Empleado'],
            r=data_ips_radar,
            name="",
            showlegend = False,
            mode = "markers",
            marker=dict(
                color='rgb(255,78,252, 0.5)',
                size=20 )
    ))

    layoutp = go.Layout(
             hovermode='closest',
             legend = dict(x = 0.0, y = 0.0, bgcolor = "transparent"),
             plot_bgcolor = 'rgba(240,240,240, 0.5)',
             orientation=270,

             width=600,
             height=600,
             title="Estado de conectividad de su IPS respecto al promedio de la región",
             paper_bgcolor = 'rgba(255,255,255, 0.5)')


    return datap, layoutp

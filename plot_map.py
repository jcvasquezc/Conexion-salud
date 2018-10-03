# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 12:16:14 2018

@author: TOMAS
"""

import plotly.graph_objs as go
import numpy as np

#Token para mapaplotly
token = 'pk.eyJ1IjoiamN2YXNxdWV6YyIsImEiOiJjajhpOHJzYzEwd2lhMndteGE3dXdoZ2JwIn0.FXt2St8t89mIZ-L-UpCYkg'
mapbox_access_token = token

colorlist = [
    'rgba(0,0,255,0.7)',
    'rgba(0,255,0,0.7)',
    'rgba(255,0,0,0.7)',
    'rgba(255,128,0,0.7)',
    'rgba(255,51,51,0.7)',
    'rgba(153,0,0,0.7)'
]

#***************************************************************************
#***************************************************************************
def get_data_map(lati, longi, sizem, textm,resp, nivel,mapname):
    #print(textm)
    latl=[]
    longl=[]
    sizel=[]
    textl=[]
    lati=np.asarray(lati)
    longi=np.asarray(longi)
    sizem=np.asarray(sizem)

    for j in np.unique(nivel):

        pos=np.where(nivel==j)[0]
        latl.append(lati[pos])
        longl.append(longi[pos])
        sizel.append(sizem[pos])
        textl.append([textm[k] for k in pos])

    datamap = go.Data([
        go.Scattermapbox(
            lat=latl[j],
            lon=longl[j],
            mode='markers',
            name= resp[j],
            marker=go.Marker(size=sizel[j],
            color=colorlist[j],
            ),
            text=textl[j],
        )
    for j in range(len(np.unique(nivel)))] )

    layoutmap = go.Layout(
        title=mapname,
        hovermode='closest',
#        sizing= "stretch",
        autosize=True,
#        width = 800,
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
#***************************************************************************
#***************************************************************************
#***************************************************************************

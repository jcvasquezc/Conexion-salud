import pandas as pd


df=pd.read_csv('./static/encuestaMod2.csv')
df.head
Nq=len(df)
l=0
pregunta=[]
for j in range(Nq):
    if df["Tipo"][j]=="checkbox":
        pregunta.append('<div class="row">')
        pregunta.append('  <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">')
        pregunta.append('    <label for="question'+str(j+1)+'"><h4>'+str(j+1)+'. '+df['Pregunta'][j]+'</h4></label>')
        pregunta.append('    <a href="#" data-toggle="tooltip" title=""'+df["Ayuda"][j]+'""><i class="fa fa-question-circle" style=font-size:24px></i></a><br>')
        pregunta.append('  </div>')
        pregunta.append('</div>')
        pregunta.append('<div class="row">')
        pregunta.append('  <div class="col-xs-8 col-sm-8 col-md-8 col-lg-8">')
        respuestas=df["Respuestas"][j].split(';')
        for k in range(len(respuestas)):
            if respuestas[k]=='Otro' or respuestas[k]=='Otros:':
                l=l+1
                pregunta.append('    <label><input type="checkbox" class="option-input checkbox" id="question'+str(j+1)+'" name="cboxq'+str(j+1)+'" value="'+str(k+1)+'" onclick="var input=document.getElementById(\'name'+str(l)+'\'); if(this.checked){ input.disabled = false; input.focus();}else{input.disabled=true;}" />Otro<br><input id=" name'+str(l)+'" name=" name'+str(l)+'" disabled="disabled"/></label><br>')
                print(pregunta[-1])
            else:
                pregunta.append('    <label><input type="checkbox" id="question'+str(j+1)+'" ondragover="" class="option-input checkbox" name="cboxq'+str(j+1)+'" value="'+str(k+1)+'"> '+respuestas[k]+'</label><br>')
        pregunta.append('    <br>')
        pregunta.append('  </div>')
        pregunta.append('</div>')
        if df["Adjuntar"][j]=='SI' or df["Adjuntar"][j]=='si':
            pregunta.append('<div class="row">')
            pregunta.append('  <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">')
            pregunta.append('    <label>Adjuntar soporte:</label>')
            pregunta.append('    <input type="file" id="file_p'+str(j+1)+'" name="file_p'+str(j+1)+'" accept="image/*,video/*" onchange="enb_dis(\'file_p'+str(j+1)+'\',\'del_p'+str(j+1)+'\')"/>')
            pregunta.append('    <br><br>')
            pregunta.append('    <button type="button" id="del_p'+str(j+1)+'" class="state" onclick="delete_attached(\'del_p'+str(j+1)+'\',\'file_p'+str(j+1)+'\')" disabled="disabled">Eliminar soporte</button>')
            pregunta.append('  </div>')
            pregunta.append('</div>')
        pregunta.append('<br><hr>')
    elif df["Tipo"][j]=="radio":
        pregunta.append('<div class="row">')
        pregunta.append('  <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">')
        pregunta.append('    <label for="question'+str(j+1)+'"><h4>'+str(j+1)+'. '+df['Pregunta'][j]+'</h4></label>')
        pregunta.append('    <a href="#" data-toggle="tooltip" title=""'+df["Ayuda"][j]+'""><i class="fa fa-question-circle" style=font-size:24px></i></a><br>')
        pregunta.append('  </div>')
        pregunta.append('</div>')
        pregunta.append('<div class="row">')
        pregunta.append('  <div class="col-xs-8 col-sm-8 col-md-8 col-lg-8">')
        respuestas=df["Respuestas"][j].split(';')
        for k in range(len(respuestas)):
            if respuestas[k]=='Otro' or respuestas[k]=='Otros:':
                l=l+1
                pregunta.append('    <input type="radio" class="option-input radio" id="question'+str(k+1)+'" name="question'+str(j+1)+'" value="'+str(k+1)+'" onclick="var input = document.getElementById(\'name'+str(l)+'\'); if(this.checked){ input.disabled = false; input.focus();}else{input.disabled=true;}" />Otro<br><input id="name'+str(l)+'" name="name'+str(l)+'" disabled="disabled"/><br>')
            else:
                pregunta.append('	 <input type="radio" class="option-input radio" id="question'+str(k+1)+'" name="question'+str(j+1)+'" value="'+str(k+1)+'" required>'+respuestas[k]+'<br>')
        pregunta.append('    <br>')
        pregunta.append('  </div>')
        pregunta.append('</div>')
        if df["Adjuntar"][j]=='SI' or df["Adjuntar"][j]=='si':
            pregunta.append('<div class="row">')
            pregunta.append('  <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">')
            pregunta.append('    <label>Adjuntar soporte:</label>')
            pregunta.append('    <input type="file" id="file_p'+str(j+1)+'" name="file_p'+str(j+1)+'" accept="image/*,video/*" onchange="enb_dis(\'file_p'+str(j+1)+'\',\'del_p'+str(j+1)+'\')"/>')
            pregunta.append('    <br><br>')
            pregunta.append('    <button type="button" id="del_p'+str(j+1)+'" class="state" onclick="delete_attached(\'del_p'+str(j+1)+'\',\'file_p'+str(j+1)+'\')" disabled="disabled">Eliminar soporte</button>')
            pregunta.append('  </div>')
            pregunta.append('</div>')
        pregunta.append('<br><hr>')
    elif df["Tipo"][j]=="input":
        pregunta.append('<div class="row">')
        pregunta.append('  <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">')
        pregunta.append('    <label for="question'+str(j+1)+'"><h4>'+str(j+1)+'. '+df['Pregunta'][j]+'</h4></label>')
        pregunta.append('    <a href="#" data-toggle="tooltip" title=""'+df["Ayuda"][j]+'""><i class="fa fa-question-circle" style=font-size:24px></i></a><br>')
        pregunta.append('  </div>')
        pregunta.append('</div>')
        respuestas=df["Respuestas"][j].split(';')
        for k in range(len(respuestas)):
            if respuestas[k]=='Otro' or respuestas[k]=='Otros:':
                l=l+1
                pregunta.append('<div class="row">')
                pregunta.append('  <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">')
                pregunta.append('      <label>Otro:</label>')
                pregunta.append('  </div>')
                pregunta.append('  <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">')
                pregunta.append('    <input type="text" id="q'+str(j+1)+'f'+str(k+1)+'" name="q'+str(j+1)+'f'+str(k+1)+'" placeholder="Cuál?" required><br>')
                pregunta.append('    <input id="name'+str(j+1)+'" name="name'+str(j+1)+'"  placeholder="Cuántos?"/></label>')
                pregunta.append('  </div>')
                pregunta.append('</div>')
            else:
                pregunta.append('<div class="row">')
                pregunta.append('  <div class="col-xs-12 col-sm-3 col-md-3 col-lg-2">')
                pregunta.append('      <label>'+respuestas[k]+'</label>')
                pregunta.append('  </div>')
                pregunta.append('  <div class="col-xs-12 col-sm-2 col-md-2 col-lg-1">')
                pregunta.append('    <input type="text" id="q'+str(j+1)+'f'+str(k+1)+'" name="q'+str(j+1)+'f'+str(k+1)+'" placeholder="0" required><br>')
                pregunta.append('  </div>')
                pregunta.append('</div>')
        pregunta.append('    <br>')
        if df["Adjuntar"][j]=='SI' or df["Adjuntar"][j]=='si':
            pregunta.append('<div class="row">')
            pregunta.append('  <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">')
            pregunta.append('    <label>Adjuntar soporte:</label>')
            pregunta.append('    <input type="file" id="file_p'+str(j+1)+'" name="file_p'+str(j+1)+'" accept="image/*,video/*" onchange="enb_dis(\'file_p'+str(j+1)+'\',\'del_p'+str(j+1)+'\')"/>')
            pregunta.append('    <br><br>')
            pregunta.append('    <button type="button" id="del_p'+str(j+1)+'" class="state" onclick="delete_attached(\'del_p'+str(j+1)+'\',\'file_p'+str(j+1)+'\')" disabled="disabled">Eliminar soporte</button>')
            pregunta.append('  </div>')
            pregunta.append('</div>')
        pregunta.append('<br><hr>')
    elif df["Tipo"][j]=="text":
        pregunta.append('<div class="row">')
        pregunta.append('  <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">')
        pregunta.append('    <label for="question'+str(j+1)+'"><h4>'+str(j+1)+'. '+df['Pregunta'][j]+'</h4></label>')
        pregunta.append('  </div>')
        pregunta.append('</div>')
        pregunta.append('<br><hr>')



header1=open('./templates/header1.txt', 'r')
header1txt=header1.read()

header2=open('./templates/header2.txt', 'r')
header2txt=header2.read()


file_preg = open('./templates/preguntas_mod2.html','w')

file_preg.write(header1txt)
file_preg.write('\n\r')

for j in range(len(pregunta)):
    file_preg.write(pregunta[j])
    file_preg.write('\n\r')

file_preg.write(header2txt)
file_preg.write('\n\r')


file_preg.close()
